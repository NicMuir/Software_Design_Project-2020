from django.urls import reverse, resolve
from django.test import SimpleTestCase
from demo.views import *
from student_predictor.views import *


# StudentPredictor corresponds to app_name = 'student_predictor'
# Class name = app_name value
class TestStudentPredictorUrls(SimpleTestCase):


    def test_show_all_students_url(self):
        response = self.client.get(reverse('student_predictor:show_all_students'))
        self.assertEqual(response.status_code, 302) #302 means redirect to another page
        #return True
        # Do Stuff

    def test_show_all_students_selected_url(self):
        response = self.client.get(reverse('student_predictor:show_all_students_selected',args='1'))
        self.assertEqual(response.status_code, 302)
        #return True
        # Do Stuff

    def test_predict_student_url(self):
        response = self.client.get(reverse('student_predictor:predict_student'))
        self.assertEqual(response.status_code, 302)

        #return True
        # Do Stuff

    def test_re_predict_student_url(self):
        response = self.client.get(reverse('student_predictor:re_predict_student', args='1'))
        self.assertEqual(response.status_code, 302)
        #return True
        # Do Stuff

    def test_predict_multi_student_url(self):
        response = self.client.get(reverse('student_predictor:predict_multi_student'))
        self.assertEqual(response.status_code, 302)
        #return True
        # Do Stuff
        
    # def test_Research_url(self):
    #     return True
    #     # Do Stuff

    def test_Research_url(self):
        response = self.client.get(reverse('student_predictor:Research'))
        self.assertEqual(response.status_code, 200) #directed to actual page


    def test_Statistics_url(self):
        response = self.client.get(reverse('student_predictor:Statistics'))
        self.assertEqual(response.status_code, 200)

    def test_RE_url(self):
        response = self.client.get(reverse('student_predictor:RE'))
        self.assertEqual(response.status_code, 200)

    def test_RE2_url(self):
        response = self.client.get(reverse('student_predictor:RE2'))
        self.assertEqual(response.status_code, 200)

    def test_Manual_url(self):
        response = self.client.get(reverse('student_predictor:Manual'))
        self.assertEqual(response.status_code, 200)


class TestDemoUrls(SimpleTestCase):
    def test_home_url(self):
        response = self.client.get(reverse('demo:home'))
        self.assertEqual(response.status_code, 302)




