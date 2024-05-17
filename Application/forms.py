from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from Application.models import *
from django import forms
from Application.models import User_Registration_table
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User_Registration_table
        fields = "__all__"


class Staff_RegistationForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = (
            "username",
            "password",
            "satus",
        )


class CompanyRegistationForm(forms.ModelForm):
    class Meta:
        model = Company_table
        fields = "__all__"


class InvestorRegistationForm(forms.ModelForm):
    class Meta:
        model = Investors
        fields = (
            "first_name",
            "last_name",
            "Display_name",
            "email_id",
            "mobile_number",
            "Pan_number",
            "Aadhar_card_no",
            "contact_address",
            "City",
            "State",
            "pincode",
            "status",
        )


class Project_create_Form(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "project_name",
            "Project_location",
            "Latitude",
            "Longitude",
            "Project_value",
            "Kickoff_date",
            "Returns_projection_type",
            "Returns_projection_value",
            "Other_expense",
            "Total_share",
            "Per_share_value",
            "share_count",
            "Expected_return_date",
            "status",
        )


class Project_expense_create_Form(forms.ModelForm):
    class Meta:
        model = ProjectExpense
        fields = (
            "project_name",
            "amount",
            "Mode_of_payment",
            "payment_id",
            "status",
        )


class Project_profit_Form(forms.ModelForm):
    class Meta:
        model = ProjectSales
        fields = (
            "project_name",
            "unit_sold",
            "amount",
        )


class Project_settlement_Form(forms.ModelForm):
    class Meta:
        model = Projectsettlement
        fields = (
            "investor_name",
            "project_name",
            "amount",
        )


class InvestorWalletDetailsForm(forms.ModelForm):
    class Meta:
        model = Investor_Wallet_Details
        fields = (
            "investor_name",
            "amount",
            "mode_of_payment",
            "payment_id",
            "payment_given_by",
        )


class Project_investor_create_Form(forms.ModelForm):
    class Meta:
        model = Invesments_Db
        fields = ("project", "investor_name", "amount", "Payment_given_by")


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email")
