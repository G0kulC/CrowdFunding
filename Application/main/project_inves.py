import datetime
from django.shortcuts import render, get_object_or_404, redirect
from Application.models import *
from Application.forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


@login_required
@csrf_protect
def project_investor_list(request):
    try:
        s = request.user
        check_inv = Company_table.objects.get(email_id=s)
        code = check_inv.company_code
        name = check_inv.company_name
        my_model_instances = Invesments_Db.objects.filter(
            company_code=code, delete_status=False
        )
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
                "admin_dash_menu/pages/Project_Investor/Project_Investors.html",
                context,
            )

        else:
            pass
    except Company_table.DoesNotExist:
        check = Staff.objects.get(username=s)
        code = check.company_code
        name = check.company_name
        staf_name = check.username
        my_model_instances = Invesments_Db.objects.filter(
            company_code=code, delete_status=False
        )
        proj_inv_per = Project_investor_menu.objects.get(
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
                    "wallet_permissions": wallet_permissions,
                    "pro_inv_permissions": pro_inv_permissions,
                    "pro_exp_permissions": pro_exp_permissions,
                    "pro_profit_permissions": pro_profit_permissions,
                    "dashbord_permissions": dashbord_permissions,
                    "settlement_permissions": settlement_permissions,
                    "Reports_permissions": Reports_permissions,
                }
                return render(
                    request,
                    "admin_dash_menu/pages/Project_Investor/Project_Investors.html",
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
def save_project_investor_form(request, form, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            books = Invesments_Db.objects.all()
            data["html_book_list"] = render_to_string(
                "admin_dash_menu/pages/Project_Investor/Project_Investors.html",
                {"books": books},
            )
        else:
            data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def get_company_investors(request):
    if request.user.is_authenticated:
        try:
            current_company = Company_table.objects.get(email_id=request.user)
        except Company_table.DoesNotExist:
            current_company = None
            staff_check = Staff.objects.get(username=request.user)
            current_company = Company_table.objects.get(
                company_code=staff_check.company_code
            )
        comp_name = current_company.company_name
        comp_code = current_company.company_code

        current_projects = Investors.objects.filter(
            company_code=comp_code, status=True, delete_status=False
        )
        project_list = [{"invs_name": p.email_id} for p in current_projects]
        return JsonResponse({"projects": project_list})
    else:
        return JsonResponse({"error": "User is not authenticated"})


@login_required
def get_company_projects(request):
    if request.user.is_authenticated:
        try:
            current_company = Company_table.objects.get(email_id=request.user)
        except Company_table.DoesNotExist:
            current_company = None
            staff_check = Staff.objects.get(username=request.user)
            current_company = Company_table.objects.get(
                company_code=staff_check.company_code
            )
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
def get_company_projects_sales(request):
    if request.user.is_authenticated:
        try:
            current_company = Company_table.objects.get(email_id=request.user)
        except Company_table.DoesNotExist:
            current_company = None
            staff_check = Staff.objects.get(username=request.user)
            current_company = Company_table.objects.get(
                company_code=staff_check.company_code
            )
        comp_name = current_company.company_name
        comp_code = current_company.company_code

        current_projects = Project.objects.filter(
            company_code=comp_code, status=True, delete_status=False
        )
        project_list = [{"id": p.pk, "name": p.project_name} for p in current_projects]
        return JsonResponse({"projects": project_list})
    else:
        return JsonResponse({"error": "User is not authenticated"})


@login_required
@csrf_protect
def view_project_investors(request, pk):
    data = dict()
    my_model_instances = get_object_or_404(Invesments_Db, pk=pk, delete_status=False)
    context = {"my_model_instances": my_model_instances}

    template_name = "admin_dash_menu/pages/Project_Investor/project_ins_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def project_investor_update(request, pk):
    book = get_object_or_404(Invesments_Db, pk=pk)
    data = dict()
    first = None
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
        update_approvel = Invesments_Db.objects.get(pk=pk)
        if update_approvel is not None:
            first = update_approvel.First_Approved_by
            if first is None:
                First_Approved_by = request.POST["First_Approved_by"]
                First_Approved_date = request.POST["First_Approved_date_add"]
                update = Invesments_Db.objects.filter(pk=pk).update(
                    First_Approved_by=First_Approved_by,
                    First_Approved_date=First_Approved_date,
                )
                temp_data_first = {
                    "company_name": update_approvel.company_name,
                    "investor_name": update_approvel.investor_name,
                    "project": update_approvel.project,
                    "amount": update_approvel.amount,
                    "project_share_value": update_approvel.project_share_value,
                    "investor_share_count": update_approvel.investor_share_count,
                    "Payment_given_by": update_approvel.investor_name,
                    "Payment_revceiver_name": update_approvel.Payment_revceiver_name,
                    "Paid_date": str(update_approvel.Paid_date),
                    "First_Approved_by": update_approvel.First_Approved_by,
                    "First_Approved_date": str(update_approvel.First_Approved_date),
                    "Second_Approved_by": update_approvel.Second_Approved_by,
                    "Second_Approved_date": str(update_approvel.Second_Approved_date),
                    "status": update_approvel.status,
                }
                create_log = Invested_project_Log.objects.create(
                    company_name=update_approvel.company_name,
                    company_code=update_approvel.company_code,
                    project_name=update_approvel.project,
                    project_code=update_approvel.project_code,
                    investor_name=update_approvel.investor_name,
                    investor_code=update_approvel.investor_code,
                    ip_address=request.META["REMOTE_ADDR"],
                    action="Approved",
                    action_data=temp_data_first,
                    user=request.user,
                )
                data["update1"] = True
            elif first is not None:
                f1 = first
                name = request.user
                Second_Approved_by = request.POST["Second_Approved_by"]
                Second_Approved_date = request.POST["Second_Approved_date_add"]

                update_amount = Investor_Wallet_Details.objects.get(
                    investor_id=update_approvel.investor_code
                )
                blance = int(update_amount.total_amount) - int(update_approvel.amount)
                filter_update = Investor_Wallet_Details.objects.filter(
                    investor_id=update_approvel.investor_code
                ).update(total_amount=blance)
                update = Invesments_Db.objects.filter(pk=pk).update(
                    Second_Approved_by=Second_Approved_by,
                    Second_Approved_date=Second_Approved_date,
                    status=True,
                )
                update_project = Project.objects.get(
                    prject_key=update_approvel.project_code
                )
                update_project.share_count = int(update_project.share_count) - int(
                    update_approvel.investor_share_count
                )
                wallet_history = Investor_Wallet_History_Details.objects.create(
                    investor_name=update_approvel.investor_name,
                    reason="Money Invested to " + update_approvel.project + " Project",
                    credited_amount=0,
                    wallet_key=update_approvel.wallet_key,
                    credited_time=datetime.datetime.now(),
                    debited_amount=update_approvel.amount,
                    debited_date=datetime.datetime.now(),
                    total_amount=blance,
                )
                temp_data_second = {
                    "company_name": update_approvel.company_name,
                    "investor_name": update_approvel.investor_name,
                    "project": update_approvel.project,
                    "amount": update_approvel.amount,
                    "project_share_value": update_approvel.project_share_value,
                    "investor_share_count": update_approvel.investor_share_count,
                    "Payment_given_by": update_approvel.investor_name,
                    "Payment_revceiver_name": update_approvel.Payment_revceiver_name,
                    "Paid_date": str(update_approvel.Paid_date),
                    "First_Approved_by": update_approvel.First_Approved_by,
                    "First_Approved_date": str(update_approvel.First_Approved_date),
                    "Second_Approved_by": Second_Approved_by,
                    "Second_Approved_date": str(Second_Approved_date),
                    "Paid_date": str(update_approvel.Paid_date),
                    "status": update_approvel.status,
                }
                create_log = Invested_project_Log.objects.create(
                    company_name=update_approvel.company_name,
                    company_code=update_approvel.company_code,
                    project_name=update_approvel.project,
                    project_code=update_approvel.project_code,
                    investor_name=update_approvel.investor_name,
                    investor_code=update_approvel.investor_code,
                    ip_address=request.META["REMOTE_ADDR"],
                    action="Approved",
                    action_data=temp_data_second,
                    user=request.user,
                )
                update_project.save()

                data["update2"] = True

        data["form_is_valid"] = True
        books = Invesments_Db.objects.all()
        data["html_book_list"] = render_to_string(
            "admin_dash_menu/pages/Project_Investor/Project_Investors.html",
            {"books": books},
        )

        form = Project_investor_create_Form(request.POST, instance=book)
    else:
        form = Project_investor_create_Form(instance=book)
        data["form_is_valid"] = False
    context = {"form": form, "hidden_field": hidden_field}
    template_name = "admin_dash_menu/pages/Project_Investor/project_inv_edit.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def delete_project_investor(request, pk):
    mymodel = get_object_or_404(Invesments_Db, pk=pk)
    trashed_data = TrashedData.objects.create(
        user=request.user,
        original_data=mymodel.__dict__,
    )
    blance_redo = 0
    if mymodel.status == True:
        redo_amount = Investor_Wallet_Details.objects.get(
            investor_id=mymodel.investor_code
        )
        blance_redo = int(redo_amount.total_amount) + int(mymodel.amount)
        filter_update = Investor_Wallet_Details.objects.filter(
            investor_id=mymodel.investor_code
        ).update(total_amount=blance_redo)
        update_project = Project.objects.get(prject_key=mymodel.project_code)
        update_project.share_count = int(update_project.share_count) + int(
            mymodel.investor_share_count
        )
        update_project.save()
    else:
        pass
    wallet_history = Investor_Wallet_History_Details.objects.create(
        investor_name=mymodel.investor_name,
        reason="Money Reversed from " + mymodel.project + " Project",
        credited_amount=mymodel.amount,
        wallet_key=mymodel.wallet_key,
        credited_time=datetime.datetime.now(),
        debited_date=datetime.datetime.now(),
        debited_amount=0,
        total_amount=blance_redo,
    )
    temp_data_second = {
        "company_name": mymodel.company_name,
        "investor_name": mymodel.investor_name,
        "project": mymodel.project,
        "amount": mymodel.amount,
        "project_share_value": mymodel.project_share_value,
        "investor_share_count": mymodel.investor_share_count,
        "Payment_given_by": mymodel.investor_name,
        "Payment_revceiver_name": mymodel.Payment_revceiver_name,
        "Paid_date": str(mymodel.Paid_date),
        "First_Approved_by": mymodel.First_Approved_by,
        "First_Approved_date": str(mymodel.First_Approved_date),
        "Second_Approved_by": mymodel.Second_Approved_by,
        "Second_Approved_date": str(mymodel.Second_Approved_date),
        "status": mymodel.status,
    }
    create_log = Invested_project_Log.objects.create(
        company_name=mymodel.company_name,
        company_code=mymodel.company_code,
        project_name=mymodel.project,
        project_code=mymodel.project_code,
        investor_name=mymodel.investor_name,
        investor_code=mymodel.investor_code,
        ip_address=request.META["REMOTE_ADDR"],
        action="Deleted",
        action_data=temp_data_second,
        user=request.user,
    )

    mymodel.delete()

    return JsonResponse({"status": "ok"})


@login_required
@csrf_protect
def project_investor_create(request):
    data = dict()
    form = Project_investor_create_Form()
    if request.method == "POST":
        company_id = request.user
        try:
            get_com_name = Company_table.objects.get(email_id=company_id)
        except Company_table.DoesNotExist:
            get_com_name = None
            staff_login = Staff.objects.get(username=company_id)
            checkcompany = staff_login.company_name
            get__name = Company_table.objects.get(company_name=checkcompany)
            get_com_name = get__name

        code = get_com_name.company_code
        cmp_name = get_com_name.company_name
        project = request.POST["project"]
        investor_name = request.POST["investor_name"]
        amount = request.POST["amount"]
        Payment_revceiver_name = request.POST["Payment_revceiver_name"]
        project_share_value = request.POST["project_share_value"]
        investor_share_count = request.POST["investor_share_count"]

        investor_code_get = Investors.objects.get(
            email_id=investor_name, company_code=code
        )
        investor_code = investor_code_get.investors_code
        project_code_get = Project.objects.get(
            project_name=project, company_code=code, delete_status=False
        )
        project_code = project_code_get.prject_key
        investor_value_invesment = None
        deleted_amount = int(amount)
        invested_amount = 0
        try:
            check_last_approval = Invesments_Db.objects.filter(
                company_code=code
            ).latest("id")

            if check_last_approval.status == True:
                try:
                    investor_value_invesment = Investor_Wallet_Details.objects.get(
                        investor_id=investor_code
                    )
                    if investor_value_invesment is None:
                        invested_amount = 0
                    elif investor_value_invesment is not None:
                        invested_amount = int(
                            investor_value_invesment.total_amount - deleted_amount
                        )
                        project_inv_save = Invesments_Db.objects.create(
                            company_name=cmp_name,
                            company_code=code,
                            investor_name=investor_name,
                            investor_code=investor_code,
                            project=project,
                            project_code=project_code,
                            wallet_key=investor_value_invesment.wallet_key,
                            amount=amount,
                            project_share_value=project_share_value,
                            investor_share_count=investor_share_count,
                            Payment_given_by=investor_name,
                            Payment_revceiver_name=Payment_revceiver_name,
                            status=False,
                            invesment_start=True,
                            invesment_end=False,
                        )

                        project_inv_save.save()
                        temp_data = {
                            "company_name": cmp_name,
                            "investor_name": investor_name,
                            "project": project,
                            "amount": amount,
                            "project_share_value": project_share_value,
                            "investor_share_count": investor_share_count,
                            "Payment_given_by": investor_name,
                            "Payment_revceiver_name": Payment_revceiver_name,
                            "status": False,
                            "invesment_start": True,
                            "invesment_end": False,
                        }
                        create_log = Invested_project_Log.objects.create(
                            company_name=project_inv_save.company_name,
                            company_code=project_inv_save.company_code,
                            project_name=project_inv_save.project,
                            project_code=project_inv_save.project_code,
                            investor_name=project_inv_save.investor_name,
                            investor_code=project_inv_save.investor_code,
                            ip_address=request.META["REMOTE_ADDR"],
                            action="Created",
                            action_data=temp_data,
                            user=request.user,
                        )

                        # wallet_history.save()
                        data["form_is_valid"] = True
                        data["add"] = True
                except Investor_Wallet_Details.DoesNotExist:
                    investor_value_invesment = None
                    data["form_is_valid"] = False
            else:
                data["pending"] = True
        except Invesments_Db.DoesNotExist:
            try:
                investor_value_invesment = Investor_Wallet_Details.objects.get(
                    investor_id=investor_code
                )
                if investor_value_invesment is None:
                    invested_amount = 0
                elif investor_value_invesment is not None:
                    invested_amount = int(
                        investor_value_invesment.total_amount - deleted_amount
                    )
                    project_inv_save = Invesments_Db.objects.create(
                        company_name=cmp_name,
                        company_code=code,
                        investor_name=investor_name,
                        investor_code=investor_code,
                        project=project,
                        project_code=project_code,
                        wallet_key=investor_value_invesment.wallet_key,
                        amount=amount,
                        project_share_value=project_share_value,
                        investor_share_count=investor_share_count,
                        Payment_given_by=investor_name,
                        Payment_revceiver_name=Payment_revceiver_name,
                        status=False,
                        invesment_start=True,
                        invesment_end=False,
                    )

                    project_inv_save.save()
                    temp_data = {
                        "company_name": cmp_name,
                        "investor_name": investor_name,
                        "project": project,
                        "amount": amount,
                        "project_share_value": project_share_value,
                        "investor_share_count": investor_share_count,
                        "Payment_given_by": investor_name,
                        "Payment_revceiver_name": Payment_revceiver_name,
                        "status": False,
                        "invesment_start": True,
                        "invesment_end": False,
                    }
                    create_log = Invested_project_Log.objects.create(
                        company_name=project_inv_save.company_name,
                        company_code=project_inv_save.company_code,
                        project_name=project_inv_save.project,
                        project_code=project_inv_save.project_code,
                        investor_name=project_inv_save.investor_name,
                        investor_code=project_inv_save.investor_code,
                        ip_address=request.META["REMOTE_ADDR"],
                        action="Created",
                        action_data=temp_data,
                        user=request.user,
                    )

                    # wallet_history.save()
                    data["form_is_valid"] = True
                    data["add"] = True
            except Investor_Wallet_Details.DoesNotExist:
                investor_value_invesment = None
                data["form_is_valid"] = False

        books = Invesments_Db.objects.all()
        data["html_book_list"] = render_to_string(
            "admin_dash_menu/pages/Project_Investor/Project_Investors.html",
            {"books": books},
        )
    else:
        data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(
        "admin_dash_menu/pages/Project_Investor/project_inv_reg.html",
        context,
        request=request,
    )
    return JsonResponse(data)


# ------------------------              LOGS                -------------------------------->


@login_required
@csrf_protect
def company_logs_project_investor(request):
    s = request.user
    try:
        check_com = Company_table.objects.get(email_id=s, delete_status=False)
        code = check_com.company_code
        name = check_com.company_name
        sts = "Admin"
        proj_log = Invested_project_Log.objects.filter(company_code=code)
        if request.method == "POST":
            from_date = request.POST["from_date"]
            to_date = request.POST["to_date"]
            name = request.POST["name"]
            checkuser = User.objects.get(username=name)
            proj_log = Invested_project_Log.objects.filter(
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
        return render(
            request, "admin_dash_menu/pages/logs/project_investor_log.html", context
        )
    except Company_table.DoesNotExist:
        return redirect("notallowed")


@login_required
@csrf_protect
def view_logs_project_investor(request, pk):
    data = dict()
    mydata = Invested_project_Log.objects.get(pk=pk)
    my_model_instances = mydata.action_data
    get_date = Investor_Wallet_Details.objects.get(investor_id=mydata.investor_code)
    paid_date = get_date.paid_date
    update_date = get_date.updated_date
    context = {
        "my_model_instances": my_model_instances,
        "paid_date": paid_date,
        "update_date": update_date,
    }
    template_name = "admin_dash_menu/pages/logs/project_investor_log_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
