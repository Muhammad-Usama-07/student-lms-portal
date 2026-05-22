from django.contrib import admin
from .models import Course, Assignment, Submission, Quiz, Question, QuizAttempt, LiveClass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display  = ('code', 'name', 'teacher')
    search_fields = ('code', 'name')
    filter_horizontal = ('students',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'created_by')
    list_filter  = ('course',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'marks_obtained', 'submitted_at')
    list_filter  = ('status',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'total_marks', 'due_date')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'text', 'correct_option', 'marks')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'attempted_at')


@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'date', 'start_time', 'status')
    list_filter  = ('status', 'course')