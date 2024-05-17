import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField(blank=True, null=True)
    active_time = models.DurationField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate active time if both login and logout times are available
        if self.login_time and self.logout_time:
            self.active_time = self.logout_time - self.login_time

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


class User_Registration_table(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    Display_name = models.CharField(max_length=30, blank=True)
    email_id = models.EmailField(max_length=254, unique=True, blank=False)
    user_name = models.CharField(max_length=30, blank=False, unique=False)
    password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=30, blank=False)
    Pan_number = models.CharField(max_length=50, blank=False, unique=False)
    Aadhar_card_no = models.BigIntegerField(blank=True, unique=False)
    contact_address = models.TextField()
    City = models.CharField(max_length=200)
    State = models.CharField(max_length=200)
    pincode = models.CharField(max_length=200)

    def __str__(self):
        return self.email_id


class Company_table(models.Model):
    company_name = models.CharField(max_length=200, blank=False, unique=True)
    company_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email_id = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=50)
    contact_number = models.BigIntegerField(blank=False, unique=True)
    company_pan = models.CharField(max_length=16, blank=False)
    gstin = models.CharField(max_length=16, blank=False)
    Company_addresss = models.TextField(blank=False)
    City = models.CharField(max_length=200, blank=False)
    State = models.CharField(max_length=200, blank=False)
    pincode = models.BigIntegerField(blank=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    delete_status = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ["-created_at"]


class CompanyLog(models.Model):
    email_id = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    company = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField()
    action = models.CharField(max_length=100)
    action_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    perment_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company}"

    class Meta:
        ordering = ["-timestamp"]


class Investors(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.UUIDField()
    investors_code = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    Display_name = models.CharField(max_length=30, blank=True)
    email_id = models.EmailField(max_length=254, blank=False)
    user_name = models.CharField(max_length=30, blank=False)
    password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=30, blank=False)
    Pan_number = models.CharField(max_length=50, blank=False)
    Aadhar_card_no = models.BigIntegerField(blank=True)
    contact_address = models.TextField()
    City = models.CharField(max_length=200)
    State = models.CharField(max_length=200)
    pincode = models.CharField(max_length=200)
    status = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delete_status = models.BooleanField(default=False)

    def __str__(self):
        return self.email_id

    class Meta:
        ordering = ["-created_at"]


class InvestorLog(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.UUIDField()
    investors_code = models.UUIDField()
    email_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    action = models.CharField(max_length=100)
    action_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    perment_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email_id}"

    class Meta:
        ordering = ["-timestamp"]


class Investor_Wallet_Details(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.UUIDField()
    investor_id = models.UUIDField()
    wallet_key = models.UUIDField(default=uuid.uuid4, editable=False)
    investor_name = models.CharField(max_length=100)
    amount = models.BigIntegerField()
    total_amount = models.BigIntegerField(null=True, blank=True)
    mode_of_payment = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=200)
    payment_given_by = models.CharField(max_length=100)
    payment_receiver_name = models.CharField(max_length=100)
    First_Approved_by = models.CharField(max_length=200, null=True, blank=True)
    First_Approved_date = models.DateField(null=True, blank=True)
    Second_Approved_by = models.CharField(max_length=200, null=True, blank=True)
    Second_Approved_date = models.DateField(null=True, blank=True)
    paid_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)
    delete_status = models.BooleanField(default=False)

    def __str__(self):
        return self.investor_name

    class Meta:
        ordering = ["-paid_date"]


class InvestorsWalletLog(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.UUIDField()
    investors_code = models.UUIDField()
    investor_name = models.CharField(max_length=100)
    wallet_key = models.UUIDField()
    ip_address = models.GenericIPAddressField()
    action = models.CharField(max_length=100)
    action_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    perment_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.investor_name}"

    class Meta:
        ordering = ["-timestamp"]


class Investor_Wallet_History_Details(models.Model):
    investor_name = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    credited_amount = models.BigIntegerField()
    wallet_key = models.UUIDField()
    credited_time = models.DateTimeField(blank=True)
    debited_amount = models.BigIntegerField()
    debited_date = models.DateTimeField(blank=True)
    total_amount = models.BigIntegerField()
    delete_status = models.BooleanField(default=False)

    def __str__(self):
        return self.investor_name


