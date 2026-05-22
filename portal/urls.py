from django.urls import path
from . import views

urlpatterns = [
    path('',              views.dashboard,          name='dashboard'),
    path('grades/',       views.grades_view,         name='grades'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('attendance/',   views.attendance_view,     name='attendance'),
]