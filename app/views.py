from _decimal import Decimal
from django.core.exceptions import ValidationError
from django.forms import formset_factory, BaseFormSet, modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.views.generic import TemplateView
from app.validators import *
from app.forms import GPAFormSet, InflationForm
from app.models import *
import json
import requests
import datetime


def refresh(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def home(request):
    getipaddress(request)

    return render(request, 'home.html')


def tools(request):
    getipaddress(request)

    return render(request, 'tools.html')


def inflation(request):
    getipaddress(request)
    today = datetime.date.today()
    data = Inflation.objects.all().order_by('-year', '-month_code')

    if not Inflation.objects.filter(year=today.year, month_code="M" + str(today.month - 2)).exists():
        headers = {'Content-type': 'application/json'}
        data = json.dumps({"seriesid": ['CUUR0000SA0'], "startyear": str(today.year - 9), "endyear": str(today.year)})
        p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
        json_data = json.loads(p.text)
        print(json_data)

        if 'series' in json_data.get('Results', {}):
            for series in json_data['Results']['series']:
                # x = prettytable.PrettyTable(["seriesID", "year", "period", "value"])

                # seriesId = series['seriesID']
                for item in series['data']:
                    year = item['year']
                    month_code = item['period']
                    month = item['periodName']
                    value = item['value']
                    inflation_data = Inflation(year=year, month_code=month_code, month=month, inflation_rate=value)

                    if not Inflation.objects.filter(year=year, month_code=month_code).exists():
                        inflation_data.save()

                    # if 'M01' <= month <= 'M12':
                    #      x.add_row([seriesId, year, month, value])

        return render(request, "inflation.html", {'data': data})

    if request.method == "POST":
        form = InflationForm(request.POST)
        if form.is_valid():
            print('test')

            month_start = form.cleaned_data.get('month_start')
            year_start = form.cleaned_data.get('year_start')
            month_end = form.cleaned_data.get('month_end')
            year_end = form.cleaned_data.get('year_end')

            start_money = form.cleaned_data.get('start_money')

            inflation_rate_end = Inflation.objects.get(year=year_end, month=month_end)
            inflation_rate_start = Inflation.objects.get(year=year_start, month=month_start)
            print(inflation_rate_end.inflation_rate)
            print(inflation_rate_start.inflation_rate)

            end_muney = (float(inflation_rate_end.inflation_rate) / float(
                inflation_rate_start.inflation_rate)) * start_money
            print(end_muney)

            return render(request, "inflation.html", {'data': data, 'formset': form, 'end_muney': end_muney})

    formset = InflationForm()
    return render(request, "inflation.html", {'data': data, 'formset': formset})


class GPACalc(TemplateView):
    template_name = "gpacalculator.html"

    def get(self, *args, **kwargs):
        formset = GPAFormSet(queryset=GPA.objects.none())
        return self.render_to_response({'formset': formset})

    def post(self, *args, **kwargs):
        formset = GPAFormSet(data=self.request.POST)

        if formset.is_valid():
            total_credits = []
            total_gpa_points = []

            grade_to_gpa = {
                "A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0,
                "B-": 2.7, "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3,
                "D": 1.0, "D-": 0.7, "F": 0.0
            }

            for form in formset:
                if form.is_valid():
                    class_grade = form.cleaned_data.get('class_grade')
                    class_credits = form.cleaned_data.get('class_credits')

                    if not class_grade or not class_credits:
                        form.add_error(None, "Fill out both class grade and credits.")
                        continue

                    raw_gpa = grade_to_gpa.get(class_grade)
                    total_gpa_points.append(raw_gpa * class_credits)
                    total_credits.append(class_credits)

                    form.save()

            if total_credits:
                cumulative_weighted_gpa = sum(total_gpa_points) / sum(total_credits)
            else:
                cumulative_weighted_gpa = 0.0

            return render(self.request, "gpacalculator.html",
                          {'formset': formset, 'cum_gpa': cumulative_weighted_gpa})

        return self.render_to_response({'formset': formset})


def getipaddress(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if not Visitor.objects.filter(ipaddress=ip).exists():
            bruh = Visitor(ipaddress=ip)
            bruh.save()
    except:
        pass


def YearUpdate():
    today = datetime.date.today()
    if not Year.objects.filter(year=today.year).exists():
        year = Year(year=today.year)
        year.save()
