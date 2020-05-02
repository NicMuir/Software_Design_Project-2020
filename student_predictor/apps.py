from django.apps import AppConfig
import pickle
from sklearn.svm import SVC
import pandas as pd


class StudentPredictorConfig(AppConfig):
    name = 'student_predictor'
    # Load ML model
    filename = "student_predictor/svc_model.pickle"  # TODO
    svc_predictor = pickle.load(open(filename, 'rb'))

    # TODO
    # def predict_student(self, student):
    #     data_dict = student.predict_data()
    #     df_data = pd.DataFrame.from_dict(data_dict)
    #
    #     # TODO - Test
    #     prediction = self.svc_predictor.predict(df_data)
    #     return prediction
