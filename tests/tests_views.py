from django.test import TestCase, Client
from django.urls import reverse
from student_predictor.views import ShowAllStudentsView,ShowStudentView,PredictStudentView,PredictMultiStudentView,RePredictStudentView
#from demo.views

class TestViews(TestCase):

    def get_queryset(self):
        

        self.client.login(username=my_admin.username, password=password)
        return self
