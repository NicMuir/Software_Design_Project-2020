from django.shortcuts import render, HttpResponse, Http404, get_object_or_404
from .models import *
from django.urls import reverse
from django.views import generic

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


# Old way of doing this
# def show_all_students(request):
#     alphabetical_students = Student.objects.order_by('first_name')
#     context = {'alphabetical_students': alphabetical_students}
#     return render(request, 'student_predictor/show_all_students.html', context)
#
#
# def show_student(request, student_no):
#     # If student does not exist site will be taken to 404 page
#     student = get_object_or_404(Student, student_no=student_no)
#     return render(request, 'student_predictor/show_student.html', {'student': student})
