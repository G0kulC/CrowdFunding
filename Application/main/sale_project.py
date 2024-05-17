from django.shortcuts import render, get_object_or_404, redirect
from Application.models import *
from Application.forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import datetime


@login_required
@csrf_protect
def project_profit_create(request):
    data = dict()
    form = Project_profit_Form()
    if request.method == "POST":
        company_id = request.user
        try:
            get_com_name = Company_table.objects.get(email_id=company_id)
            code = get_com_name.company_code
            cmp_name = get_com_name.company_name
        except Company_table.DoesNotExist:
            get_com_name = Staff.objects.get(username=company_id)
            code = get_com_name.company_code
            cmp_name = get_com_name.company_name
        project_name = request.POST["project"]
        unit_sold = int(request.POST["unit_sold"])
        unit_amount = int(request.POST["amount"])
        avalibale_unit = 0
        avalibale_unit_cost = 0
        ###########################################################################################################
        project_code_get = Project.objects.get(
            project_name=project_name, company_code=code, delete_status=False
        )
        project_code = project_code_get.prject_key
        project_unit_get = ProjectSales.objects.filter(
            project_code=project_code_get.prject_key, Second_Approved_by__isnull=False
        )
        if project_unit_get.exists():
            avalibale_unit = int(project_code_get.Returns_projection_type - (unit_sold))
            avalibale_unit_cost = int(
                (
                    project_code_get.Returns_projection_type
                    * project_code_get.Returns_projection_value
                )
                - (unit_amount)
            )
            # print('avalibale_unit=',avalibale_unit)
            # print('avalibale_unit_cost=',avalibale_unit_cost)
            project_sle_save = ProjectSales.objects.create(
                company_name=cmp_name,
                company_code=code,
                project_name=project_name,
                project_code=project_code,
                unit_sold=unit_sold,
                amount=unit_amount,
                blance_unit=avalibale_unit,
                blance_amount=avalibale_unit_cost,
            )

            project_code_get.save()
            temp_data = {
                "company_name": cmp_name,
                "project_name": project_name,
                "unit_sold": unit_sold,
                "amount": unit_amount,
                "blance_unit": avalibale_unit,
                "blance_amount": avalibale_unit_cost,
                "sales_date": str(project_sle_save.sales_date.strftime("%d-%m-%Y")),
                "status": False,
            }
            create_log = Sales_log.objects.create(
                company_name=project_sle_save.company_name,
                company_code=project_sle_save.company_code,
                project_name=project_sle_save.project_name,
                project_code=project_sle_save.project_code,
                ip_address=request.META["REMOTE_ADDR"],
                action="Created",
                action_data=temp_data,
                user=request.user,
            )

        if not project_unit_get.exists():
            avalibale_unit = int(project_code_get.Returns_projection_type - (unit_sold))
            avalibale_unit_cost = int(
                (
                    project_code_get.Returns_projection_type
                    * project_code_get.Returns_projection_value
                )
                - (unit_amount)
            )
            print("avalibale_unit=", avalibale_unit)
            print("avalibale_unit_cost=", avalibale_unit_cost)
            project_sle_save = None
            project_sle_save = ProjectSales.objects.create(
                company_name=cmp_name,
                company_code=code,
                project_name=project_name,
                project_code=project_code,
                unit_sold=unit_sold,
                amount=unit_amount,
                blance_unit=avalibale_unit,
                blance_amount=avalibale_unit_cost,
            )
            project_code_get.blance_unit = avalibale_unit
            project_code_get.blance_amount = avalibale_unit_cost
            project_code_get.Returns_projection_type = avalibale_unit

            project_code_get.save()
            project_sle_save.save()
            temp_data = {
                "company_name": cmp_name,
                "project_name": project_name,
                "unit_sold": unit_sold,
                "amount": unit_amount,
                "blance_unit": avalibale_unit,
                "blance_amount": avalibale_unit_cost,
                "sales_date": str(project_sle_save.sales_date.strftime("%d-%m-%Y")),
                "status": False,
            }
            create_log = Sales_log.objects.create(
                company_name=project_sle_save.company_name,
                company_code=project_sle_save.company_code,
                project_name=project_sle_save.project_name,
                project_code=project_sle_save.project_code,
                ip_address=request.META["REMOTE_ADDR"],
                action="Created",
                action_data=temp_data,
                user=request.user,
            )

        data["form_is_valid"] = True
        data["add"] = True
        books = ProjectSales.objects.all()
        data["html_book_list"] = render_to_string(
            "admin_dash_menu/pages/profit/Project_profit.html", {"books": books}
        )
    else:
        data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(
        "admin_dash_menu/pages/profit/project_profit_reg.html", context, request=request
    )
    return JsonResponse(data)


