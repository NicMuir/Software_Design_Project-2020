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
    path('predict_lgr', login_required(views.PredictStudentViewLGR.as_view()), name='predict_student_lgr'),
    path('predict/<int:pk>/', login_required(views.RePredictStudentView.as_view()), name='re_predict_student'),
    path('predict_lgr/<int:pk>/', login_required(views.RePredictStudentViewLGR.as_view()), name='re_predict_student_lgr'),

    # PredictMultiStudentView

    path('multipredict/', login_required(views.PredictMultiStudentView.as_view()), name='predict_multi_student'),
    path('multipredict/multipredict_lgr/', login_required(views.PredictMultiStudentViewLGR.as_view()), name='predict_multi_student_lgr'),
    path('Research' , views.Research , name = 'Research'),
    path('ResearchExplained' , views.RE , name = 'RE'),
    path('Statistics' , views.Statistics , name = 'Statistics'),
    path('Manual' , views.Manual , name = 'Manual'),
    path('p_chart', views.chart_data, name='p'),
    path('b_chart', views.bar_chart, name='b'),
    path('b_chart2', views.bar_chart2, name='b2')
]
