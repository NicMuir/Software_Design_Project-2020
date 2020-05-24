from django.test import SimpleTestCase, Client , RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from student_predictor.models import Student
from student_predictor.views import ShowAllStudentsView , PredictStudentView , PredictMultiStudentView , RePredictStudentView
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client


class TestShowAllStudentsView(TestCase):
    # This method is run before any other tests i.e. sets up whatever is needed for tests
    def setUp(self):
        self.login_as_superuser()  # Need to be logged in

    def login_as_superuser(self):
        # store the password to login later
        password = 'temp_password'
        my_admin = get_user_model().objects.create_superuser('myuser', 'myemail@test.com', password)
        # You'll need to log in before you can send requests through the client
        self.client.login(username=my_admin.username, password=password)

    def test_SASVget(self):
        status_code = 200
        view_class = ShowAllStudentsView
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = ShowAllStudentsView.as_view() (req , *[],**{})
        self.assertEqual(resp.status_code,200)

    def test_PSVget(self):
        status_code = 200
        view_class = PredictStudentView
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = PredictStudentView.as_view() (req , *[],**{})
        self.assertEqual(resp.status_code,200)

    def test_PMSVget(self):
        status_code = 200
        view_class = PredictMultiStudentView
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = PredictMultiStudentView.as_view() (req , *[],**{})
        self.assertEqual(resp.status_code,200)

    # def test_RPSVget(self):
    #     status_code = 200
    #     view_class = RePredictStudentView
    #     req = RequestFactory().get('/')
    #     req.user = AnonymousUser()
    #     resp = RePredictStudentView.as_view() (req , *[],**{})
    #     self.assertEqual(resp.status_code,200)

    # generic.ListView
    # def TestShowAllStudentsView(self):
    #
    #     url = reverse("student_predictor.views.ShowAllStudentsView")
    #     resp = self.client.get(url)
    #     self.assertEqual(resp.status_code, 200)
    #     # Do stuff

    # generic.CreateView
    # def TestPredictStudentView(self):
    #
    #
    #     # Do stuff
    #     return True

    # def TestPredictMultiStudentView(self):
    #
    #     # Do stuff
    #     return True
    #
    # # generic.UpdateView
    # def TestRePredictStudentView(self):
    #
    #     # Do stuff
    #     return True
