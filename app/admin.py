import tablib
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.forms import *
from import_export import resources
from app.models import CustomUser, Visitor, GPA, Inflation
from import_export.admin import ImportExportModelAdmin


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


class InflationMixin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'year', 'month_code', 'month', 'inflation_rate', 'percent_change')
    search_fields = ('id', 'year', 'month_code', 'month', 'inflation_rate', 'percent_change')
    list_filter = ('id', 'year', 'month_code', 'month', 'inflation_rate', 'percent_change')

    class Meta:
        model = Inflation


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(GPA, GPAAdmin)
admin.site.register(Inflation, InflationMixin)
