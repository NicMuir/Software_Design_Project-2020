from django.urls import path

from . import views

app_name = 'student_predictor'
urlpatterns = [
    path('', views.ShowStudentView.as_view(), name='show_student' ),
    path('<int:pk>/', views.ShowAllStudentsView.as_view(), name='show_all_students' ),
]