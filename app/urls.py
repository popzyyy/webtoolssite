from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('gpacalc/', GPACalc.as_view(), name='gpacalc'),
    path('gpacalc/<int:pk>/', GPACalc.as_view(), name='gpacalc'),
    path('refresh/', views.refresh, name='refresh'),
    path('tools/', views.tools, name='tools'),
    path('inflation/', views.inflation, name='inflation'),



]