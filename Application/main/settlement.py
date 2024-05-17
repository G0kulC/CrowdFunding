from django.shortcuts import render, get_object_or_404, redirect
from Application.models import *
from Application.forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Sum
from django.db.models import Count


@login_required
@csrf_protect
def project_settlement_create(request):
    data = dict()
    form = Project_settlement_Form()
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
        investor_name = request.POST["investor_name"]
        project_name = request.POST["project"]
        Settlement_blance = int(request.POST["Settlement_blance"])
        amount = int(request.POST["amount"])
        get = Project.objects.get(prject_key=project_name, company_code=code)
        get_wallet = Investor_Wallet_Details.objects.get(
            investor_id=investor_name, company_code=code
        )

        get_last_settlement = Projectsettlement.objects.filter(
            project_code=project_name, investor_code=investor_name, company_code=code
        )
        if get_last_settlement.count() == 0:
            avalable_profit = Settlement_blance - amount

            settlement_crete = Projectsettlement.objects.create(
                company_code=code,
                company_name=cmp_name,
                investor_name=get_wallet.investor_name,
                investor_code=investor_name,
                project_name=get.project_name,
                project_code=get.prject_key,
                wallet_key=get_wallet.wallet_key,
                amount=amount,
                blance_amount=avalable_profit,
                status=False,
            )
            settlement_crete.save()
            temp_data = {
                "company_name": settlement_crete.company_name,
                "investor_name": settlement_crete.investor_name,
                "project_name": settlement_crete.project_name,
                "amount": settlement_crete.amount,
                "blance_amount": settlement_crete.blance_amount,
                "settlement_date": str(
                    settlement_crete.settlement_date.strftime("%d-%m-%Y")
                ),
                "status": False,
            }
            create_log = settlement_log.objects.create(
                company_name=settlement_crete.company_name,
                company_code=settlement_crete.company_code,
                investor_code=settlement_crete.investor_code,
                wallet_key=settlement_crete.wallet_key,
                ip_address=request.META["REMOTE_ADDR"],
                action="Created",
                action_data=temp_data,
                user=request.user,
            )
            data["form_is_valid"] = True
            data["add"] = True
            books = Projectsettlement.objects.all()
            data["html_book_list"] = render_to_string(
                "admin_dash_menu/pages/settlement/settlement.html", {"books": books}
            )
        elif get_last_settlement.count() > 0:
            check_Exits = Projectsettlement.objects.filter(
                project_code=project_name,
                investor_code=investor_name,
                company_code=code,
            ).latest("id")
            if check_Exits.status == True:
                settlement_crete_last = Projectsettlement.objects.filter(
                    project_code=project_name,
                    investor_code=investor_name,
                    company_code=code,
                ).latest("id")
                if settlement_crete_last is not None:
                    settlement_crete = Projectsettlement.objects.create(
                        company_code=code,
                        company_name=cmp_name,
                        investor_name=get_wallet.investor_name,
                        investor_code=investor_name,
                        project_name=get.project_name,
                        project_code=get.prject_key,
                        wallet_key=get_wallet.wallet_key,
                        amount=amount,
                        blance_amount=Settlement_blance,
                        status=False,
                    )
                    settlement_crete.save()
                    temp_data = {
                        "company_name": cmp_name,
                        "investor_name": settlement_crete.investor_name,
                        "project_name": settlement_crete.project_name,
                        "amount": settlement_crete.amount,
                        "blance_amount": settlement_crete.blance_amount,
                        "settlement_date": str(
                            settlement_crete.settlement_date.strftime("%d-%m-%Y")
                        ),
                        "status": False,
                    }
                    create_log = settlement_log.objects.create(
                        company_name=settlement_crete.company_name,
                        company_code=settlement_crete.company_code,
                        investor_code=settlement_crete.investor_code,
                        wallet_key=settlement_crete.wallet_key,
                        ip_address=request.META["REMOTE_ADDR"],
                        action="Created",
                        action_data=temp_data,
                        user=request.user,
                    )
                data["form_is_valid"] = True
                data["add"] = True
                books = Projectsettlement.objects.all()
                data["html_book_list"] = render_to_string(
                    "admin_dash_menu/pages/settlement/settlement.html", {"books": books}
                )

            else:
                data["pending"] = True

    else:
        data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(
        "admin_dash_menu/pages/settlement/settlement_reg.html", context, request=request
    )
    return JsonResponse(data)


