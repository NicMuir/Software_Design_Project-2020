from django.urls import reverse, resolve
from django.test import SimpleTestCase
from student_predictor.views import *


# StudentPredictor corresponds to app_name = 'student_predictor'
# Class name = app_name value
class TestStudentPredictorUrls(SimpleTestCase):
    # method name = name of url
    def test_show_all_students_url(self):
        return True
        # Do Stuff

    def test_show_all_students_selected_url(self):
        return True
        # Do Stuff

    def test_predict_student_url(self):
        return True
        # Do Stuff

    def test_re_predict_student_url(self):
        return True
        # Do Stuff

    def test_predict_multi_student_url(self):
        return True
        # Do Stuff

    def test_Research_url(self):
        return True
        # Do Stuff
    def test_Statistics_url(self):
        return True
        # Do Stuff

class TestDemoUrls(SimpleTestCase):
    def test_home_url(self):
        return True
        # Do Stuff

