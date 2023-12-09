from _decimal import Decimal
from django.core.exceptions import ValidationError
from django.forms import formset_factory, BaseFormSet, modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.views.generic import TemplateView

from .forms import GPAFormSet
from app.models import *


def refresh(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def home(request):
    getipaddress(request)

    return render(request, 'home.html')

def tools(request):
    getipaddress(request)

    return render(request, 'tools.html')



class GPACalc(TemplateView):
    template_name = "gpacalculator.html"

    def get(self, *args, **kwargs):
        # Use the correct key for the formset in the context
        formset = GPAFormSet(queryset=GPA.objects.none())
        return self.render_to_response({'formset': formset})

    def post(self, *args, **kwargs):
        formset = GPAFormSet(data=self.request.POST)

        if formset.is_valid():
            instances = formset.save(commit=False)
            print(formset.cleaned_data)

            total_credits = []
            total_gpa_points = []

            grade_to_gpa = {
                "A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0,
                "B-": 2.7, "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3,
                "D": 1.0, "D-": 0.7, "F": 0.0
            }

            for instance in instances:
                class_grade = instance.class_grade
                raw_gpa = grade_to_gpa.get(class_grade)
                total_gpa_points.append(raw_gpa*instance.class_credits)
                total_credits.append(instance.class_credits)

                instance.save()

            cumulative_weighted_gpa = sum(total_gpa_points) / sum(total_credits)

            # Use the correct key for rendering the formset in the context
            return render(self.request, "gpacalculator.html", {'formset': formset, 'cum_gpa': cumulative_weighted_gpa})

        # Use the correct key for rendering the formset in the context
        return self.render_to_response({'formset': formset})






def getipaddress(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        exists = Visitor.objects.filter(ipaddress=ip).exists()
        if not exists:
            bruh = Visitor(ipaddress=ip)
            bruh.save()
    except:
        pass
