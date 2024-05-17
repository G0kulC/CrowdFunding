from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.exclude(is_superuser=True)
        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and obj.is_staff:
            obj.is_staff = False
            obj.is_superuser = False
        super().save_model(request, obj, form, change)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class User_reg(admin.ModelAdmin):
    list_display = [field.name for field in User_Registration_table._meta.get_fields()]


admin.site.register(User_Registration_table, User_reg)


class Company_reg(admin.ModelAdmin):
    list_display = ("company_name", "company_code", "contact_number", "email_id")


admin.site.register(Company_table, Company_reg)


class Project_expense_reg(admin.ModelAdmin):
    list_display = ("pk", "company_name", "amount", "status")


admin.site.register(ProjectExpense, Project_expense_reg)


class Project_Investors_reg(admin.ModelAdmin):
    list_display = ("company_name", "project", "amount", "status")


admin.site.register(Invesments_Db, Project_Investors_reg)


class Project_table_reg(admin.ModelAdmin):
    list_display = ("project_name", "Project_value", "Kickoff_date", "Total_share")


admin.site.register(Project, Project_table_reg)


class Investors_table_reg(admin.ModelAdmin):
    list_display = ("email_id", "mobile_number", "status")


admin.site.register(Investors, Investors_table_reg)
