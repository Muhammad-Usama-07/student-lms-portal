from django.db import models
from django.conf import settings
from lms.models import Course


class Grade(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='grades', limit_choices_to={'role': 'student'})
    course  = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    score   = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    remarks = models.CharField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-score']

    def grade_badge(self):
        ratio = float(self.score) / float(self.max_score)
        if ratio >= 0.7:
            return 'good'
        elif ratio >= 0.5:
            return 'average'
        return 'low'

    def __str__(self):
        return f"{self.student.username} | {self.course.code} | {self.score}"


class Notification(models.Model):
    TYPE_CHOICES = (
        ('info',    'Info'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('danger',  'Danger'),
    )
    recipient   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='notifications', null=True, blank=True,
                                    help_text='Leave blank to send to all students')
    title       = models.CharField(max_length=255)
    message     = models.TextField()
    notif_type  = models.CharField(max_length=10, choices=TYPE_CHOICES, default='info')
    is_read     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='notifications_sent', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent',  'Absent'),
        ('late',    'Late'),
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='attendance', limit_choices_to={'role': 'student'})
    course  = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance')
    date    = models.DateField()
    status  = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')

    class Meta:
        unique_together = ('student', 'course', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.username} | {self.course.code} | {self.date} | {self.status}"