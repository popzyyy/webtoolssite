from _decimal import Decimal
from dateutil import relativedelta
from django.shortcuts import render
from django.views.generic import TemplateView
from app.forms import *
from app.models import *
import json
import requests
import datetime
from dateutil.relativedelta import relativedelta


def refresh(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def home(request):
    getipaddress(request)

    return render(request, 'home.html')


def tools(request):
    getipaddress(request)

    return render(request, 'tools.html')


def calculators(request):
    getipaddress(request)

    return render(request, 'calculators.html')


def time(request):
    timeform = TimeForm(request.POST)
    if request.method == "POST":
        if timeform.is_valid():
            date1 = timeform.cleaned_data.get('date1')
            date2 = timeform.cleaned_data.get('date2')

            date_difference = relativedelta(date1, date2)

            date_dif_years = abs(date_difference.years)
            date_dif_months = abs(date_difference.months)
            date_dif_days = abs(date_difference.days)

            return render(request, 'datetime.html',
                          {'timeform': timeform, 'date_dif_months': date_dif_months, 'date_dif_days': date_dif_days,
                           'date_dif_years': date_dif_years})

    else:
        timeform = TimeForm(
            {"date1": datetime.date.today(), "date2": datetime.date.today() - datetime.timedelta(days=364)})

    return render(request, 'datetime.html', {'timeform': timeform})


def date(request):
    dateform = DateForm(request.POST)
    dateform2 = DateForm2(request.POST)

    print(request.POST)

    if request.method == "POST":
        if 'date1_month' in request.POST:
            if dateform.is_valid():
                print('date1')
                date1 = dateform.cleaned_data.get('date1')
                date2 = dateform.cleaned_data.get('date2')

                date_difference = relativedelta(date1, date2)

                date_dif_years = abs(date_difference.years)
                date_dif_months = abs(date_difference.months)
                date_dif_days = abs(date_difference.days)

                dateform = DateForm(
                    {"date_between": datetime.date.today(), "date1": datetime.date.today(),
                     "date2": datetime.date.today() - datetime.timedelta(days=364)})

                dateform2 = DateForm2(
                    {"day": 0, "month": 0, "year": 0, "math_type": "Add", "date_between": datetime.date.today()})

                return render(request, 'time.html',
                              {'dateform': dateform, 'dateform2': dateform2, 'date_dif_months': date_dif_months,
                               'date_dif_days': date_dif_days,
                               'date_dif_years': date_dif_years})

        if 'date_between_month' in request.POST:
            print('date2')
            if dateform2.is_valid():
                math_type = dateform2.cleaned_data.get('math_type')
                date_between = dateform2.cleaned_data.get('date_between')

                math_days = dateform2.cleaned_data.get('day')
                math_months = dateform2.cleaned_data.get('month')
                math_years = dateform2.cleaned_data.get('year')

                orig_days = dateform2.cleaned_data.get('date_between').day
                orig_months = dateform2.cleaned_data.get('date_between').month
                orig_years = dateform2.cleaned_data.get('date_between').year

                if math_type == 'Add':
                    new_date = datetime.date(year=orig_years, month=orig_months, day=orig_days) + relativedelta(
                        days=math_days, months=math_months, years=math_years)
                    new_date = new_date.strftime('%B %d, %Y')
                elif math_type == 'Subtract':
                    new_date = datetime.date(year=orig_years, month=orig_months, day=orig_days) - relativedelta(
                        days=math_days, months=math_months, years=math_years)
                    new_date = new_date.strftime('%B %d, %Y')



                dateform = DateForm(
                    {"date_between": datetime.date.today(), "date1": datetime.date.today(),
                     "date2": datetime.date.today() - datetime.timedelta(days=364)})

                dateform2 = DateForm2(
                    {"day": 0, "month": 0, "year": 0, "math_type": "Add", "date_between": datetime.date.today()})

                return render(request, 'time.html',
                              {'new_date': new_date, 'dateform2': dateform2, 'dateform': dateform, 'math_type': math_type,
                               'date_between': date_between})



    else:
        dateform = DateForm(
            {"date_between": datetime.date.today(), "date1": datetime.date.today(),
             "date2": datetime.date.today() - datetime.timedelta(days=364)})

        dateform2 = DateForm2(
            {"day": 0, "month": 0, "year": 0, "math_type": "Add", "date_between": datetime.date.today()})

    return render(request, 'time.html', {'dateform': dateform, 'dateform2': dateform2})


def line(request):
    getipaddress(request)
    global text_sessions

    if request.method == "POST":
        lineform = LineForm(request.POST)
        if lineform.is_valid():
            text = lineform.cleaned_data.get('text')

            new_text = []

            for i in text:
                if i != "\n" and i != "\r":
                    new_text.append(i)

            joined_text = "".join(new_text)

            lineform = LineForm({"text": joined_text})

            return render(request, 'line.html', {'lineform': lineform})


    else:
        lineform = LineForm()

    return render(request, 'line.html', {'lineform': lineform})


def inflation(request):
    getipaddress(request)
    data = Inflation.objects.all().order_by('-year', '-month_code')
    today = datetime.date.today()
    year_math = today - datetime.timedelta(weeks=12)

    month_dict = [
        '01', '02', '03', '04', '05', '06',
        '07', '08', '09', '10', '11', '12'
    ]
    if not Inflation.objects.filter(year=year_math.year, month_code="M" + str(month_dict[today.month - 3])).exists():
        try:
            headers = {'Content-type': 'application/json'}
            # data = json.dumps({"seriesid": ['CUUR0000SA0'], "startyear": str(2022), "endyear": str(2023)})
            data = json.dumps(
                {"seriesid": ['CUUR0000SA0'], "startyear": str(today.year - 9), "endyear": str(today.year)})
            p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
            json_data = json.loads(p.text)
            print(json_data)

            if 'series' in json_data.get('Results', {}):
                for series in json_data['Results']['series']:
                    for item in series['data']:
                        year = item['year']
                        month_code = item['period']
                        month = item['periodName']
                        value = item['value']
                        inflation_data = Inflation(year=year, month_code=month_code, month=month, inflation_rate=value)

                        if not Inflation.objects.filter(year=year, month_code=month_code).exists():
                            inflation_data.save()
        except:
            pass

            month_dict = [
                '01', '02', '03', '04', '05', '06',
                '07', '08', '09', '10', '11', '12'
            ]

            year = today.year

            counter1 = 0
            for total_years in Inflation.objects.all():
                for month_code in month_dict:
                    try:
                        object1 = Inflation.objects.get(year=str(year - counter1), month_code='M' + str(month_code))
                        object2 = Inflation.objects.get(year=str(1913), month_code='M01')

                        percent_change_all = (((float(object1.inflation_rate) - float(object2.inflation_rate)) / float(
                            object2.inflation_rate)) * 100)

                        object1.percent_change_all = percent_change_all
                        object1.save()
                    except:
                        pass

                counter1 += 1

            counter = 0
            for total_years in Inflation.objects.filter(year__range=(1914, year)).values('year').distinct():
                for month_code in month_dict:
                    try:
                        object1 = Inflation.objects.get(year=str(year - counter), month_code='M' + str(month_code))
                        object2 = Inflation.objects.get(year=str(year - (counter + 1)),
                                                        month_code='M' + str(month_code))

                        percent_change = (((float(object1.inflation_rate) - float(object2.inflation_rate)) / float(
                            object2.inflation_rate)) * 100)

                        object1.percent_change = percent_change
                        object1.save()
                    except:
                        pass

                counter += 1

            for target_year in range(1913, int(year) + 1):
                for count in range(len(month_dict)):
                    current_month_code = "M" + str(month_dict[count])
                    previous_month_code = "M" + str(month_dict[count - 1]) if count > 0 else "M12"  # Handle December
                    # trash code and digital duct tape
                    try:
                        object1 = Inflation.objects.get(year=str(target_year), month_code=current_month_code)
                        object2 = Inflation.objects.get(year=str(target_year - 1 if count == 0 else target_year),
                                                        month_code=previous_month_code)

                        percent_change_mom = ((float(object1.inflation_rate) - float(object2.inflation_rate))
                                              / float(object2.inflation_rate)) * 100

                        object1.percent_change_mom = percent_change_mom
                        object1.save()

                    except:
                        pass
        inflationform = InflationForm()
        return render(request, "inflation.html", {'data': data, 'inflationform': inflationform})

    if request.method == "POST":
        inflationform = InflationForm(request.POST)
        if inflationform.is_valid():

            month_start = inflationform.cleaned_data.get('month_start')
            year_start = inflationform.cleaned_data.get('year_start')
            month_end = inflationform.cleaned_data.get('month_end')
            year_end = inflationform.cleaned_data.get('year_end')
            start_money = inflationform.cleaned_data.get('start_money')

            today = datetime.date.today()
            year = today.year
            month = today.month

            # month_dict = {month: index for index, month in enumerate(calendar.month_name) if month}

            if not Inflation.objects.filter(month=month_end, year=year_end).exists() or not Inflation.objects.filter(
                    month=month_start, year=year_start).exists():
                inflationform.add_error('year_end', "A date is in the future or CPI data not available.")

            if inflationform.errors:
                return render(request, "inflation.html",
                              {'data': data, 'inflationform': inflationform})

            inflation_rate_end = Inflation.objects.get(year=str(year_end), month=month_end)
            inflation_rate_start = Inflation.objects.get(year=str(year_start), month=month_start)

            end_muney = (Decimal(inflation_rate_end.inflation_rate) / Decimal(
                inflation_rate_start.inflation_rate)) * Decimal(start_money)

            return render(request, "inflation.html",
                          {'data': data, 'inflationform': inflationform, 'end_muney': end_muney})

    inflationform = InflationForm()
    return render(request, "inflation.html",
                  {'data': data, 'inflationform': inflationform})


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
