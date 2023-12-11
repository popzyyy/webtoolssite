import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, Textarea, TextInput, formset_factory, modelformset_factory, BaseModelFormSet
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

from django import forms
import datetime
import calendar


class InflationForm(forms.Form):
    today = datetime.date.today()
    year = today.year
    month = today.month

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    month_alt_choices = months[0:month - 2]

    end_month_choices_raw = [(month, month) for month in month_alt_choices]
    end_month_choices = tuple(end_month_choices_raw)



    year_choice = [(i, i) for i in range(1913, year + 1)]
    start_month_choices = [
        ("January", "January"), ("February", "February"), ("March", "March"),
        ("April", "April"), ("May", "May"),
        ("June", "June"), ("July", "July"), ("August", "August"), ("September", "September"), ("October", "October"),
        ("November", "November"), ("December", "December")
    ]

    start_money = forms.FloatField(initial=1, label="$USD", min_value=0.01, max_value=999999)
    month_start = forms.ChoiceField(choices=end_month_choices, initial="January", label="Start Month")
    year_start = forms.TypedChoiceField(choices=year_choice, coerce=int, initial="2000", label="Start Year")
    # end_money = forms.FloatField(initial=1, label="$USD", min_value=0, max_value=999999)
    month_end = forms.ChoiceField(choices=start_month_choices, initial="January", label="End Month")
    year_end = forms.TypedChoiceField(choices=year_choice, coerce=int, initial=year, label="End Year")
