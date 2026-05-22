from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from .models import Grade, Notification, Attendance
from lms.models import Course, Assignment, Submission, Quiz, QuizAttempt, LiveClass


def role_required(role):
    """Decorator to restrict views by role."""
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


@login_required
def dashboard(request):
    user = request.user
    if user.role == 'teacher':
        return teacher_dashboard(request)
    return student_dashboard(request)


def student_dashboard(request):
    user = request.user
    grades       = Grade.objects.filter(student=user).select_related('course').order_by('-score')
    notifications = Notification.objects.filter(
        Q(recipient=user) | Q(recipient__isnull=True)
    ).order_by('-created_at')[:10]
    attendance   = Attendance.objects.filter(student=user)
    courses      = user.enrolled_courses.all()
    upcoming     = LiveClass.objects.filter(
        course__in=courses, status__in=['scheduled', 'live']
    ).order_by('date', 'start_time')[:5]
    pending_assignments = Assignment.objects.filter(
        course__in=courses
    ).exclude(submissions__student=user).order_by('due_date')[:5]

    # Attendance summary
    total_att   = attendance.count()
    present_att = attendance.filter(status='present').count()
    att_pct     = round((present_att / total_att * 100) if total_att else 0)

    # Monthly performance (last 6 months)
    from datetime import date, timedelta
    from django.db.models.functions import TruncMonth
    monthly = (
        Grade.objects.filter(student=user)
        .values('course__name')
        .annotate(avg=Avg('score'))
    )

    context = {
        'grades': grades,
        'notifications': notifications,
        'upcoming': upcoming,
        'pending_assignments': pending_assignments,
        'att_pct': att_pct,
        'present_att': present_att,
        'total_att': total_att,
        'courses': courses,
    }
    return render(request, 'portal/student_dashboard.html', context)


def teacher_dashboard(request):
    user = request.user
    courses     = Course.objects.filter(teacher=user)
    assignments = Assignment.objects.filter(created_by=user).order_by('-created_at')[:5]
    quizzes     = Quiz.objects.filter(created_by=user).order_by('-created_at')[:5]
    live_classes = LiveClass.objects.filter(created_by=user).order_by('date', 'start_time')[:5]
    pending_subs = Submission.objects.filter(
        assignment__created_by=user, status='submitted'
    ).select_related('student', 'assignment').order_by('-submitted_at')[:10]

    context = {
        'courses': courses,
        'assignments': assignments,
        'quizzes': quizzes,
        'live_classes': live_classes,
        'pending_subs': pending_subs,
        'total_students': sum(c.students.count() for c in courses),
    }
    return render(request, 'portal/teacher_dashboard.html', context)


# ── GRADES ────────────────────────────────────────────────────────────────────
@login_required
@role_required('student')
def grades_view(request):
    grades = Grade.objects.filter(student=request.user).select_related('course').order_by('-score')
    avg = grades.aggregate(avg=Avg('score'))['avg'] or 0
    context = {'grades': grades, 'avg': round(float(avg), 2)}
    return render(request, 'portal/grades.html', context)


# ── NOTIFICATIONS ─────────────────────────────────────────────────────────────
@login_required
def notifications_view(request):
    user = request.user
    notifs = Notification.objects.filter(
        Q(recipient=user) | Q(recipient__isnull=True)
    ).order_by('-created_at')
    # Mark all as read
    notifs.filter(recipient=user, is_read=False).update(is_read=True)
    return render(request, 'portal/notifications.html', {'notifications': notifs})


# ── ATTENDANCE ────────────────────────────────────────────────────────────────
@login_required
@role_required('student')
def attendance_view(request):
    user    = request.user
    records = Attendance.objects.filter(student=user).select_related('course').order_by('-date')
    courses = user.enrolled_courses.all()

    # Per-course summary
    summary = []
    for course in courses:
        course_att = records.filter(course=course)
        total   = course_att.count()
        present = course_att.filter(status='present').count()
        late    = course_att.filter(status='late').count()
        absent  = course_att.filter(status='absent').count()
        pct     = round((present / total * 100) if total else 0)
        summary.append({
            'course': course,
            'total': total,
            'present': present,
            'late': late,
            'absent': absent,
            'pct': pct,
        })

    context = {'records': records, 'summary': summary}
    return render(request, 'portal/attendance.html', context)