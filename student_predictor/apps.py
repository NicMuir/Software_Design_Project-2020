from django.apps import AppConfig
import pickle
from sklearn.svm import SVC


class StudentPredictorConfig(AppConfig):
    name = 'student_predictor'