class Project(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.UUIDField()
    project_name = models.CharField(max_length=100, blank=False)
    prject_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    Project_location = models.CharField(max_length=200)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    Project_value = models.BigIntegerField(blank=True, null=True)
    Kickoff_date = models.CharField(max_length=20, blank=True, null=True)
    Returns_projection_type = models.BigIntegerField(blank=True, null=True)
    Returns_projection_value = models.BigIntegerField(blank=True, null=True)
    total_unit_value = models.BigIntegerField(blank=True, null=True)
    blance_unit = models.BigIntegerField(null=True)
    blance_amount = models.BigIntegerField(null=True)
    Other_expense = models.BigIntegerField(blank=True, null=True)
    Total_share = models.BigIntegerField(blank=True, null=True)
    Per_share_value = models.BigIntegerField(blank=True, null=True)
    share_count = models.BigIntegerField(blank=True, null=True)
    Expected_return_date = models.CharField(max_length=20, blank=True, null=True)
    Created_datetime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(null=True)
    closed_project = models.BooleanField(null=True)
    closed_date = models.DateField(null=True, blank=True)
    delete_status = models.BooleanField(default=False)

    def __str__(self):
        return self.project_name

    class Meta:
        ordering = ["-Created_datetime"]


class ProjectLog(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.UUIDField()
    project_name = models.CharField(max_length=100)
    project_code = models.UUIDField()
    ip_address = models.GenericIPAddressField()
    action = models.CharField(max_length=100)
    action_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    perment_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project_name}"

    class Meta:
        ordering = ["-timestamp"]


class Invesments_Db(models.Model):
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    project = models.CharField(max_length=100)
    project_code = models.UUIDField()
    investor_name = models.CharField(max_length=100)
    investor_code = models.UUIDField()
    wallet_key = models.UUIDField()
    project_share_value = models.BigIntegerField()
    investor_share_count = models.BigIntegerField()
    amount = models.BigIntegerField()
    Payment_given_by = models.CharField(max_length=200)
    Payment_revceiver_name = models.CharField(max_length=200)
    Paid_date = models.DateTimeField(auto_now_add=True)
    First_Approved_by = models.CharField(max_length=200, null=True, blank=True)
    First_Approved_date = models.DateField(null=True, blank=True)
    Second_Approved_by = models.CharField(max_length=200, null=True, blank=True)
    Second_Approved_date = models.DateField(null=True, blank=True)
    Createdatetime = models.DateTimeField(auto_now_add=True)
    invesment_start = models.BooleanField()
    invesment_end = models.BooleanField()
    status = models.BooleanField()
    delete_status = models.BooleanField(default=False)

    class Meta:
        ordering = ["-Paid_date"]


class Invested_project_Log(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.UUIDField()
    project_name = models.CharField(max_length=100)
    project_code = models.UUIDField()
    investor_name = models.CharField(max_length=100)
    investor_code = models.UUIDField()
    ip_address = models.GenericIPAddressField()
    action = models.CharField(max_length=100)
    action_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    perment_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.investor_name}"

    class Meta:
        ordering = ["-timestamp"]


class ProjectExpense(models.Model):
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    project_name = models.CharField(max_length=100)
    project_code = models.UUIDField()
    Expense_date = models.DateTimeField(auto_now_add=True)
    amount = models.BigIntegerField()
    Mode_of_payment = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=200)
    First_Approved_by = models.CharField(max_length=200, null=True, blank=True)
    First_Approved_date = models.DateField(null=True, blank=True)
    Second_Approved_by = models.CharField(max_length=200, null=True, blank=True)
    Second_Approved_date = models.DateField(null=True, blank=True)
    Createddatetime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(null=True)
    delete_status = models.BooleanField(default=False)

    class Meta:
        ordering = ["-Expense_date"]


class Expence_log(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.UUIDField()
    project_name = models.CharField(max_length=100)
    project_code = models.UUIDField()
    ip_address = models.GenericIPAddressField()
    action = models.CharField(max_length=100)
    action_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    perment_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project_name}"

    class Meta:
        ordering = ["-timestamp"]


class ProjectSales(models.Model):
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    project_name = models.CharField(max_length=100)
    project_code = models.UUIDField()
    unit_sold = models.BigIntegerField(null=True)
    amount = models.BigIntegerField(null=True)
    blance_unit = models.BigIntegerField(null=True)
    blance_amount = models.BigIntegerField(null=True)
    First_Approved_by = models.CharField(max_length=200, null=True, blank=True)
    First_Approved_date = models.DateField(null=True, blank=True)
    Second_Approved_by = models.CharField(max_length=200, null=True, blank=True)
    Second_Approved_date = models.DateField(null=True, blank=True)
    sales_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(null=True)
    delete_status = models.BooleanField(default=False)

    class Meta:
        ordering = ["-sales_date"]