@login_required
def get_company_setletment_investors(request):
    if request.user.is_authenticated:
        try:
            current_company = Company_table.objects.get(email_id=request.user)
        except Company_table.DoesNotExist:
            current_company = Staff.objects.get(username=request.user)
        comp_name = current_company.company_name
        comp_code = current_company.company_code
        current_projects = Investors.objects.filter(company_code=comp_code, status=True)
        project_list = [
            {"id": p.investors_code, "name": p.email_id} for p in current_projects
        ]
        return JsonResponse({"projects": project_list})
    else:
        return JsonResponse({"error": "User is not authenticated"})


@login_required
def get_company_setletment_project(request, inves_id):
    if request.user.is_authenticated:
        try:
            current_company = Company_table.objects.get(email_id=request.user)
        except Company_table.DoesNotExist:
            current_company = Staff.objects.get(username=request.user)
        comp_name = current_company.company_name
        comp_code = current_company.company_code
        current_projects = Invesments_Db.objects.filter(
            company_code=comp_code, status=True, investor_code=inves_id
        )
        project_list = [
            {"id": p.project_code, "project_name": p.project} for p in current_projects
        ]
        return JsonResponse({"projects": project_list})
    else:
        return JsonResponse({"error": "User is not authenticated"})


@login_required
@csrf_protect
def get_company_setletment_invested_amount(request, inves_id, proj_id):
    data = dict()
    get_project_main = Project.objects.get(prject_key=proj_id)
    main_total_share = int(get_project_main.Total_share)
    profit_amount = 0
    try:
        get_project = Invesments_Db.objects.filter(
            investor_code=inves_id,
            project_code=proj_id,
            Second_Approved_by__isnull=False,
        ).latest("id")
        get_investor = Invesments_Db.objects.filter(
            investor_code=get_project.investor_code,
            company_code=get_project.company_code,
            project=get_project.project,
            status=True,
        )
        get_invested_amount = int(get_investor.aggregate(Sum("amount"))["amount__sum"])

        get_unit_buy = int(
            get_investor.aggregate(Sum("investor_share_count"))[
                "investor_share_count__sum"
            ]
        )
        total_invesment = Invesments_Db.objects.filter(
            company_code=get_project.company_code,
            project=get_project.project,
            status=True,
        )
        totale_investor_value = int(
            total_invesment.aggregate(Sum("amount"))["amount__sum"]
        )

        if main_total_share == totale_investor_value:
            try:
                check_exp = ProjectExpense.objects.filter(
                    project_code=get_project_main.prject_key
                ).latest("id")
                get_exp = ProjectExpense.objects.filter(
                    project_code=get_project_main.prject_key,
                    Second_Approved_by__isnull=False,
                )
                total_expense = get_exp.aggregate(Sum("amount"))["amount__sum"]
            except ProjectExpense.DoesNotExist:
                expense_count = 0
                total_expense = 0
            try:
                check_sale = ProjectSales.objects.filter(
                    project_code=get_project_main.prject_key
                ).latest("id")
                get_sale = ProjectSales.objects.filter(
                    project_code=get_project_main.prject_key,
                    Second_Approved_by__isnull=False,
                )
                total_sale = get_sale.aggregate(Sum("amount"))["amount__sum"]
            except ProjectSales.DoesNotExist:
                sale_count = 0
                total_sale = 0
                total_unit_sale = 0
            temp_profit_1 = total_sale - totale_investor_value
            company_share = 0
            unused_exp = 0
            if total_expense > get_project_main.Other_expense:
                company_share = int(total_expense - get_project_main.Other_expense)
                temp_profit_1 = temp_profit_1 - company_share
            elif total_expense < get_project_main.Other_expense:
                unused_share = int(get_project_main.Other_expense - total_expense)
                investor_count_get = (
                    Invesments_Db.objects.filter(
                        project_code=get_project_main.prject_key
                    )
                    .values("investor_name")
                    .annotate(count=Count("investor_name"))
                    .count()
                )
                unused_exp = unused_share / investor_count_get
            else:
                company_share = 0
                temp_profit_1 = temp_profit_1
            real_profit = (get_invested_amount / totale_investor_value) * temp_profit_1
            if unused_exp > 0:
                real_profit = real_profit + unused_exp
            profit_amount = int(real_profit)

        if main_total_share == totale_investor_value + 1:
            try:
                check_exp = ProjectExpense.objects.filter(
                    project_code=get_project_main.prject_key
                ).latest("id")
                get_exp = ProjectExpense.objects.filter(
                    project_code=get_project_main.prject_key,
                    Second_Approved_by__isnull=False,
                )
                total_expense = get_exp.aggregate(Sum("amount"))["amount__sum"]
            except ProjectExpense.DoesNotExist:
                expense_count = 0
                total_expense = 0
            try:
                check_sale = ProjectSales.objects.filter(
                    project_code=get_project_main.prject_key
                ).latest("id")
                get_sale = ProjectSales.objects.filter(
                    project_code=get_project_main.prject_key,
                    Second_Approved_by__isnull=False,
                )
                total_sale = get_sale.aggregate(Sum("amount"))["amount__sum"]
            except ProjectSales.DoesNotExist:
                sale_count = 0
                total_sale = 0
                total_unit_sale = 0
            temp_profit_1 = total_sale - totale_investor_value
            company_share = 0
            unused_exp = 0
            if total_expense > get_project_main.Other_expense:
                company_share = int(total_expense - get_project_main.Other_expense)
                temp_profit_1 = temp_profit_1 - company_share
            elif total_expense < get_project_main.Other_expense:
                unused_share = int(get_project_main.Other_expense - total_expense)
                investor_count_get = (
                    Invesments_Db.objects.filter(
                        project_code=get_project_main.prject_key
                    )
                    .values("investor_name")
                    .annotate(count=Count("investor_name"))
                    .count()
                )
                unused_exp = unused_share / investor_count_get
            else:
                company_share = 0
                temp_profit_1 = temp_profit_1
            real_profit = (get_invested_amount / totale_investor_value) * temp_profit_1
            print("real_profit", real_profit)
            print("get_invested_amount", get_invested_amount)
            print("totale_investor_value", totale_investor_value)
            print("temp_profit_1", temp_profit_1)

            if unused_exp > 0:
                real_profit = real_profit + unused_exp
            profit_amount = int(real_profit)

    except Invesments_Db.DoesNotExist:
        get_invested_amount = 0
        get_Settlement_blance = 0
        get_unit_buy = 0
        profit_amount = 0
        totale_investor_value = 0

    setment_blc = 0
    get_Settlement_blance = Projectsettlement.objects.filter(
        investor_code=inves_id,
        company_code=get_project_main.company_code,
        project_code=proj_id,
        status=True,
    )
    if get_Settlement_blance.count() > 0:
        setment_blc = get_Settlement_blance.aggregate(Sum("amount"))["amount__sum"]
        avalible_amount = int(profit_amount + get_invested_amount - setment_blc)
        setment_blc = avalible_amount
    else:
        setment_blc = int(profit_amount + get_invested_amount)

    data["get_invested_amount"] = get_invested_amount
    data["setment_blc"] = setment_blc
    data["get_unit_buy"] = get_unit_buy
    data["totale_investor_value"] = totale_investor_value
    data["profit_amount"] = profit_amount

    return JsonResponse(data)


