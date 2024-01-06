from django.conf.urls.static import static
from django.urls import path, include

from debtwebsite import settings
from . import views
from .views import *

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('gpacalculator/', GPACalc.as_view(), name='gpacalc'),
    path('gpacalculator/<int:pk>/', GPACalc.as_view(), name='gpacalc'),
    path('refresh/', views.refresh, name='refresh'),
    path('tools/', views.tools, name='tools'),
    path('inflationcalculator/', views.inflation, name='inflation'),
    path('calculators/', views.calculators, name='calculators'),
    path('onelinemaker/', views.line, name='line'),
    path('datecalculation/', views.date, name='date'),
    path('timecalculation/', views.time, name='time'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
