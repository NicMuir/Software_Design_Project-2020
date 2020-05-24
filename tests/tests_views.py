<<<<<<< HEAD
from django.test import TestCase, Client
from django.urls import reverse
from student_predictor.views import ShowAllStudentsView,ShowStudentView,PredictStudentView,PredictMultiStudentView,RePredictStudentView
#from demo.views

class TestViews(TestCase):

    def get_queryset(self):
        

        self.client.login(username=my_admin.username, password=password)
        return self
=======
from django.test import SimpleTestCase
from django.contrib.auth import get_user_model


class TestStudentPredictorViews(SimpleTestCase):
    # This method is run before any other tests i.e. sets up whatever is needed for tests
    def setUp(self):
        self.login_as_superuser()  # Need to be logged in

    def login_as_superuser(self):
        # store the password to login later
        password = 'temp_password'
        my_admin = get_user_model().objects.create_superuser('myuser', 'myemail@test.com', password)
        # You'll need to log in before you can send requests through the client
        self.client.login(username=my_admin.username, password=password)

    # generic.ListView
    def TestShowAllStudentsView(self):
        # Do stuff
        return True

    # generic.CreateView
    def TestPredictStudentView(self):
        # Do stuff
        return True

    def TestPredictMultiStudentView(self):
        # Do stuff
        return True

    # generic.UpdateView
    def TestRePredictStudentView(self):
        # Do stuff
        return True
>>>>>>> b730a4b0e4eb1e5cd5ff1d04b124cb49a6db953b
