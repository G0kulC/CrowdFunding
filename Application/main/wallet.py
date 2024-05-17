import datetime
from django.shortcuts import render, get_object_or_404, redirect
from Application.models import *
from Application.forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


@login_required
@csrf_protect
def add_money_wallet(request):
    data = dict()
    form = InvestorWalletDetailsForm()
    investor_wallet_save = None
    recived_by = None
    get_investor_data_wallet = None
    if request.method == "POST":
        company_id = request.user
        try:
            get_com_name = Company_table.objects.get(email_id=company_id)
            code = get_com_name.company_code
            cmp_name = get_com_name.company_name
            recived_by = cmp_name
        except Company_table.DoesNotExist:
            get_com_name = Staff.objects.get(username=company_id)
            code = get_com_name.company_code
            cmp_name = get_com_name.company_name
            recived_by = cmp_name

        investor_name = request.POST["investor_name"]
        amount = int(request.POST["amount"])
        mode_of_payment = request.POST["mode_of_payment"]
        payment_id = request.POST["payment_id"]
        payment_given_by = request.POST["payment_given_by"]
        money = int(amount)

        get_investor_data = Investors.objects.get(
            email_id=investor_name, company_code=code, delete_status=False
        )

        try:
            get_investor_data_wallet = Investor_Wallet_Details.objects.get(
                investor_id=get_investor_data.investors_code, delete_status=False
            )
            if get_investor_data_wallet.Second_Approved_by is not None:
                if get_investor_data_wallet is not None:
                    update = Investor_Wallet_Details.objects.filter(
                        pk=get_investor_data_wallet.pk
                    ).update(
                        investor_name=get_investor_data.email_id,
                        amount=money,
                        mode_of_payment=mode_of_payment,
                        payment_id=payment_id,
                        payment_given_by=payment_given_by,
                        payment_receiver_name=recived_by,
                        First_Approved_by=None,
                        First_Approved_date=None,
                        Second_Approved_by=None,
                        Second_Approved_date=None,
                        updated_date=datetime.datetime.now(),
                        status=False,
                    )

                    temp_data = {
                        "company_name": get_investor_data_wallet.company_name,
                        "investor_name": get_investor_data_wallet.investor_name,
                        "amount": get_investor_data_wallet.amount,
                        "total_amount": get_investor_data_wallet.total_amount,
                        "mode_of_payment": get_investor_data_wallet.mode_of_payment,
                        "payment_id": get_investor_data_wallet.payment_id,
                        "payment_given_by": get_investor_data_wallet.payment_given_by,
                        "payment_receiver_name": get_investor_data_wallet.payment_receiver_name,
                        "First_Approved_by": get_investor_data_wallet.First_Approved_by,
                        "First_Approved_date": str(
                            get_investor_data_wallet.First_Approved_date
                        ),
                        "Second_Approved_by": get_investor_data_wallet.Second_Approved_by,
                        "Second_Approved_date": str(
                            get_investor_data_wallet.Second_Approved_date
                        ),
                        "paid_date": str(get_investor_data_wallet.paid_date),
                        "updated_date": str(get_investor_data_wallet.updated_date),
                        "status": get_investor_data_wallet.status,
                    }
                    wallet_log = InvestorsWalletLog.objects.create(
                        company_name=cmp_name,
                        company_code=code,
                        investors_code=get_investor_data.investors_code,
                        investor_name=get_investor_data.email_id,
                        wallet_key=get_investor_data_wallet.wallet_key,
                        ip_address=request.META["REMOTE_ADDR"],
                        action="Updated",
                        action_data=temp_data,
                        user=request.user,
                    )
                    data["form_is_valid"] = True
                    data["add"] = True
            else:
                data["form_is_valid"] = True
                data["pending"] = True
                data["name"] = get_investor_data_wallet.investor_name

        except Investor_Wallet_Details.DoesNotExist:
            if request.method == "POST" and not get_investor_data_wallet is not None:
                investor_wallet_save = Investor_Wallet_Details.objects.create(
                    company_name=cmp_name,
                    company_code=code,
                    investor_id=get_investor_data.investors_code,
                    investor_name=get_investor_data.email_id,
                    amount=amount,
                    mode_of_payment=mode_of_payment,
                    payment_id=payment_id,
                    payment_given_by=payment_given_by,
                    payment_receiver_name=recived_by,
                    total_amount=0,
                    status=False,
                )
                investor_wallet_save.save()

                temp_data = {
                    "company_name": investor_wallet_save.company_name,
                    "investor_name": investor_wallet_save.investor_name,
                    "amount": investor_wallet_save.amount,
                    "total_amount": investor_wallet_save.total_amount,
                    "mode_of_payment": investor_wallet_save.mode_of_payment,
                    "payment_id": investor_wallet_save.payment_id,
                    "payment_given_by": investor_wallet_save.payment_given_by,
                    "payment_receiver_name": investor_wallet_save.payment_receiver_name,
                    "status": investor_wallet_save.status,
                }
                wallet_log = InvestorsWalletLog.objects.create(
                    company_name=cmp_name,
                    company_code=code,
                    investors_code=get_investor_data.investors_code,
                    investor_name=get_investor_data.email_id,
                    wallet_key=investor_wallet_save.wallet_key,
                    ip_address=request.META["REMOTE_ADDR"],
                    action="Created",
                    action_data=temp_data,
                    user=request.user,
                )
                data["form_is_valid"] = True
                data["add"] = True

            books = Investor_Wallet_Details.objects.all()
            data["html_book_list"] = render_to_string(
                "admin_dash_menu/pages/wallet/investors_wallet.html", {"books": books}
            )
    else:
        data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(
        "admin_dash_menu/pages/wallet/addwallet.html", context, request=request
    )
    return JsonResponse(data)


