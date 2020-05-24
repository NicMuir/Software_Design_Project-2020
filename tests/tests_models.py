from django.test import TestCase
from student_predictor.models import Student
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client


class TestStudentModel(TestCase):
    def setUp(self):
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
        self.temp_stud = Student.objects.create(**stud_vals)
        self.client = Client()

    def tearDown(self):
        Student.objects.get(pk=self.temp_stud.pk).delete()
        del self.temp_stud
        del self.client

    def login_as_superuser(self):
        # store the password to login later
        password = 'temp_password'
        my_admin = get_user_model().objects.create_superuser('myuser', 'myemail@test.com', password)
        # You'll need to log in before you can send requests through the client
        self.client.login(username=my_admin.username, password=password)

    def test_predict_data(self):
        predict_data_dict = dict(
            AggregateYOS1=[60.4],
            AggregateYOS2=[53.2],
            FYComsAvg=[70.5],
            SYComsAvg=[67.4],
            FYMathAvg=[60.3],
            SYMathAvg=[54.3],
        )
        self.assertDictEqual(self.temp_stud.predict_data(), predict_data_dict)

    def test_str_(self):
        """Test if string representation of Student model object is correct"""
        self.assertEqual(str(self.temp_stud), 'John Doe(12345)')

    def test_full_name(self):
        self.assertEqual(self.temp_stud.full_name(), "John Doe")

    def test_get_absolute_url(self):
        """Test if url given by student model on update or creation corresponds to a valid page"""
        self.login_as_superuser()
        response = self.client.get(reverse('student_predictor:show_all_students_selected',
                                           kwargs={'student_pk': self.temp_stud.pk}))
        self.assertEqual(response.status_code, 200)

    def test_prediction_text(self):
        self.assertEqual(self.temp_stud.prediction_text(), "High Risk")