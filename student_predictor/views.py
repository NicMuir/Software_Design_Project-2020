from django.shortcuts import render, HttpResponse, Http404, get_object_or_404
from .models import *
from .forms import *

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy, resolve
from django.views import generic

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
    template_name = "student_predictor/predict_student.html"

    # If student model is created successfully run following code to add predicted data
    def form_valid(self, form):
        out_response = super().form_valid(form)
        # Do stuff here
        data_dict = self.object.predict_data()
        stud_data = pd.DataFrame.from_dict(data_dict)

        self.object.prediction = StudentPredictorConfig.svc_predictor.predict(stud_data)[0]

        self.object.save()
        return out_response
