import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, Textarea, TextInput, formset_factory, modelformset_factory, BaseModelFormSet, \
    NumberInput
from app.models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'is_staff', 'is_active',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'is_staff', 'is_active',)


class GPAForm(forms.ModelForm):
    class Meta:
        model = GPA
        fields = ('class_name', 'class_grade', 'class_credits')


GPAFormSet = modelformset_factory(GPA, form=GPAForm, extra=4)


class InflationForm(forms.Form):
    today = datetime.date.today()
    year = today.year
    month = today.month

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    month_alt_choices = months[0: month - 2]

    end_month_choices = tuple([(month, month) for month in months])

    year_choice = [(i, i) for i in range(1913, year + 1)]
    start_month_choices = [
        ("January", "January"), ("February", "February"), ("March", "March"),
        ("April", "April"), ("May", "May"),
        ("June", "June"), ("July", "July"), ("August", "August"), ("September", "September"), ("October", "October"),
        ("November", "November"), ("December", "December")
    ]

    start_money = forms.DecimalField(initial=1, label='$', min_value=.01, decimal_places=2, max_digits=18)
    month_start = forms.ChoiceField(choices=end_month_choices, initial="January", label='')
    year_start = forms.TypedChoiceField(choices=year_choice, coerce=int, initial="2000", label='')
    month_end = forms.ChoiceField(choices=start_month_choices, initial="January", label='')
    year_end = forms.TypedChoiceField(choices=year_choice, coerce=int, initial=year - 1, label='')


class LineForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 8, 'cols': 40, 'margin': '0px', 'padding': '0px', 'border': '0px'}
                              ))


class DateForm(forms.Form):
    year = datetime.datetime.now().year
    initial_date = datetime.date(year, 1, 1)
    initial_date_min_one = datetime.date(year - 1, 12, 31)

    date1 = forms.DateField(widget=forms.SelectDateWidget(years=range(1, 2250), attrs={'style': 'width: 10em;'}))
    date2 = forms.DateField(widget=forms.SelectDateWidget(years=range(1, 2250), attrs={'style': 'width: 10em;'}))


class DateForm2(forms.Form):
    math_choices = [('Subtract', 'Subtract'), ('Add', 'Add')]

    math_type = forms.ChoiceField(choices=math_choices)
    date_between = forms.DateField(label='Start Date', initial=datetime.datetime.now(),
                                   widget=forms.SelectDateWidget(years=range(1, 2250), attrs={'style': 'width: 10em;'}))

    day = forms.IntegerField(label='Days', min_value=0, max_value=999999, widget=forms.TextInput(attrs={'style': 'width: 10em;'}))
    month = forms.IntegerField(label='Months', min_value=0, max_value=999999, widget=forms.TextInput(attrs={'style': 'width: 10em;'}))
    year = forms.IntegerField(label='Years', min_value=0, max_value=999999, widget=forms.TextInput(attrs={'style': 'width: 10em;'}))


class TimeForm(forms.Form):
    timefield1 = forms.DateTimeField(widget=forms.SplitDateTimeWidget(attrs={'style': 'width: 10em;'}))
    timefield2 = forms.DateTimeField(widget=forms.SplitDateTimeWidget(attrs={'style': 'width: 10em;'}))
