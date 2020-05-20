from django.urls import reverse, resolve
from django.test import SimpleTestCase
from student_predictor.views import ShowAllStudentsView,ShowStudentView,PredictStudentView

class TestUrls(SimpleTestCase):
    def test_ShowAllStudentsView(self):
        url = reverse('student_predictor/show_all_students.html')
        self.assertEquals(resolve(url).func, ShowAllStudentsView)

    def test_ShowStudentView(self):
        url = reverse('student_predictor/show_student.html')
        self.assertEquals(resolve(url).func, ShowStudentView)

    def test_PredictStudentView(self):
        url = reverse('student_predictor/predict_student.html')
        self.assertEquals(resolve(url).func, ShowStudentView)