@login_required
def get_company_projects_project(request):
    if request.user.is_authenticated:
        try:
            current_company = Company_table.objects.get(email_id=request.user)
        except Company_table.DoesNotExist:
            current_company = Staff.objects.get(username=request.user)
        comp_name = current_company.company_name
        comp_code = current_company.company_code
        current_projects = Project.objects.filter(company_code=comp_code, status=True)
        project_list = [{"id": p.id, "name": p.project_name} for p in current_projects]
        return JsonResponse({"projects": project_list})
    else:
        return JsonResponse({"error": "User is not authenticated"})


@login_required
@csrf_protect
def project_profit_list(request):
    try:
        s = request.user
        check_inv = Company_table.objects.get(email_id=s)
        code = check_inv.company_code
        name = check_inv.company_name
        my_model_instances = ProjectSales.objects.filter(company_code=code)
        sts = "Admin"
        if check_inv is not None:
            context = {
                "my_model_instances": my_model_instances,
                "name": name,
                "satus": sts,
                "company": name,
            }
            return render(
                request, "admin_dash_menu/pages/profit/Project_profit.html", context
            )

        else:
            pass
    except Company_table.DoesNotExist:
        check = Staff.objects.get(username=s)
        code = check.company_code
        name = check.company_name
        staf_name = check.username
        my_model_instances1 = ProjectSales.objects.filter(company_code=code)
        proj_inv_per = Project_Profit_menu.objects.get(
            staff_name=staf_name, company_code=code
        )
        if proj_inv_per.status:
            if (
                proj_inv_per.add
                or proj_inv_per.view
                or proj_inv_per.edit
                or proj_inv_per.can_delete
            ):
                sts = "Staff"
                staff = True
                project_permissions = get_object_or_404(
                    Project_menu, staff_name=s, company_code=code
                )
                investor_permissions = get_object_or_404(
                    Investor_menu, staff_name=s, company_code=code
                )
                pro_inv_permissions = get_object_or_404(
                    Project_investor_menu, staff_name=s, company_code=code
                )
                wallet_permissions = get_object_or_404(
                    Investor_wallet_menu, staff_name=s, company_code=code
                )
                pro_exp_permissions = get_object_or_404(
                    Project_Exp_menu, staff_name=s, company_code=code
                )
                pro_profit_permissions = get_object_or_404(
                    Project_Profit_menu, staff_name=s, company_code=code
                )
                dashbord_permissions = get_object_or_404(
                    Dashbord_view, staff_name=s, company_code=code
                )
                settlement_permissions = get_object_or_404(
                    Project_settlement_menu, staff_name=s, company_code=code
                )
                Reports_permissions = get_object_or_404(
                    Report_view, staff_name=s, company_code=code
                )

                context = {
                    "my_model_instances": my_model_instances1,
                    "proj_inv_per": proj_inv_per,
                    "name": name,
                    "satus": sts,
                    "staff": staff,
                    "company": name,
                    "project_permissions": project_permissions,
                    "investor_permissions": investor_permissions,
                    "wallet_permissions": wallet_permissions,
                    "pro_inv_permissions": pro_inv_permissions,
                    "pro_exp_permissions": pro_exp_permissions,
                    "pro_profit_permissions": pro_profit_permissions,
                    "dashbord_permissions": dashbord_permissions,
                    "settlement_permissions": settlement_permissions,
                    "Reports_permissions": Reports_permissions,
                }
                return render(
                    request, "admin_dash_menu/pages/profit/Project_profit.html", context
                )
            else:
                return redirect("notallowed")
        else:
            return redirect("notallowed")

    else:
        return redirect("notallowed")


