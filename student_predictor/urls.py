from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'student_predictor'
urlpatterns = [
    path('', login_required(views.ShowAllStudentsView.as_view()), name='show_all_students'),
    path('<int:pk>/', login_required(views.ShowStudentView.as_view()), name='show_student'),
    path('predict', login_required(views.PredictStudentView.as_view()), name='predict_student'),
]