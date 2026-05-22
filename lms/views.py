from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Course, Assignment, Submission, Quiz, Question, QuizAttempt, LiveClass
from .forms import AssignmentForm, SubmissionForm, QuizForm, QuestionForm, LiveClassForm


def role_required(role):
    from functools import wraps
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role != role:
                messages.error(request, f'This page is only for {role}s.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


# ── ASSIGNMENTS ───────────────────────────────────────────────────────────────
@login_required
def assignments_list(request):
    user = request.user
    if user.role == 'teacher':
        assignments = Assignment.objects.filter(created_by=user).select_related('course')
    else:
        assignments = Assignment.objects.filter(
            course__in=user.enrolled_courses.all()
        ).select_related('course')
    return render(request, 'lms/assignments.html', {'assignments': assignments})


@login_required
@role_required('teacher')
def assignment_create(request):
    form = AssignmentForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        messages.success(request, 'Assignment created successfully!')
        return redirect('assignments_list')
    return render(request, 'lms/assignment_form.html', {'form': form, 'action': 'Create'})


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    user = request.user
    submission = None
    all_submissions = None
    form = None

    if user.role == 'student':
        submission = Submission.objects.filter(assignment=assignment, student=user).first()
        if not submission:
            form = SubmissionForm(request.POST or None, request.FILES or None)
            if request.method == 'POST' and form.is_valid():
                sub = form.save(commit=False)
                sub.assignment = assignment
                sub.student = user
                if timezone.now() > assignment.due_date:
                    sub.status = 'late'
                sub.save()
                messages.success(request, 'Assignment submitted!')
                return redirect('assignment_detail', pk=pk)
    else:
        all_submissions = assignment.submissions.select_related('student').all()

    context = {
        'assignment': assignment,
        'submission': submission,
        'all_submissions': all_submissions,
        'form': form,
    }
    return render(request, 'lms/assignment_detail.html', context)


@login_required
@role_required('teacher')
def grade_submission(request, sub_pk):
    submission = get_object_or_404(Submission, pk=sub_pk)
    if request.method == 'POST':
        marks    = request.POST.get('marks')
        feedback = request.POST.get('feedback', '')
        submission.marks_obtained = marks
        submission.feedback = feedback
        submission.status = 'graded'
        submission.save()
        messages.success(request, f'Submission graded: {marks} marks')
    return redirect('assignment_detail', pk=submission.assignment.pk)


# ── QUIZZES ───────────────────────────────────────────────────────────────────
@login_required
def quizzes_list(request):
    user = request.user
    if user.role == 'teacher':
        quizzes = Quiz.objects.filter(created_by=user).select_related('course')
    else:
        quizzes = Quiz.objects.filter(course__in=user.enrolled_courses.all()).select_related('course')
    return render(request, 'lms/quizzes.html', {'quizzes': quizzes})


@login_required
@role_required('teacher')
def quiz_create(request):
    form = QuizForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        messages.success(request, 'Quiz created! Now add questions.')
        return redirect('quiz_add_question', pk=obj.pk)
    return render(request, 'lms/quiz_form.html', {'form': form, 'action': 'Create'})


@login_required
@role_required('teacher')
def quiz_add_question(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    form = QuestionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        q = form.save(commit=False)
        q.quiz = quiz
        q.save()
        messages.success(request, 'Question added!')
        return redirect('quiz_add_question', pk=pk)
    questions = quiz.questions.all()
    return render(request, 'lms/quiz_add_question.html', {'quiz': quiz, 'form': form, 'questions': questions})


@login_required
@role_required('student')
def quiz_take(request, pk):
    quiz    = get_object_or_404(Quiz, pk=pk)
    attempt = QuizAttempt.objects.filter(quiz=quiz, student=request.user).first()
    if attempt:
        messages.info(request, f'You already attempted this quiz. Score: {attempt.score}')
        return redirect('quizzes_list')

    questions = quiz.questions.all()
    if request.method == 'POST':
        score = 0
        for q in questions:
            answer = request.POST.get(f'q_{q.pk}', '')
            if answer == q.correct_option:
                score += q.marks
        QuizAttempt.objects.create(quiz=quiz, student=request.user, score=score)
        messages.success(request, f'Quiz submitted! Your score: {score}/{quiz.total_marks}')
        return redirect('quizzes_list')

    return render(request, 'lms/quiz_take.html', {'quiz': quiz, 'questions': questions})


# ── LIVE CLASSES ──────────────────────────────────────────────────────────────
@login_required
def live_classes_list(request):
    user = request.user
    if user.role == 'teacher':
        classes = LiveClass.objects.filter(created_by=user).select_related('course')
    else:
        classes = LiveClass.objects.filter(
            course__in=user.enrolled_courses.all()
        ).select_related('course')
    return render(request, 'lms/live_classes.html', {'classes': classes})


@login_required
@role_required('teacher')
def live_class_create(request):
    form = LiveClassForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        messages.success(request, 'Live class scheduled!')
        return redirect('live_classes_list')
    return render(request, 'lms/live_class_form.html', {'form': form, 'action': 'Schedule'})


@login_required
@role_required('teacher')
def live_class_update_status(request, pk):
    lc = get_object_or_404(LiveClass, pk=pk, created_by=request.user)
    status = request.POST.get('status')
    if status in dict(LiveClass.STATUS_CHOICES):
        lc.status = status
        lc.save()
        messages.success(request, f'Class status updated to {lc.get_status_display()}')
    return redirect('live_classes_list')