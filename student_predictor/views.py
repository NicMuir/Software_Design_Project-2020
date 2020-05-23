from django.shortcuts import render, HttpResponse, Http404, get_object_or_404
from .models import *
from .forms import *

from django.urls import reverse
from django.views import generic
from django.urls import resolve
from .apps import StudentPredictorConfig
import pandas as pd


# Create your views here.
# Class based views
# @login_required
class ShowAllStudentsView(generic.ListView):
    template_name = 'student_predictor/show_all_students.html'
    context_object_name = 'alphabetical_students'

    def get_queryset(self):
        # print(self.kwargs["student_pk"])
        return Student.objects.order_by('first_name')

    def get_context_data(self, *, object_list=None, **kwargs):
        # Add new variables to context
        context = super(ShowAllStudentsView, self).get_context_data(**kwargs)

        if "student_pk" in self.kwargs.keys():
            try:
                context['selected_student'] = Student.objects.get(pk=self.kwargs["student_pk"])
            except Student.DoesNotExist:
                print("Student does not exist")
                context['selected_student'] = None
        else:
            print("student_pk was not in kwargs")
            context['selected_student'] = None

        return context


# @login_required
class ShowStudentView(generic.DetailView):
    model = Student
    template_name = "student_predictor/show_student.html"


# @login_required
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

        # prediction = self.svc_predictor.predict(df_data)

        self.object.prediction = StudentPredictorConfig.svc_predictor.predict(stud_data)[0]

        self.object.save()
        return out_response

    def get_context_data(self, **kwargs):
        ctx = super(PredictStudentView, self).get_context_data(**kwargs)
        # Below copy and pasted, need to read up on this
        if self.request.POST:
            ctx['file_upload_form'] = UploadFileForm(self.request.POST)  # Keeps data I think
        else:
            ctx['file_upload_form'] = UploadFileForm()
        return ctx

    def post(self, request, *args, **kwargs):
        out = super().post(self, request, *args, **kwargs)
        # # https://chriskief.com/2012/12/30/django-class-based-views-with-multiple-forms/
        return out


# @login_required
class RePredictStudentView(generic.UpdateView):
    model = Student
    fields = ['student_no', 'first_name', 'last_name', 'aggregate_YOS1', 'aggregate_YOS2',
              'coms_avg_YOS1', 'coms_avg_YOS2', 'maths_avg_YOS1', 'maths_avg_YOS2']
    template_name = "student_predictor/re_predict_student.html"

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



