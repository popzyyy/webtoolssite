from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, Textarea, TextInput, formset_factory, modelformset_factory
from app.models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'is_staff', 'is_active',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'is_staff', 'is_active',)


'''
class GPAForm(forms.ModelForm):


    class_name = forms.CharField(label='Class Name', max_length=20, required=False)
    class_grade = forms.ChoiceField(label='Grade', choices=class_grade_choices, error_messages={"required": "*"})
    class_credits = forms.CharField(label='Credits',  error_messages={"required": "+64+989849819198419851"})

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
GPAFormset = formset_factory(GPAForm, extra=4)
'''


GPAFormSet = modelformset_factory(

    GPA, fields=("class_name", "class_grade", "class_credits"), extra=2
)
