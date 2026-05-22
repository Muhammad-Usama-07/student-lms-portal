from django.db import models
from django.conf import settings


class Course(models.Model):
    name    = models.CharField(max_length=200)
    code    = models.CharField(max_length=20, unique=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='courses_taught', limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                      related_name='enrolled_courses', limit_choices_to={'role': 'student'})
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


# ── ASSIGNMENTS ──────────────────────────────────────────────────────────────
class Assignment(models.Model):
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title       = models.CharField(max_length=255)
    description = models.TextField()
    due_date    = models.DateTimeField()
    total_marks = models.PositiveIntegerField(default=100)
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='assignments_created')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.code})"

    class Meta:
        ordering = ['-due_date']


class Submission(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('graded',    'Graded'),
        ('late',      'Late'),
    )
    assignment   = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='submissions')
    file         = models.FileField(upload_to='submissions/', blank=True, null=True)
    text_answer  = models.TextField(blank=True)
    marks_obtained = models.PositiveIntegerField(blank=True, null=True)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    feedback     = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.username} → {self.assignment.title}"


# ── QUIZZES ───────────────────────────────────────────────────────────────────
class Quiz(models.Model):
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    total_marks = models.PositiveIntegerField(default=10)
    time_limit  = models.PositiveIntegerField(default=30, help_text='Minutes')
    due_date    = models.DateTimeField()
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='quizzes_created')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.code})"

    class Meta:
        ordering = ['-due_date']
        verbose_name_plural = 'Quizzes'


class Question(models.Model):
    quiz          = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text          = models.TextField()
    option_a      = models.CharField(max_length=300)
    option_b      = models.CharField(max_length=300)
    option_c      = models.CharField(max_length=300)
    option_d      = models.CharField(max_length=300)
    correct_option = models.CharField(max_length=1, choices=(
        ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')
    ))
    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Q: {self.text[:60]}"


class QuizAttempt(models.Model):
    quiz       = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='quiz_attempts')
    score      = models.PositiveIntegerField(default=0)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'student')

    def __str__(self):
        return f"{self.student.username} → {self.quiz.title} ({self.score})"


# ── LIVE CLASSES ──────────────────────────────────────────────────────────────
class LiveClass(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('live',      'Live Now'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='live_classes')
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date        = models.DateField()
    start_time  = models.TimeField()
    end_time    = models.TimeField()
    meet_link   = models.URLField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='live_classes_created')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.date}"

    class Meta:
        ordering = ['date', 'start_time']