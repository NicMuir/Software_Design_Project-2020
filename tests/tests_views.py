from django.test import SimpleTestCase, Client , RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from student_predictor.models import Student
from demo.views import home
from student_predictor.views import *
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.test import Client
import pandas as pd
from student_predictor.models import Student
from django.db.models import Count
import json


class TestViews(TestCase):
    # This method is run before any other tests i.e. sets up whatever is needed for tests
    def setUp(self):
        self.login_as_superuser()  # Need to be logged in

    def login_as_superuser(self):
        # store the password to login later
        password = 'temp_password'
        my_admin = get_user_model().objects.create_superuser('myuser', 'myemail@test.com', password)
        # You'll need to log in before you can send requests through the client
        self.client.login(username=my_admin.username, password=password)

    # check if handle_file successfully adds 5 students
    def test_handle_file(self):
        correct_file = open("test_upload_data/5_students.csv")
        prev_no_students = Student.objects.count()
        PredictMultiStudentView.handle_file(correct_file)
        self.assertEquals(Student.objects.count(), prev_no_students+5)

    # url kwarg with pk of student that exists
    def test_SASV_student_exists_arg(self):
        # create student
        stud_vals = dict(
            student_no=12345,
            first_name="John",
            last_name="Doe",
            # ML Predict Data
            aggregate_YOS1=60.4,
            aggregate_YOS2=53.2,
            coms_avg_YOS1=70.5,
            coms_avg_YOS2=67.4,
            maths_avg_YOS1=60.3,
            maths_avg_YOS2=54.3,
            prediction='H',
        )
        temp_student = Student.objects.create(**stud_vals)
        student_pk = temp_student.pk

        status_code = 200
        view_class = ShowAllStudentsView
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = ShowAllStudentsView.as_view()(req, *[], **{"student_pk": student_pk})  # corresponds to url kwargs for view
        self.assertEqual(resp.status_code, 200)

    # url kwarg with pk of student that does not exist
    def test_SASV_student_does_not_exist_arg(self):
        student_pk = 10000  # student pk that will definitely not exist

        status_code = 200
        view_class = ShowAllStudentsView
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = ShowAllStudentsView.as_view()(req, *[], **{"student_pk": student_pk})  # corresponds to url kwargs for view
        self.assertEqual(resp.status_code, 200)

    def test_SASVget(self):
        status_code = 200
        view_class = ShowAllStudentsView
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = ShowAllStudentsView.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code,200)

    def test_PSVget(self):
        status_code = 200
        view_class = PredictStudentView
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = PredictStudentView.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)

    def test_PMSVget(self):
        status_code = 200
        view_class = PredictMultiStudentView
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = PredictMultiStudentView.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code,200)

    # Test home page view
    def test_demo_view(self):
        url = reverse('demo:home')
        self.assertEquals(resolve(url).func, home)

    def test_chart_data_view(self):
        dataset = Student.objects \
            .values('prediction') \
            .exclude(prediction='') \
            .annotate(total=Count('prediction')) \
            .order_by('prediction')
        preds = dict()
        for pred_tuple in Student.PRED_CHOICES:
            preds[pred_tuple[0]] = pred_tuple[1]

        testchart = {
            'chart': {'type': 'pie'},
            'title': {'text': 'Student Success Predictor'},
            'subtitle': {'text': 'Pie Chart'},
            'tooltip': {
                'pointFormat': '{series.name}: <br>{point.percentage:.1f} %<br>Count: {point.y}'
            },
            'series': [{
                'name': 'Percentage',
                'data': list(map(lambda row: {'name': preds[row['prediction']], 'y': row['total']}, dataset))
            }]
        }

        temp = JsonResponse(testchart)
        output = chart_data()

        if temp == output:
            return True
        else:
            return False

