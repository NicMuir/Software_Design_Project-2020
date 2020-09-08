from django.shortcuts import render, HttpResponse, Http404, get_object_or_404
from .models import *
from .forms import *

import json

from django.db.models import Count, Q
from django.shortcuts import render
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy, resolve
from django.views import generic

from .apps import StudentPredictorConfig
import pandas as pd
from django.core import serializers


# Create your views here.
# Class based views
# @login_required


class ShowAllStudentsView(generic.ListView):
    template_name = 'student_predictor/show_all_students.html'
    context_object_name = 'alphabetical_students'

    def get_queryset(self):
        #print(self.kwargs["student_pk"])
        return Student.objects.order_by('first_name')

    def get_context_data(self, *, object_list=None, **kwargs):
        # Add new variables to context
        context = super(ShowAllStudentsView, self).get_context_data(**kwargs)

        if "student_pk" in self.kwargs.keys():
            try:
                selected_student = Student.objects.get(pk=self.kwargs["student_pk"])
                context['selected_student'] = selected_student
                context['selected_student_no'] = selected_student.student_no
            except Student.DoesNotExist:
                print("Student does not exist")
                context['selected_student'] = None
                context['selected_student_no'] = None
        else:
            print("student_pk was not in kwargs")
            context['selected_student'] = None
            context['selected_student_no'] = None

        return context


# # @login_required
# class ShowStudentView(generic.DetailView):
#     model = Student
#     template_name = "student_predictor/show_student.html"


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


# TODO - TEST (No idea if this will work)
class PredictMultiStudentView(generic.FormView):
    template_name = 'student_predictor/predict_multi_student.html'
    success_url = reverse_lazy('student_predictor:show_all_students')
    form_class = UploadFileForm

    @staticmethod
    def handle_file(file):
        # # seek ensures pointer is at start of file (this may not be the case due to other processes using this file)
        # file.seek(0)

        df = pd.read_csv(file)

        # create and predict student via data given in row of dataframe
        def predict_and_save(row):
            row_dict = row.to_dict()

            # row_dict should be of right format as this should be validated in form
            # if student with given student number exists simply update the values rather than create new instance
            temp_student, created = Student.objects.update_or_create(student_no=row_dict['student_no'], defaults=row_dict)

            data_dict = temp_student.predict_data()
            stud_data = pd.DataFrame.from_dict(data_dict)

            temp_student.prediction = StudentPredictorConfig.svc_predictor.predict(stud_data)[0]
            temp_student.save()

        for i in range(0, df.shape[0]):
            row = df.iloc[i]
            predict_and_save(row)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            self.handle_file(file=request.FILES['file'])  # error handling will be done in form validator
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


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

        self.object.prediction = StudentPredictorConfig.svc_predictor.predict(stud_data)[0]

        self.object.save()
        return out_response

def Research(request):
    return render(request,'student_predictor/Research.html')

def Statistics(request):
    return render(request,'student_predictor/Statistics.html')

def Test(request):
    return render(request,'student_predictor/Test.html')

from highcharts.views import (HighChartsMultiAxesView, HighChartsPieView,
                              HighChartsSpeedometerView, HighChartsHeatMapView, HighChartsPolarView)


def chart_data(request):
    dataset = Student.objects \
        .values('prediction') \
        .exclude(prediction='') \
        .annotate(total=Count('prediction')) \
        .order_by('prediction')

    preds = dict()
    for pred_tuple in Student.PRED_CHOICES:
        preds[pred_tuple[0]] = pred_tuple[1]

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Student Success Predictor'},
        'subtitle':{'text':'Pie Chart'},
        'tooltip': {
      'pointFormat': '{series.name}: <br>{point.percentage:.1f} %<br>Count: {point.y}'
      },
        'series': [{
            'name': 'Percentage',
            'data': list(map(lambda row: {'name': preds[row['prediction']], 'y': row['total']}, dataset))
        }]
    }
    return JsonResponse(chart)


def bar_chart(request):
    dataset = Student.objects \
        .values('prediction') \
        .annotate(high_count=Count('prediction', filter=Q(prediction= 'H')),
                  low_count=Count('prediction', filter=Q(prediction='L')),
                  medium_count=Count('prediction', filter=Q(prediction= 'M'))) \
        .order_by('prediction')


    categories = list()
    high_risk_series_data = list()
    medium_risk_series_data = list()
    low_risk_series_data = list()

    for entry in dataset:
        categories.append('%s prediction' % entry['prediction'])
        high_risk_series_data.append(entry['high_count'])
        low_risk_series_data.append(entry['low_count'])
        medium_risk_series_data.append(entry['medium_count'])

    high_risk_series = {
        'name': 'High Risk',
        'data': high_risk_series_data,
        'color': 'orange'
    }

    low_risk_series = {
        'name': 'Low Risk',
        'data': low_risk_series_data,
        'color': 'blue'
    }

    medium_risk_series = {
        'name': 'Medium Risk',
        'data': medium_risk_series_data,
        'color': 'red'
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Student Success Predictor','x':12},
        'subtitle':{'text':'Bar Chart'},
        'xAxis': {'categories': ['High Risk','Low Risk','Medium Risk']},
        'series': [high_risk_series,low_risk_series, medium_risk_series]
    }

    dump = json.dumps(chart)

    return render(request, 'student_predictor/Statistics.html', {'chart': dump})

def heat_chart(request):

    chart = {
        'chart': {'type': 'heatmap'},
        'title': {'text': 'Student Success Predictor'},
        'subtitle':{'text':'Heatmap Chart'},
        'xAxis': {'categories': ['Alexander', 'Marie', 'Maximilian', 'Sophia', 'Lukas',
         'Maria', 'Leon', 'Anna', 'Tim', 'Laura']},
        'yAxis': {'categories': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']},
        'colorAxis' :{
                       'min': 0,
                       'minColor': '#FFFFFF'

                   },
         'legend' : {
              'align': 'right',
              'layout': 'vertical',
              'margin': 0,
              'verticalAlign': 'top',
              'y': 25,
              'symbolHeight': 280
           },
            'series' : [{
                   'name': 'Sales per employee',
                   'borderWidth': 1,
                   'data': [[0, 0, 10], [0, 1, 19], [0, 2, 8], [0, 3, 24], [0, 4, 67],
                      [1, 0, 92], [1, 1, 58], [1, 2, 78], [1, 3, 117], [1, 4, 48],
                      [2, 0, 35], [2, 1, 15], [2, 2, 123], [2, 3, 64], [2, 4, 52],
                      [3, 0, 72], [3, 1, 132], [3, 2, 114], [3, 3, 19], [3, 4, 16],
                      [4, 0, 38], [4, 1, 5], [4, 2, 8], [4, 3, 117], [4, 4, 115],
                      [5, 0, 88], [5, 1, 32], [5, 2, 12], [5, 3, 6], [5, 4, 120],
                      [6, 0, 13], [6, 1, 44], [6, 2, 88], [6, 3, 98], [6, 4, 96],
                      [7, 0, 31], [7, 1, 1], [7, 2, 82], [7, 3, 32], [7, 4, 30],
                      [8, 0, 85], [8, 1, 97], [8, 2, 123], [8, 3, 64], [8, 4, 84],
                      [9, 0, 47], [9, 1, 114], [9, 2, 31], [9, 3, 48], [9, 4, 91]],
                   'dataLabels': {
                      'enabled': 'true',
                      'color': '#000000'
                   }
                }]
            }

    dump = json.dumps(chart)

    return render(request, 'student_predictor/Statistics.html', {'chart': dump})
