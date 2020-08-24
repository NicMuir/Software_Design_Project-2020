from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'student_predictor'
urlpatterns = [
    # <int:student_id>
    path('students/', login_required(views.ShowAllStudentsView.as_view()), name='show_all_students'),


    # show all students with specific student to show
    path('<int:student_pk>/', login_required(views.ShowAllStudentsView.as_view()), name='show_all_students_selected'),


    # show_student needs to be removed but first, dependencies need to be fixed
    # path('<int:pk>/', login_required(views.ShowStudentView.as_view()), name='show_student'),
    path('predict', login_required(views.PredictStudentView.as_view()), name='predict_student'),
    path('predict/<int:pk>/', login_required(views.RePredictStudentView.as_view()), name='re_predict_student'),

    # PredictMultiStudentView

    path('multipredict/', login_required(views.PredictMultiStudentView.as_view()), name='predict_multi_student'),
    path('Research' , views.Research , name = 'Research'),
    path('Statistics' , views.Statistics , name = 'Statistics')
]