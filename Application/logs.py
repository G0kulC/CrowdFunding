from django.utils.timezone import now
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import datetime
from django.utils.timezone import now
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from Application.models import *
from django.template.loader import render_to_string
import ast


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    user_log = UserLog(
        user=user,
        device=request.META.get("HTTP_USER_AGENT"),
        ip_address=request.META.get("REMOTE_ADDR"),
    )
    user_log.save()


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    user_log = (
        UserLog.objects.filter(user=user, logout_time__isnull=True)
        .order_by("-login_time")
        .first()
    )
    if user_log:
        user_log.logout_time = now()
        user_log.save()


@login_required
@csrf_protect
def User_logs_view(request):
    if request.user.is_superuser:
        sts = "Super Admin"
        user_log = UserLog.objects.all()
        context = {
            "name": request.user,
            "satus": sts,
            "user_logs": user_log,
        }
        return render(request, "admin_dash_menu/pages/logs/user_logs.html", context)
    else:
        return redirect("notallowed")


@login_required
@csrf_protect
def company_logs_view(request):
    if request.user.is_superuser:
        sts = "Super Admin"
        user_log = CompanyLog.objects.all()
        context = {
            "name": request.user,
            "satus": sts,
            "user_logs": user_log,
        }
        return render(request, "admin_dash_menu/pages/logs/company_logs.html", context)
    else:
        return redirect("notallowed")


@login_required
@csrf_protect
def view_company_logs_pk(request, pk):
    data = dict()
    mydata = CompanyLog.objects.get(pk=pk)
    my_model_instances = mydata.action_data
    context = {
        "my_model_instances": my_model_instances,
    }
    template_name = "admin_dash_menu/pages/logs/company_logs_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def company_logs_project(request):
    s = request.user
    try:
        check_com = Company_table.objects.get(email_id=s, delete_status=False)
        code = check_com.company_code
        name = check_com.company_name
        sts = "Admin"
        proj_log = ProjectLog.objects.filter(company_code=code)
        if request.method == "POST":
            from_date = request.POST["from_date"]
            to_date = request.POST["to_date"]
            name = request.POST["name"]
            checkuser = User.objects.get(username=name)
            proj_log = ProjectLog.objects.filter(
                timestamp__range=(from_date, to_date),
                company_code=code,
                user_id=checkuser.pk,
            )
            context = {
                "name": name,
                "satus": sts,
                "proj_logs": proj_log,
                "company": name,
                "from_date": from_date,
                "to_date": to_date,
                "name": name,
            }

        context = {"name": name, "satus": sts, "proj_logs": proj_log, "company": name}
        return render(request, "admin_dash_menu/pages/logs/project_logs.html", context)
    except Company_table.DoesNotExist:
        return redirect("notallowed")


@login_required
@csrf_protect
def view_project_log(request, pk):
    data = dict()
    mydata = ProjectLog.objects.get(pk=pk)
    my_model_instances = mydata.action_data
    print(mydata)
    context = {
        "my_model_instances": my_model_instances,
    }
    template_name = "admin_dash_menu/pages/logs/project_log_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def company_logs_investor(request):
    s = request.user
    try:
        check_com = Company_table.objects.get(email_id=s, delete_status=False)
        code = check_com.company_code
        name = check_com.company_name
        sts = "Admin"
        proj_log = InvestorLog.objects.filter(company_code=code)
        if request.method == "POST":
            from_date = request.POST["from_date"]
            to_date = request.POST["to_date"]
            name = request.POST["name"]
            checkuser = User.objects.get(username=name)
            proj_log = InvestorLog.objects.filter(
                timestamp__range=(from_date, to_date),
                company_code=code,
                user_id=checkuser.pk,
            )
            context = {
                "name": name,
                "satus": sts,
                "proj_logs": proj_log,
                "company": name,
                "from_date": from_date,
                "to_date": to_date,
            }

        context = {"name": name, "satus": sts, "proj_logs": proj_log, "company": name}
        return render(request, "admin_dash_menu/pages/logs/investor_log.html", context)
    except Company_table.DoesNotExist:
        return redirect("notallowed")


@login_required
@csrf_protect
def view_logs_investor(request, pk):
    data = dict()
    mydata = InvestorLog.objects.get(pk=pk)
    my_model_instances = mydata.action_data
    context = {
        "my_model_instances": my_model_instances,
    }
    template_name = "admin_dash_menu/pages/logs/investor_log_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
