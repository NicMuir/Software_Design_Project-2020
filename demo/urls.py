from django.urls import path
from . import views

app_name = 'demo'
# Create your views here.
urlpatterns = [
    path('', views.home, name='home'),
    #path('',views.PredictStudent,name="Predict Student")
]