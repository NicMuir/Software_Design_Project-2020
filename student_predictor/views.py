from django.shortcuts import render, HttpResponse, Http404, get_object_or_404
from .models import *
from django.urls import reverse
from django.views import generic
from django.urls import resolve
from .apps import StudentPredictorConfig
import pandas as pd

# Create your views here.
# Class based views
class ShowAllStudentsView(generic.ListView):
    template_name = 'student_predictor/show_all_students.html'
    context_object_name = 'alphabetical_students'

    def get_queryset(self):
        return Student.objects.order_by('first_name')


class ShowStudentView(generic.DetailView):
    model = Student
    template_name = "student_predictor/show_student.html"


class PredictStudentView(generic.CreateView):
    model = Student
    fields = ['student_no','first_name', 'last_name', 'aggregate_YOS1', 'aggregate_YOS2',
              'coms_avg_YOS1', 'coms_avg_YOS2', 'maths_avg_YOS1', 'maths_avg_YOS2']
    template_name = "student_predictor/predict_student.html"

    # If student model is created successfully run following code to add predicted data
    def form_valid(self, form):
        out_response = super().form_valid(form)
        # Do stuff here
        data_dict = self.object.predict_data()
        stud_data = pd.DataFrame.from_dict(data_dict)

        # TODO - Test
        # prediction = self.svc_predictor.predict(df_data)

        self.object.prediction = StudentPredictorConfig.svc_predictor.predict(stud_data)[0]

        self.object.save()
        return out_response

