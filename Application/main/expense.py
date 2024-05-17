from django.shortcuts import render, get_object_or_404, redirect
from Application.models import *
from Application.forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import datetime


@login_required
def get_company_projects_exp_names(request):
    if request.user.is_authenticated:
        current_company_name = Company_table.objects.filter(email_id=request.user)
        if current_company_name.exists():
            current_company = Company_table.objects.get(email_id=request.user)
            comp_name = current_company.company_name
            comp_code = current_company.company_code
            current_projects = Staff.objects.filter(company_code=comp_code, satus=True)
            project_list = [{"id": p.id, "name": p.username} for p in current_projects]
            return JsonResponse({"projects": project_list})
        else:
            current_staff = Staff.objects.filter(username=request.user)
            if current_staff.exists():
                all_staff = Staff.objects.get(username=request.user)
                staff_comp_name = all_staff.company_name
                staff_comp_code = all_staff.company_code
                current_projects = Staff.objects.filter(
                    company_code=comp_code, satus=True
                )
                project_list = [
                    {"id": p.id, "name": p.username} for p in current_projects
                ]

    else:
        return JsonResponse({"error": "User is not authenticated"})


@login_required
@csrf_protect
def project_expense_create(request):
    data = dict()
    form = Project_expense_create_Form()
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
        amount = request.POST["amount"]
        Mode_of_payment = request.POST["Mode_of_payment"]
        payment_id = request.POST["payment_id"]

        project_code_get = Project.objects.get(
            project_name=project_name, company_code=code
        )
        project_code = project_code_get.prject_key
        if request.user == company_id:
            project_exp_save = ProjectExpense.objects.create(
                company_name=cmp_name,
                company_code=code,
                project_name=project_name,
                project_code=project_code,
                amount=amount,
                Mode_of_payment=Mode_of_payment,
                payment_id=payment_id,
                status=False,
            )
            temp_data = {
                "company_name": cmp_name,
                "project_name": project_name,
                "amount": amount,
                "Mode_of_payment": Mode_of_payment,
                "payment_id": payment_id,
                "Expense_date": str(project_exp_save.Expense_date.strftime("%d-%m-%Y")),
                "status": False,
            }
            create_log = Expence_log.objects.create(
                company_name=project_exp_save.company_name,
                company_code=project_exp_save.company_code,
                project_name=project_exp_save.project_name,
                project_code=project_exp_save.project_code,
                ip_address=request.META["REMOTE_ADDR"],
                action="Created",
                action_data=temp_data,
                user=request.user,
            )

            project_exp_save.save()
        data["form_is_valid"] = True
        data["add"] = True
        books = ProjectExpense.objects.all()
        data["html_book_list"] = render_to_string(
            "admin_dash_menu/pages/Project_expense/Project_expense.html",
            {"books": books},
        )
    else:
        data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(
        "admin_dash_menu/pages/Project_expense/project_exp_reg.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@login_required
def get_company_projects_expences(request):
    if request.user.is_authenticated:
        try:
            current_company = Company_table.objects.get(email_id=request.user)
        except Company_table.DoesNotExist:
            current_company = Staff.objects.get(username=request.user)
        comp_name = current_company.company_name
        comp_code = current_company.company_code
        current_projects = Project.objects.filter(
            company_code=comp_code, status=True, delete_status=False
        )
        project_list = [{"id": p.id, "name": p.project_name} for p in current_projects]
        return JsonResponse({"projects": project_list})
    else:
        return JsonResponse({"error": "User is not authenticated"})


@login_required
@csrf_protect
def project_expense_list(request):
    try:
        s = request.user
        check_inv = Company_table.objects.get(email_id=s)
        code = check_inv.company_code
        name = check_inv.company_name
        my_model_instances = ProjectExpense.objects.filter(company_code=code)

        sts = "Admin"
        if check_inv is not None:
            context = {
                "my_model_instances": my_model_instances,
                "name": name,
                "satus": sts,
                "company": name,
            }
            return render(
                request,
                "admin_dash_menu/pages/Project_expense/Project_expense.html",
                context,
            )

        else:
            pass
    except Company_table.DoesNotExist:
        check = Staff.objects.get(username=s)
        code = check.company_code
        name = check.company_name
        staf_name = check.username
        my_model_instances = ProjectExpense.objects.filter(company_code=code)
        proj_inv_per = Project_Exp_menu.objects.get(
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
                    "my_model_instances": my_model_instances,
                    "proj_inv_per": proj_inv_per,
                    "name": name,
                    "satus": sts,
                    "staff": staff,
                    "company": name,
                    "project_permissions": project_permissions,
                    "investor_permissions": investor_permissions,
                    "pro_inv_permissions": pro_inv_permissions,
                    "wallet_permissions": wallet_permissions,
                    "pro_exp_permissions": pro_exp_permissions,
                    "pro_profit_permissions": pro_profit_permissions,
                    "dashbord_permissions": dashbord_permissions,
                    "settlement_permissions": settlement_permissions,
                    "Reports_permissions": Reports_permissions,
                }
                return render(
                    request,
                    "admin_dash_menu/pages/Project_expense/Project_expense.html",
                    context,
                )
            else:
                return redirect("notallowed")
        else:
            return redirect("notallowed")
        pass

    else:
        return redirect("notallowed")


@login_required
@csrf_protect
def save_project_expense_form(request, form, template_name):
    data = dict()

    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            books = ProjectExpense.objects.all()
            data["html_book_list"] = render_to_string(
                "admin_dash_menu/pages/Project_expense/Project_expense.html",
                {"books": books},
            )
        else:
            data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def view_project_expense(request, pk):
    data = dict()
    my_model_instances = get_object_or_404(ProjectExpense, pk=pk)
    context = {"my_model_instances": my_model_instances}

    template_name = "admin_dash_menu/pages/Project_expense/project_exp_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def project_expense_update(request, pk):
    book = get_object_or_404(ProjectExpense, pk=pk)
    data = dict()
    hidden_field = None
    try:
        get_com_name = Company_table.objects.get(email_id=request.user)
        first_company = book.First_Approved_by == get_com_name.email_id
        if first_company:
            hidden_field = True
    except Company_table.DoesNotExist:
        hidden_field = None
        get_staff_name = Staff.objects.get(username=request.user)
        first_staff = book.First_Approved_by == get_staff_name.username
        if first_staff:
            hidden_field = True

    if request.method == "POST":
        update_approvel = ProjectExpense.objects.get(pk=pk)
        if update_approvel is not None:
            first = update_approvel.First_Approved_by
            if first is None:
                First_Approved_by = request.POST["First_Approved_by"]
                First_Approved_date = request.POST["First_Approved_date_add"]
                update = ProjectExpense.objects.filter(pk=pk).update(
                    First_Approved_by=First_Approved_by,
                    First_Approved_date=First_Approved_date,
                )
                temp_data = {
                    "company_name": update_approvel.company_name,
                    "project_name": update_approvel.project_name,
                    "amount": update_approvel.amount,
                    "Mode_of_payment": update_approvel.Mode_of_payment,
                    "payment_id": update_approvel.payment_id,
                    "Expense_date": str(
                        update_approvel.Expense_date.strftime("%d-%m-%Y")
                    ),
                    "First_Approved_by": First_Approved_by,
                    "First_Approved_date": str(First_Approved_date),
                    "status": False,
                }
                create_log = Expence_log.objects.create(
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
            elif first is not None:
                Second_Approved_by = request.POST["Second_Approved_by"]
                Second_Approved_date = request.POST["Second_Approved_date_add"]
                update = ProjectExpense.objects.filter(pk=pk).update(
                    Second_Approved_by=Second_Approved_by,
                    Second_Approved_date=Second_Approved_date,
                    status=True,
                )
                temp_data = {
                    "company_name": update_approvel.company_name,
                    "project_name": update_approvel.project_name,
                    "amount": update_approvel.amount,
                    "Mode_of_payment": update_approvel.Mode_of_payment,
                    "payment_id": update_approvel.payment_id,
                    "Expense_date": str(
                        update_approvel.Expense_date.strftime("%d-%m-%Y")
                    ),
                    "First_Approved_by": update_approvel.First_Approved_by,
                    "First_Approved_date": str(
                        update_approvel.First_Approved_date.strftime("%d-%m-%Y")
                    ),
                    "Second_Approved_by": Second_Approved_by,
                    "Second_Approved_date": str(Second_Approved_date),
                    "status": True,
                }
                create_log = Expence_log.objects.create(
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
        data["form_is_valid"] = True
        books = ProjectExpense.objects.all()
        data["html_book_list"] = render_to_string(
            "admin_dash_menu/pages/Project_expense/Project_expense.html",
            {"books": books},
        )

        form = Project_expense_create_Form(request.POST, instance=book)
    else:
        form = Project_expense_create_Form(instance=book)
        data["form_is_valid"] = False

    context = {"form": form, "hidden_field": hidden_field}
    template_name = "admin_dash_menu/pages/Project_expense/project_exp_edit.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def delete_project_expense(request, pk):
    mymodel = get_object_or_404(ProjectExpense, pk=pk)
    trashed_data = TrashedData.objects.create(
        user=request.user,
        original_data=mymodel.__dict__,
    )
    if mymodel.First_Approved_date is not None:
        day1 = mymodel.First_Approved_date.strftime("%d-%m-%Y")
    else:
        day1 = None
    if mymodel.Second_Approved_date is not None:
        day2 = mymodel.Second_Approved_date.strftime("%d-%m-%Y")
    else:
        day2 = None
    temp_data = {
        "company_name": mymodel.company_name,
        "project_name": mymodel.project_name,
        "amount": mymodel.amount,
        "Mode_of_payment": mymodel.Mode_of_payment,
        "payment_id": mymodel.payment_id,
        "Expense_date": str(mymodel.Expense_date.strftime("%d-%m-%Y")),
        "First_Approved_by": mymodel.First_Approved_by,
        "First_Approved_date": str(day1),
        "Second_Approved_by": mymodel.Second_Approved_by,
        "Second_Approved_date": str(day2),
        "status": False,
    }
    create_log = Expence_log.objects.create(
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
def company_logs_expence(request):
    s = request.user
    try:
        check_com = Company_table.objects.get(email_id=s, delete_status=False)
        code = check_com.company_code
        name = check_com.company_name
        sts = "Admin"
        proj_log = Expence_log.objects.filter(company_code=code)
        if request.method == "POST":
            from_date = request.POST["from_date"]
            to_date = request.POST["to_date"]
            name = request.POST["name"]
            checkuser = User.objects.get(username=name)
            proj_log = Expence_log.objects.filter(
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
        return render(request, "admin_dash_menu/pages/logs/expence_log.html", context)
    except Company_table.DoesNotExist:
        return redirect("notallowed")


@login_required
@csrf_protect
def view_logs_expence(request, pk):
    data = dict()
    mydata = Expence_log.objects.get(pk=pk)
    my_model_instances = mydata.action_data
    context = {
        "my_model_instances": my_model_instances,
    }
    template_name = "admin_dash_menu/pages/logs/expence_log_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