@login_required
@csrf_protect
def project_settlement_list(request):
    try:
        s = request.user
        check_inv = Company_table.objects.get(email_id=s)
        code = check_inv.company_code
        name = check_inv.company_name
        my_model_instances = Projectsettlement.objects.filter(company_code=code)
        sts = "Admin"
        if check_inv is not None:
            context = {
                "my_model_instances": my_model_instances,
                "name": name,
                "satus": sts,
                "company": name,
            }
            return render(
                request, "admin_dash_menu/pages/settlement/settlement.html", context
            )

        else:
            pass
    except Company_table.DoesNotExist:
        check = Staff.objects.get(username=s)
        code = check.company_code
        name = check.company_name
        staf_name = check.username
        my_model_instances1 = Projectsettlement.objects.filter(company_code=code)
        proj_inv_per = Project_settlement_menu.objects.get(
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
                    request, "admin_dash_menu/pages/settlement/settlement.html", context
                )
            else:
                return redirect("notallowed")
        else:
            return redirect("notallowed")

    else:
        return redirect("notallowed")


@login_required
@csrf_protect
def save_Project_settlement_Form(request, form, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            books = Projectsettlement.objects.all()
            data["html_book_list"] = render_to_string(
                "admin_dash_menu/pages/settlement/settlement.html", {"books": books}
            )
        else:
            data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def view_project_settlement(request, pk):
    my_model_instances = get_object_or_404(Projectsettlement, pk=pk)
    data = dict()
    context = {"my_model_instances": my_model_instances}
    template_name = "admin_dash_menu/pages/settlement/settlement_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def project_settlement_update(request, pk):
    book = get_object_or_404(Projectsettlement, pk=pk)
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
        update_approvel = Projectsettlement.objects.get(pk=pk)
        if update_approvel is not None:
            first = update_approvel.First_Approved_by
            second = update_approvel.Second_Approved_by
            if first is None:
                First_Approved_by = request.POST["First_Approved_by"]
                First_Approved_date = request.POST["First_Approved_date_add"]
                update = Projectsettlement.objects.filter(pk=pk).update(
                    First_Approved_by=First_Approved_by,
                    First_Approved_date=First_Approved_date,
                )
                temp_data = {
                    "company_name": update_approvel.company_name,
                    "investor_name": update_approvel.investor_name,
                    "project_name": update_approvel.project_name,
                    "amount": update_approvel.amount,
                    "blance_amount": update_approvel.blance_amount,
                    "First_Approved_by": First_Approved_by,
                    "First_Approved_date": str(First_Approved_date),
                    "settlement_date": str(
                        update_approvel.settlement_date.strftime("%d-%m-%Y")
                    ),
                    "status": False,
                }
                create_log = settlement_log.objects.create(
                    company_name=update_approvel.company_name,
                    company_code=update_approvel.company_code,
                    investor_code=update_approvel.investor_code,
                    wallet_key=update_approvel.wallet_key,
                    ip_address=request.META["REMOTE_ADDR"],
                    action="Approved",
                    action_data=temp_data,
                    user=request.user,
                )
                data["update1"] = True
            elif second is None and first is not None and first != request.user:
                Second_Approved_by = request.POST["Second_Approved_by"]
                Second_Approved_date = request.POST["Second_Approved_date_add"]
                update = Projectsettlement.objects.filter(pk=pk).update(
                    Second_Approved_by=Second_Approved_by,
                    Second_Approved_date=Second_Approved_date,
                    status=True,
                )
                temp_data = {
                    "company_name": update_approvel.company_name,
                    "investor_name": update_approvel.investor_name,
                    "project_name": update_approvel.project_name,
                    "amount": update_approvel.amount,
                    "blance_amount": update_approvel.blance_amount,
                    "First_Approved_by": update_approvel.First_Approved_by,
                    "First_Approved_date": str(update_approvel.First_Approved_date),
                    "Second_Approved_by": Second_Approved_by,
                    "Second_Approved_date": str(Second_Approved_date),
                    "settlement_date": str(
                        update_approvel.settlement_date.strftime("%d-%m-%Y")
                    ),
                    "status": True,
                }
                create_log = settlement_log.objects.create(
                    company_name=update_approvel.company_name,
                    company_code=update_approvel.company_code,
                    investor_code=update_approvel.investor_code,
                    wallet_key=update_approvel.wallet_key,
                    ip_address=request.META["REMOTE_ADDR"],
                    action="Approved",
                    action_data=temp_data,
                    user=request.user,
                )

                add_wallet = Investor_Wallet_Details.objects.get(
                    investor_id=update_approvel.investor_code,
                    company_code=update_approvel.company_code,
                )
                add_wallet.total_amount = (
                    add_wallet.total_amount + update_approvel.amount
                )
                add_wallet.save()
                wallet_history = Investor_Wallet_History_Details.objects.create(
                    investor_name=add_wallet.investor_name,
                    reason="Settled Profit",
                    credited_amount=update_approvel.amount,
                    wallet_key=add_wallet.wallet_key,
                    credited_time=datetime.datetime.now(),
                    debited_amount=0,
                    debited_date=datetime.datetime.now(),
                    total_amount=add_wallet.total_amount,
                )
                wallet_history.save()

                data["update2"] = True

        data["form_is_valid"] = True
        books = Projectsettlement.objects.all()
        data["html_book_list"] = render_to_string(
            "admin_dash_menu/pages/settlement/settlement.html", {"books": books}
        )
        form = Project_settlement_Form(request.POST, instance=book)
    else:
        form = Project_settlement_Form(instance=book)
        data["form_is_valid"] = False

    context = {"form": form, "hidden_field": hidden_field, "company": company}
    data["html_form"] = render_to_string(
        "admin_dash_menu/pages/settlement/settlement_edit.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@login_required
@csrf_protect
def delete_project_settlement(request, pk):
    mymodel = get_object_or_404(Projectsettlement, pk=pk)
    trashed_data = TrashedData.objects.create(
        user=request.user,
        original_data=mymodel.__dict__,
    )
    if mymodel.status == True:
        temp_data = {
            "company_name": mymodel.company_name,
            "investor_name": mymodel.investor_name,
            "project_name": mymodel.project_name,
            "amount": mymodel.amount,
            "blance_amount": mymodel.blance_amount,
            "First_Approved_by": mymodel.First_Approved_by,
            "First_Approved_date": str(mymodel.First_Approved_date),
            "Second_Approved_by": mymodel.Second_Approved_by,
            "Second_Approved_date": str(mymodel.Second_Approved_date),
            "settlement_date": str(mymodel.settlement_date.strftime("%d-%m-%Y")),
            "status": False,
        }
        create_log = settlement_log.objects.create(
            company_name=mymodel.company_name,
            company_code=mymodel.company_code,
            investor_code=mymodel.investor_code,
            wallet_key=mymodel.wallet_key,
            ip_address=request.META["REMOTE_ADDR"],
            action="Deleted",
            action_data=temp_data,
            user=request.user,
        )
        add_wallet = Investor_Wallet_Details.objects.get(
            investor_id=mymodel.investor_code, company_code=mymodel.company_code
        )
        add_wallet.total_amount = add_wallet.total_amount - mymodel.amount
        add_wallet.save()
        wallet_history = Investor_Wallet_History_Details.objects.create(
            investor_name=add_wallet.investor_name,
            reason="deleted Profit",
            credited_amount=0,
            wallet_key=add_wallet.wallet_key,
            credited_time=datetime.datetime.now(),
            debited_amount=add_wallet.amount,
            debited_date=datetime.datetime.now(),
            total_amount=add_wallet.total_amount,
        )
        wallet_history.save()
    mymodel.delete()
    return JsonResponse({"status": "ok"})


# ------------------------              LOGS                -------------------------------->


@login_required
@csrf_protect
def company_logs_settlement(request):
    s = request.user
    try:
        check_com = Company_table.objects.get(email_id=s, delete_status=False)
        code = check_com.company_code
        name = check_com.company_name
        sts = "Admin"
        proj_log = settlement_log.objects.filter(company_code=code)
        if request.method == "POST":
            from_date = request.POST["from_date"]
            to_date = request.POST["to_date"]
            name = request.POST["name"]
            checkuser = User.objects.get(username=name)
            proj_log = settlement_log.objects.filter(
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
            request, "admin_dash_menu/pages/logs/settlement_log.html", context
        )
    except Company_table.DoesNotExist:
        return redirect("notallowed")


@login_required
@csrf_protect
def view_logs_settlement(request, pk):
    data = dict()
    mydata = settlement_log.objects.get(pk=pk)
    my_model_instances = mydata.action_data
    context = {
        "my_model_instances": my_model_instances,
    }
    template_name = "admin_dash_menu/pages/logs/settlement_log_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
