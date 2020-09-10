from django.apps import AppConfig
import pickle
from sklearn.svm import SVC
import pandas as pd


class StudentPredictorConfig(AppConfig):
    name = 'student_predictor'
    # Load ML model
    filename = "student_predictor/svc_model.pickle"
    svc_predictor = pickle.load(open(filename, 'rb'))

    #filenameLGR = "student_predictor/lgr_model.pickle"
    #lgr_predictor = pickle.load(open(filenameLGR, 'rb'))
