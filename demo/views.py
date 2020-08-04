from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    # return HttpResponse("Hello you are at home")
    return render(request, 'demo/home.html')

