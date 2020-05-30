# This is for testing the form validator for the FileUpload form
from student_predictor.forms import *
import pandas as pd

from django.test import TestCase


class TestStudentPredictorForms(TestCase):
    # If no ValidationError is raised
    def test_file_validator_correct_format(self):
        correct_file = open("test_upload_data/5_students.csv")
        file_validator(correct_file)

    # If file has wrong cols format
    def test_file_validator_wrong_format_cols(self):
        with self.assertRaises(ValidationError):
            incorrect_file = open("test_upload_data/5_students_wrong_format.csv")
            file_validator(incorrect_file)

    def test_file_validator_not_csv(self):
        with self.assertRaises(ValidationError):
            incorrect_file = open("test_upload_data/textfile.txt")
            file_validator(incorrect_file)

    def test_file_validator_very_wrong(self):
        with self.assertRaises(ValidationError):
            incorrect_file = open("test_upload_data/5_students_very_wrong.csv")
            file_validator(incorrect_file)