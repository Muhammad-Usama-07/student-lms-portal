from django.contrib import admin
from .models import Grade, Notification, Attendance


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display  = ('student', 'course', 'score', 'max_score')
    list_filter   = ('course',)
    search_fields = ('student__username',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display  = ('title', 'notif_type', 'recipient', 'is_read', 'created_at')
    list_filter   = ('notif_type', 'is_read')
    search_fields = ('title', 'message')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display  = ('student', 'course', 'date', 'status')
    list_filter   = ('status', 'course', 'date')
    search_fields = ('student__username',)