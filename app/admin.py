from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.forms import *

from app.models import CustomUser, Visitor, GPA


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'first_name')
    list_filter = ('email',)
    fieldsets = (
        (None,
         {'fields': ('email', 'first_name', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'first_name')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class VisitorAdmin(admin.ModelAdmin):
    model = Visitor
    list_display = ('id', 'ipaddress', 'when_visited')
    search_fields = ('id', 'ipaddress', 'when_visited')
    list_filter = ('id', 'ipaddress', 'when_visited')


class GPAAdmin(admin.ModelAdmin):
    model = Visitor
    list_display = ('class_name', 'class_grade', 'class_credits')
    search_fields = ('class_name', 'class_grade', 'class_credits')
    list_filter = ('class_name', 'class_grade', 'class_credits')

class YearAdmin(admin.ModelAdmin):
    model = Year



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(GPA, GPAAdmin)
admin.site.register(Year, YearAdmin)
