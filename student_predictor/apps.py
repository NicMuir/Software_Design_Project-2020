from django.apps import AppConfig
import pickle
from sklearn.svm import SVC
import pandas as pd


class StudentPredictorConfig(AppConfig):
    name = 'student_predictor'
    # Load ML model
    filename = "student_predictor/svc_model.pickle"  # TODO
    svc_predictor = pickle.load(open(filename, 'rb'))
