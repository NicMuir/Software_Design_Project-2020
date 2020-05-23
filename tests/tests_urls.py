from django.urls import reverse, resolve
from django.test import SimpleTestCase


# StudentPredictor corresponds to app_name = 'student_predictor'
# Class name = app_name value
class TestStudentPredictorUrls(SimpleTestCase):
    # method name = name of url
    def test_show_all_students_url(self):
        return True
        # Do Stuff

    def test_show_student_url(self):
        return True
        # Do Stuff

    def test_predict_student_url(self):
        return True
        # Do Stuff


class TestDemoUrls(SimpleTestCase):
    def test_home_url(self):
        return True
        # Do Stuff

