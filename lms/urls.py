from django.urls import path
from . import views

urlpatterns = [
    # Assignments
    path('assignments/',                    views.assignments_list,        name='assignments_list'),
    path('assignments/create/',             views.assignment_create,       name='assignment_create'),
    path('assignments/<int:pk>/',           views.assignment_detail,       name='assignment_detail'),
    path('assignments/grade/<int:sub_pk>/', views.grade_submission,        name='grade_submission'),
    # Quizzes
    path('quizzes/',                        views.quizzes_list,            name='quizzes_list'),
    path('quizzes/create/',                 views.quiz_create,             name='quiz_create'),
    path('quizzes/<int:pk>/questions/',     views.quiz_add_question,       name='quiz_add_question'),
    path('quizzes/<int:pk>/take/',          views.quiz_take,               name='quiz_take'),
    # Live Classes
    path('live-classes/',                   views.live_classes_list,       name='live_classes_list'),
    path('live-classes/create/',            views.live_class_create,       name='live_class_create'),
    path('live-classes/<int:pk>/status/',   views.live_class_update_status, name='live_class_status'),
]