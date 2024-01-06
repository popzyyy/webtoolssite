from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone
from app.managers import CustomUserManager
from app.validators import *





def refresh(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, editable=False)
    email = models.EmailField(_('email address'), validators=[validate_email], unique=True)
    first_name = models.CharField(max_length=75)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    is_superuser = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Admins"
        verbose_name = "Admin"


class Visitor(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    ipaddress = models.TextField(max_length=150, blank=True)
    when_visited = models.DateTimeField(default=timezone.now)


class GPA(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)

    class_grade_choices = [
        ("A+", "A+"), ("A", "A"), ("A-", "A-"), ("B+", "B+"), ("B", "B"), ("B-", "B-"), ("C+", "C+"), ("C", "C"),
        ("C-", "C-"), ("D+", "D+"), ("D", "D"), ("D-", "D-"), ("F", "F")
    ]
    class_credit_choices = [
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)
    ]
    class_name = models.CharField(max_length=12, blank=True, null=True)
    class_grade = models.CharField(max_length=2, choices=class_grade_choices, blank=True, null=True)
    class_credits = models.IntegerField(choices=class_credit_choices, blank=True, null=True)

    class Meta:
        verbose_name_plural = "GPAs"

    def __str__(self):
        return self.id, self.class_credits, self.class_grade


class Inflation(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    year = models.CharField(blank=True, null=True, max_length=4)
    month_code = models.CharField(blank=True, null=True, max_length=4)
    month = models.CharField(blank=True, null=True, max_length=12)
    inflation_rate = models.DecimalField(blank=True, null=True, decimal_places=15,max_digits=25)
    percent_change = models.DecimalField(blank=True, null=True, decimal_places=15,max_digits=25) # percent change in january from previous january
    percent_change_mom = models.DecimalField(blank=True, null=True, decimal_places=15,max_digits=25)
    percent_change_all = models.DecimalField(blank=True, null=True, decimal_places=15,max_digits=25)




    class Meta:
        verbose_name_plural = "Inflation"

    def __str__(self):
        # Return a string representation of the object
        return f"{self.year},{self.month},{self.inflation_rate}"



