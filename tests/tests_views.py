from django.test import SimpleTestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from student_predictor.models import Student
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

    # generic.ListView
    # def TestShowAllStudentsView(self):
    #     self.login_as_superuser()
    #     # Do stuff
    #     return True

    # generic.CreateView
    # def TestPredictStudentView(self):
    #     self.login_as_superuser()
    #     predict_data_dict = dict(
    #         AggregateYOS1=[60.4],
    #         AggregateYOS2=[53.2],
    #         FYComsAvg=[70.5],
    #         SYComsAvg=[67.4],
    #         FYMathAvg=[60.3],
    #         SYMathAvg=[54.3],
    #     )
    #     self.assertDictEqual(self.temp_stud.predict_data(), predict_data_dict)
    #     # Do stuff
    #     return True

    # def TestPredictMultiStudentView(self):
    #     login_as_superuser();
    #     # Do stuff
    #     return True
    #
    # # generic.UpdateView
    # def TestRePredictStudentView(self):
    #     login_as_superuser();
    #     # Do stuff
    #     return True