@login_required
@csrf_protect
def investors_wallet(request):
    try:
        s = request.user
        check_inv = Company_table.objects.get(email_id=s)
        code = check_inv.company_code
        name = check_inv.company_name
        my_model_instances = Investor_Wallet_Details.objects.filter(
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
                request, "admin_dash_menu/pages/wallet/investors_wallet.html", context
            )

        else:
            pass
    except Company_table.DoesNotExist:
        check = Staff.objects.get(username=s)
        code = check.company_code
        name = check.company_name
        staf_name = check.username
        my_model_instances1 = Investor_Wallet_Details.objects.filter(company_code=code)
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
                wallet_permissions = get_object_or_404(
                    Investor_wallet_menu, staff_name=s, company_code=code
                )
                pro_inv_permissions = get_object_or_404(
                    Project_investor_menu, staff_name=s, company_code=code
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
                    request,
                    "admin_dash_menu/pages/wallet/investors_wallet.html",
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
def get_company_investors_wallet(request):
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
def get_company_investors_account(request, email):
    if request.user.is_authenticated:
        data = dict()
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
        try:
            get_investor = Investors.objects.get(
                email_id=email, company_code=comp_code, status=True, delete_status=False
            )
        except Investors.DoesNotExist:
            get_investor = None
        if get_investor is not None:
            data["email"] = True
            print("true")
        else:
            print("False")

        return JsonResponse(data)
    else:
        data["error"] = "User is not authenticated"
        return JsonResponse(data)


@login_required
def get_company_investors_account_edit(request, email, pk):
    if request.user.is_authenticated and not request.user.is_superuser:
        data = dict()
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
        try:
            get_investor = Investors.objects.get(
                email_id=email, company_code=comp_code, status=True, delete_status=False
            )
            if get_investor is not None:
                if (get_investor.pk == pk) and (get_investor.email_id == email):
                    data["email"] = False
                else:
                    data["email"] = True

        except Investors.DoesNotExist:
            get_investor = None
            data["email"] = False

        return JsonResponse(data)
    elif request.user.is_superuser:
        data = dict()
        try:
            check = Investors.objects.get(pk=pk)
            adm_vestor = Investors.objects.get(
                email_id=email,
                company_code=check.company_code,
                status=True,
                delete_status=False,
            )
            if adm_vestor is not None:
                if (adm_vestor.pk == pk) and (adm_vestor.email_id == email):
                    data["email"] = False
                else:
                    data["email"] = True

        except Investors.DoesNotExist:
            adm_vestor = None
            data["email"] = False

        return JsonResponse(data)

    else:
        data["error"] = "User is not authenticated"
        return JsonResponse(data)


@login_required
@csrf_protect
def view_investor_wallet(request, pk):
    data = dict()
    total_insesment_invstor = 0
    context = None
    my_model_instances = get_object_or_404(Investor_Wallet_Details, pk=pk)
    investor_value_invesment = Investor_Wallet_Details.objects.filter(
        investor_id=my_model_instances.investor_id
    ).latest("paid_date")
    context = {
        "my_model_instances": my_model_instances,
        "total_insesment_invstor": investor_value_invesment.total_amount,
    }

    template_name = "admin_dash_menu/pages/wallet/view_wallet.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def get_investor_wallet_blance(request, investor_name):
    data = dict()
    total_insesment_invstor = None
    try:
        current_company = Company_table.objects.get(email_id=request.user)
    except Company_table.DoesNotExist:
        current_company = None
        staff_check = Staff.objects.get(username=request.user)
        current_company = Company_table.objects.get(
            company_code=staff_check.company_code
        )
    try:
        investor_value_invesment = Investor_Wallet_Details.objects.get(
            investor_name=investor_name,
            company_code=current_company.company_code,
            delete_status=False,
        )
        total_insesment_invstor = investor_value_invesment.total_amount
        if total_insesment_invstor <= 0:
            total_insesment_invstor = 0
            data["not_found"] = True
        else:
            data["total_insesment_invstor"] = total_insesment_invstor
            data["not_found"] = False

    except Investor_Wallet_Details.DoesNotExist:
        total_insesment_invstor = 0
        data["not_found"] = True
    return JsonResponse(data)


@login_required
@csrf_protect
def get_project_per_share_value(request, project_name):
    data = dict()
    try:
        current_company = Company_table.objects.get(
            email_id=request.user, delete_status=False
        )
    except Company_table.DoesNotExist:
        current_company = None
        staff_check = Staff.objects.get(username=request.user)
        current_company = Company_table.objects.get(
            company_code=staff_check.company_code
        )
    comp_name = current_company.company_name
    comp_code = current_company.company_code
    get_value = Project.objects.get(
        project_name=project_name, company_code=comp_code, delete_status=False
    )
    share_value = get_value.Per_share_value
    share_count = get_value.share_count

    data["share_value"] = share_value
    data["share_count"] = share_count

    return JsonResponse(data)


@login_required
@csrf_protect
def get_project_unit_value(request, project_name):
    data = dict()
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

    get_value = Project.objects.get(
        project_name=project_name,
        company_code=comp_code,
        status=True,
        delete_status=False,
    )
    given_unit = int(get_value.Returns_projection_type)
    given_value = int(get_value.Returns_projection_value)
    data["unit_value"] = given_value
    data["unit_count"] = given_unit

    return JsonResponse(data)


@login_required
@csrf_protect
def investors_wallet_permission(request, pk):
    book = get_object_or_404(Investor_Wallet_Details, pk=pk)
    data = dict()
    hidden_field = None
    total_insesment_invstor = 0
    try:
        get_com_name = Company_table.objects.get(
            email_id=request.user, delete_status=False
        )
        first_company = book.First_Approved_by == get_com_name.email_id
        if first_company:
            hidden_field = True
    except Company_table.DoesNotExist:
        hidden_field = None
        get_staff_name = Staff.objects.get(username=request.user, delete_status=False)
        first_staff = book.First_Approved_by == get_staff_name.username
        if first_staff:
            hidden_field = True
    if request.method == "POST":
        update_approvel = Investor_Wallet_Details.objects.get(pk=pk)
        if update_approvel is not None:
            first = update_approvel.First_Approved_by
            if first is None:
                First_Approved_by = request.POST["First_Approved_by"]
                First_Approved_date = request.POST["First_Approved_date_add"]

                update = Investor_Wallet_Details.objects.filter(pk=pk).update(
                    First_Approved_by=First_Approved_by,
                    First_Approved_date=First_Approved_date,
                )
                updated_data_first = Investor_Wallet_Details.objects.get(pk=pk)
                temp_data = {
                    "company_name": updated_data_first.company_name,
                    "investor_name": updated_data_first.investor_name,
                    "amount": updated_data_first.amount,
                    "total_amount": updated_data_first.total_amount,
                    "mode_of_payment": updated_data_first.mode_of_payment,
                    "payment_id": updated_data_first.payment_id,
                    "payment_given_by": updated_data_first.payment_given_by,
                    "payment_receiver_name": updated_data_first.payment_receiver_name,
                    "First_Approved_by": updated_data_first.First_Approved_by,
                    "First_Approved_date": str(updated_data_first.First_Approved_date),
                    "Second_Approved_by": updated_data_first.Second_Approved_by,
                    "Second_Approved_date": str(
                        updated_data_first.Second_Approved_date
                    ),
                    "paid_date": str(updated_data_first.paid_date),
                    "updated_date": str(updated_data_first.updated_date),
                    "status": updated_data_first.status,
                }
                wallet_log = InvestorsWalletLog.objects.create(
                    company_name=updated_data_first.company_name,
                    company_code=updated_data_first.company_code,
                    investors_code=updated_data_first.investor_id,
                    investor_name=updated_data_first.investor_name,
                    wallet_key=updated_data_first.wallet_key,
                    ip_address=request.META["REMOTE_ADDR"],
                    action="Approved",
                    action_data=temp_data,
                    user=request.user,
                )

                data["update1"] = True

            elif (
                first is not None
                and first != request.user
                and update_approvel is not None
            ):
                Second_Approved_by = request.POST["Second_Approved_by"]
                Second_Approved_date = request.POST["Second_Approved_date_add"]

                update = Investor_Wallet_Details.objects.filter(pk=pk).update(
                    Second_Approved_by=Second_Approved_by,
                    Second_Approved_date=Second_Approved_date,
                    total_amount=int(update_approvel.total_amount)
                    + int(update_approvel.amount),
                    status=True,
                )
                updated_data_second = Investor_Wallet_Details.objects.get(pk=pk)
                temp_data = {
                    "company_name": updated_data_second.company_name,
                    "investor_name": updated_data_second.investor_name,
                    "amount": updated_data_second.amount,
                    "total_amount": updated_data_second.total_amount,
                    "mode_of_payment": updated_data_second.mode_of_payment,
                    "payment_id": updated_data_second.payment_id,
                    "payment_given_by": updated_data_second.payment_given_by,
                    "payment_receiver_name": updated_data_second.payment_receiver_name,
                    "First_Approved_by": updated_data_second.First_Approved_by,
                    "First_Approved_date": str(updated_data_second.First_Approved_date),
                    "Second_Approved_by": updated_data_second.Second_Approved_by,
                    "Second_Approved_date": str(
                        updated_data_second.Second_Approved_date
                    ),
                    "paid_date": str(updated_data_second.paid_date),
                    "updated_date": str(updated_data_second.updated_date),
                    "status": updated_data_second.status,
                }
                wallet_log = InvestorsWalletLog.objects.create(
                    company_name=updated_data_second.company_name,
                    company_code=updated_data_second.company_code,
                    investors_code=updated_data_second.investor_id,
                    investor_name=updated_data_second.investor_name,
                    wallet_key=updated_data_second.wallet_key,
                    ip_address=request.META["REMOTE_ADDR"],
                    action="Approved",
                    action_data=temp_data,
                    user=request.user,
                )
                wallet_history = Investor_Wallet_History_Details.objects.create(
                    investor_name=updated_data_second.investor_name,
                    reason="Money Added to Wallet",
                    credited_amount=updated_data_second.amount,
                    wallet_key=updated_data_second.wallet_key,
                    credited_time=datetime.datetime.now(),
                    debited_amount=0,
                    debited_date=datetime.datetime.now(),
                    total_amount=updated_data_second.total_amount,
                )
                wallet_history.save()
                data["update2"] = True

        data["form_is_valid"] = True
        books = Investor_Wallet_Details.objects.all()
        data["html_book_list"] = render_to_string(
            "admin_dash_menu/pages/wallet/investors_wallet.html", {"books": books}
        )

        form = InvestorWalletDetailsForm(request.POST, instance=book)
    else:
        form = InvestorWalletDetailsForm(instance=book)
        data["form_is_valid"] = False

    context = {"form": form, "hidden_field": hidden_field}
    template_name = "admin_dash_menu/pages/wallet/wallet_permission.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def detele_investors_wallet(request, pk):
    mymodel = get_object_or_404(Investor_Wallet_Details, pk=pk)
    trashed_data = TrashedData.objects.create(
        user=request.user,
        original_data=mymodel.__dict__,
    )
    check_wallet = Invesments_Db.objects.filter(investor_code=mymodel.investor_id)
    if check_wallet.exists():
        context = {"error": "☹ Investor has started Invesment,So you can not delete!"}
        return JsonResponse(context, status=400)
    elif not check_wallet.exists():
        mymodel.delete()
        return JsonResponse({"status": "ok"})


# ------------------------              LOGS                -------------------------------->


@login_required
@csrf_protect
def company_logs_wallet(request):
    s = request.user
    try:
        check_com = Company_table.objects.get(email_id=s, delete_status=False)
        code = check_com.company_code
        name = check_com.company_name
        sts = "Admin"
        proj_log = InvestorsWalletLog.objects.filter(company_code=code)
        if request.method == "POST":
            from_date = request.POST["from_date"]
            to_date = request.POST["to_date"]
            name = request.POST["name"]
            checkuser = User.objects.get(username=name)
            proj_log = InvestorsWalletLog.objects.filter(
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
        return render(request, "admin_dash_menu/pages/logs/wallet_log.html", context)
    except Company_table.DoesNotExist:
        return redirect("notallowed")


@login_required
@csrf_protect
def view_logs_wallet(request, pk):
    data = dict()
    mydata = InvestorsWalletLog.objects.get(pk=pk)
    my_model_instances = mydata.action_data
    get_date = Investor_Wallet_Details.objects.get(investor_id=mydata.investors_code)
    paid_date = get_date.paid_date
    update_date = get_date.updated_date
    context = {
        "my_model_instances": my_model_instances,
        "paid_date": paid_date,
        "update_date": update_date,
    }
    template_name = "admin_dash_menu/pages/logs/wallet_log_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