class Sales_log(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.UUIDField()
    project_name = models.CharField(max_length=100)
    project_code = models.UUIDField()
    ip_address = models.GenericIPAddressField()
    action = models.CharField(max_length=100)
    action_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    perment_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project_name}"

    class Meta:
        ordering = ["-timestamp"]


class Projectsettlement(models.Model):
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    investor_name = models.CharField(max_length=100)
    investor_code = models.UUIDField()
    project_name = models.CharField(max_length=100)
    project_code = models.UUIDField()
    wallet_key = models.UUIDField()
    amount = models.BigIntegerField(null=True)
    blance_amount = models.BigIntegerField(null=True)
    First_Approved_by = models.CharField(max_length=200, null=True, blank=True)
    First_Approved_date = models.DateField(null=True, blank=True)
    Second_Approved_by = models.CharField(max_length=200, null=True, blank=True)
    Second_Approved_date = models.DateField(null=True, blank=True)
    settlement_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(null=True)
    delete_status = models.BooleanField(default=False)

    class Meta:
        ordering = ["-settlement_date"]


class settlement_log(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.UUIDField()
    investor_code = models.UUIDField()
    wallet_key = models.UUIDField()
    ip_address = models.GenericIPAddressField()
    action = models.CharField(max_length=100)
    action_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    perment_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]


class TrashedData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_data = models.TextField()
    trashed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-trashed_at"]


class Staff(models.Model):
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    satus = models.BooleanField(default=True)
    delete_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class staff_logs(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.UUIDField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    ip_address = models.GenericIPAddressField()
    action = models.CharField(max_length=100)
    action_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    perment_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        ordering = ["-timestamp"]


class Project_menu(models.Model):
    staff_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    view = models.BooleanField(null=True)
    add = models.BooleanField(null=True)
    edit = models.BooleanField(null=True)
    can_delete = models.BooleanField(null=True)
    status = models.BooleanField(null=True)


class Project_profit_table(models.Model):
    staff_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    view = models.BooleanField(null=True)
    add = models.BooleanField(null=True)
    edit = models.BooleanField(null=True)
    can_delete = models.BooleanField(null=True)
    status = models.BooleanField(null=True)


class Investor_menu(models.Model):
    staff_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    view = models.BooleanField(null=True)
    add = models.BooleanField(null=True)
    edit = models.BooleanField(null=True)
    can_delete = models.BooleanField(null=True)
    status = models.BooleanField(null=True)


class Investor_wallet_menu(models.Model):
    staff_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    view = models.BooleanField(null=True)
    add = models.BooleanField(null=True)
    edit = models.BooleanField(null=True)
    can_delete = models.BooleanField(null=True)
    status = models.BooleanField(null=True)


class Project_investor_menu(models.Model):
    staff_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    view = models.BooleanField(null=True)
    add = models.BooleanField(null=True)
    edit = models.BooleanField(null=True)
    can_delete = models.BooleanField(null=True)
    status = models.BooleanField(null=True)


class Project_Exp_menu(models.Model):
    staff_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    view = models.BooleanField(null=True)
    add = models.BooleanField(null=True)
    edit = models.BooleanField(null=True)
    can_delete = models.BooleanField(null=True)
    status = models.BooleanField(null=True)


class Project_Profit_menu(models.Model):
    staff_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    view = models.BooleanField(null=True)
    add = models.BooleanField(null=True)
    edit = models.BooleanField(null=True)
    can_delete = models.BooleanField(null=True)
    status = models.BooleanField(null=True)


class Project_settlement_menu(models.Model):
    staff_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    view = models.BooleanField(null=True)
    add = models.BooleanField(null=True)
    edit = models.BooleanField(null=True)
    can_delete = models.BooleanField(null=True)
    status = models.BooleanField(null=True)


class Report_view(models.Model):
    staff_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    view = models.BooleanField(null=True)
    status = models.BooleanField(null=True)


class Dashbord_view(models.Model):
    staff_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    company_code = models.UUIDField()
    view = models.BooleanField(null=True)
    status = models.BooleanField(null=True)