@login_required
@csrf_protect
def save_project_profit_form(request, form, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            books = ProjectSales.objects.all()
            data["html_book_list"] = render_to_string(
                "admin_dash_menu/pages/profit/Project_profit.html", {"books": books}
            )
        else:
            data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def view_project_profit(request, pk):
    my_model_instances = get_object_or_404(ProjectSales, pk=pk)
    data = dict()
    context = {"my_model_instances": my_model_instances}
    template_name = "admin_dash_menu/pages/profit/project_profit_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def project_profit_update(request, pk):
    book = get_object_or_404(ProjectSales, pk=pk)
    data = dict()
    hidden_field = None
    company = None

    try:
        get_com_name = Company_table.objects.get(email_id=request.user)
        first_company = book.First_Approved_by == get_com_name.email_id
        if first_company:
            hidden_field = True
        company = True
    except Company_table.DoesNotExist:
        hidden_field = None
        get_staff_name = Staff.objects.get(username=request.user)
        first_staff = book.First_Approved_by == get_staff_name.username
        if first_staff:
            hidden_field = True
    if request.method == "POST":
        update_approvel = ProjectSales.objects.get(pk=pk)
        if update_approvel is not None:
            first = update_approvel.First_Approved_by
            second = update_approvel.Second_Approved_by
            if first is None:
                First_Approved_by = request.POST["First_Approved_by"]
                First_Approved_date = request.POST["First_Approved_date_add"]
                update = ProjectSales.objects.filter(pk=pk).update(
                    First_Approved_by=First_Approved_by,
                    First_Approved_date=First_Approved_date,
                )
                temp_data = {
                    "company_name": update_approvel.company_name,
                    "project_name": update_approvel.project_name,
                    "unit_sold": update_approvel.unit_sold,
                    "amount": update_approvel.amount,
                    "blance_unit": update_approvel.blance_unit,
                    "blance_amount": update_approvel.blance_amount,
                    "sales_date": str(update_approvel.sales_date.strftime("%d-%m-%Y")),
                    "First_Approved_by": First_Approved_by,
                    "First_Approved_date": str(First_Approved_date),
                    "status": False,
                }
                create_log = Sales_log.objects.create(
                    company_name=update_approvel.company_name,
                    company_code=update_approvel.company_code,
                    project_name=update_approvel.project_name,
                    project_code=update_approvel.project_code,
                    ip_address=request.META["REMOTE_ADDR"],
                    action="Approved",
                    action_data=temp_data,
                    user=request.user,
                )

                data["update1"] = True
            elif second is None and first is not None and first != request.user:
                Second_Approved_by = request.POST["Second_Approved_by"]
                Second_Approved_date = request.POST["Second_Approved_date_add"]
                update = ProjectSales.objects.filter(pk=pk).update(
                    Second_Approved_by=Second_Approved_by,
                    Second_Approved_date=Second_Approved_date,
                    status=True,
                )
                temp_data = {
                    "company_name": update_approvel.company_name,
                    "project_name": update_approvel.project_name,
                    "unit_sold": update_approvel.unit_sold,
                    "amount": update_approvel.amount,
                    "blance_unit": update_approvel.blance_unit,
                    "blance_amount": update_approvel.blance_amount,
                    "sales_date": str(update_approvel.sales_date.strftime("%d-%m-%Y")),
                    "First_Approved_by": update_approvel.First_Approved_by,
                    "First_Approved_date": str(update_approvel.First_Approved_date),
                    "Second_Approved_by": Second_Approved_by,
                    "Second_Approved_date": str(Second_Approved_date),
                    "status": True,
                }
                create_log = Sales_log.objects.create(
                    company_name=update_approvel.company_name,
                    company_code=update_approvel.company_code,
                    project_name=update_approvel.project_name,
                    project_code=update_approvel.project_code,
                    ip_address=request.META["REMOTE_ADDR"],
                    action="Approved",
                    action_data=temp_data,
                    user=request.user,
                )

                data["update2"] = True
            elif second is not None and first is not None and company == True:
                unit_count = request.POST["unit_sold"]
                amount = request.POST["amount"]
                sales_date = request.POST["sales_date"]
                update = ProjectSales.objects.filter(pk=pk).update(
                    unit_sold=unit_count, amount=amount, sales_date=sales_date
                )
                temp_data = {
                    "company_name": update_approvel.company_name,
                    "project_name": update_approvel.project_name,
                    "unit_sold": update_approvel.unit_sold,
                    "amount": update_approvel.amount,
                    "blance_unit": update_approvel.blance_unit,
                    "blance_amount": update_approvel.blance_amount,
                    "sales_date": str(update_approvel.sales_date.strftime("%d-%m-%Y")),
                    "First_Approved_by": update_approvel.First_Approved_by,
                    "First_Approved_date": str(update_approvel.First_Approved_date),
                    "Second_Approved_by": update_approvel.Second_Approved_by,
                    "Second_Approved_date": str(update_approvel.Second_Approved_date),
                    "status": True,
                }
                create_log = Sales_log.objects.create(
                    company_name=update_approvel.company_name,
                    company_code=update_approvel.company_code,
                    project_name=update_approvel.project_name,
                    project_code=update_approvel.project_code,
                    ip_address=request.META["REMOTE_ADDR"],
                    action="Updated",
                    action_data=temp_data,
                    user=request.user,
                )
                data["Updated"] = True

        data["form_is_valid"] = True
        books = ProjectSales.objects.all()
        data["html_book_list"] = render_to_string(
            "admin_dash_menu/pages/profit/Project_profit.html", {"books": books}
        )
        form = Project_profit_Form(request.POST, instance=book)
    else:
        form = Project_profit_Form(instance=book)
        data["form_is_valid"] = False

    context = {"form": form, "hidden_field": hidden_field, "company": company}
    template_name = "admin_dash_menu/pages/profit/project_profit_edit.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def delete_project_profit(request, pk):
    mymodel = get_object_or_404(ProjectSales, pk=pk)
    trashed_data = TrashedData.objects.create(
        user=request.user,
        original_data=mymodel.__dict__,
    )
    temp_data = {
        "company_name": mymodel.company_name,
        "project_name": mymodel.project_name,
        "unit_sold": mymodel.unit_sold,
        "amount": mymodel.amount,
        "blance_unit": mymodel.blance_unit,
        "blance_amount": mymodel.blance_amount,
        "sales_date": str(mymodel.sales_date.strftime("%d-%m-%Y")),
        "First_Approved_by": mymodel.First_Approved_by,
        "First_Approved_date": str(mymodel.First_Approved_date),
        "Second_Approved_by": mymodel.Second_Approved_by,
        "Second_Approved_date": str(mymodel.Second_Approved_date),
        "status": False,
    }
    create_log = Sales_log.objects.create(
        company_name=mymodel.company_name,
        company_code=mymodel.company_code,
        project_name=mymodel.project_name,
        project_code=mymodel.project_code,
        ip_address=request.META["REMOTE_ADDR"],
        action="Deleted",
        action_data=temp_data,
        user=request.user,
    )
    mymodel.delete()
    return JsonResponse({"status": "ok"})


# ------------------------              LOGS                -------------------------------->


@login_required
@csrf_protect
def company_logs_sales(request):
    s = request.user
    try:
        check_com = Company_table.objects.get(email_id=s, delete_status=False)
        code = check_com.company_code
        name = check_com.company_name
        sts = "Admin"
        proj_log = Sales_log.objects.filter(company_code=code)
        if request.method == "POST":
            from_date = request.POST["from_date"]
            to_date = request.POST["to_date"]
            name = request.POST["name"]
            checkuser = User.objects.get(username=name)
            proj_log = Sales_log.objects.filter(
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
        return render(request, "admin_dash_menu/pages/logs/sales_log.html", context)
    except Company_table.DoesNotExist:
        return redirect("notallowed")


@login_required
@csrf_protect
def view_logs_sales(request, pk):
    data = dict()
    mydata = Sales_log.objects.get(pk=pk)
    my_model_instances = mydata.action_data
    context = {
        "my_model_instances": my_model_instances,
    }
    template_name = "admin_dash_menu/pages/logs/sales_log_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
