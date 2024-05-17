from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count
from Application.models import *
from django.db.models import Sum


def admin_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["admin_login_username"]
            password = request.POST["admin_login_pass"]
            admin = authenticate(request, username=username, password=password)
            if admin is not None:
                try:
                    active = Company_table.objects.get(email_id=username)
                    checkactive = active.status

                    if admin is not None and checkactive == 1:
                        login(request, admin)
                        return JsonResponse({"success": "/dashbord"})
                    else:
                        return JsonResponse(
                            {"success": False, "error": "Account Not Activate!"}
                        )
                except Company_table.DoesNotExist:
                    pass
                try:
                    active_investor = None
                    active_investors1 = Investors.objects.filter(
                        email_id=username, status=True
                    )
                    if active_investors1.count() > 1:
                        active_investor = active_investors1.first()
                    else:
                        active_investor = None
                        active_investor = Investors.objects.get(
                            email_id=username, status=True
                        )

                    if admin is not None and active_investor is not None:
                        login(request, admin)
                        return JsonResponse({"success": "/Dashboard"})
                    else:
                        return JsonResponse({"error": "Account Not Activate!"})
                except Investors.DoesNotExist:
                    pass
                try:
                    checkactive_staff = Staff.objects.get(username=username)
                    is_active_staff = checkactive_staff.satus
                    if admin is not None and is_active_staff == 1:
                        check_dashboard = Dashbord_view.objects.get(
                            staff_name=checkactive_staff.username
                        )
                        if check_dashboard.status == 1:
                            login(request, admin)
                            return JsonResponse({"success": "/dashbord"})
                        else:
                            return JsonResponse({"error": "Permission Not Activate!"})
                    else:
                        return JsonResponse({"error": "Account Not Activate!"})
                except Staff.DoesNotExist:
                    pass
                if admin is not None and admin.is_superuser:
                    login(request, admin)
                    return JsonResponse({"success": "/dashbord"})

            return JsonResponse({"error": "Invalid credentials"})
        else:
            return render(
                request=request, template_name="admin_dash_menu/auth/admin_login.html"
            )
    else:
        active_user = None
        active_user = Investors.objects.filter(email_id=request.user)
        if active_user.exists():
            return redirect("empty_dashboard")
        else:
            return redirect("base")


@login_required
def admim_logout(request):
    response = redirect("admin_login")
    logout(request)
    return response


@login_required
@csrf_protect
def admin_dash(request):
    a = request.user.is_authenticated
    if a == 1:
        s = request.user

        try:
            active = Company_table.objects.get(email_id=s)
            checkactive = active.company_name
            s = checkactive
            sts = "Admin"
            context = None

            if active is not None:
                try:
                    project_value = Project.objects.filter(
                        company_code=active.company_code, delete_status=False
                    )
                    total_project_value = project_value.aggregate(Sum("Total_share"))[
                        "Total_share__sum"
                    ]

                    new_projects = Project.objects.filter(
                        company_code=active.company_code, delete_status=False
                    ).order_by("-id")[:5]

                    investor_value = Invesments_Db.objects.filter(
                        company_code=active.company_code
                    )
                    totale_investor_value = int(
                        investor_value.aggregate(Sum("amount"))["amount__sum"]
                    )

                    Expenses = ProjectExpense.objects.filter(
                        company_code=active.company_code
                    )
                    total_Expenses = Expenses.aggregate(Sum("amount"))["amount__sum"]

                    projects = ProjectSales.objects.filter(
                        company_code=active.company_code
                    )
                    total_sales = projects.aggregate(Sum("amount"))["amount__sum"]
                    ext_otr_expense = project_value.aggregate(Sum("Other_expense"))[
                        "Other_expense__sum"
                    ]
                    comapny_expense = 0
                    unused_share = 0
                    if total_Expenses > ext_otr_expense:
                        comapny_expense = int(total_Expenses - ext_otr_expense)
                    elif total_Expenses < ext_otr_expense:
                        unused_share = int(ext_otr_expense - total_Expenses)
                    else:
                        comapny_expense = 0
                    temp_profit = int(total_sales - totale_investor_value)
                    if unused_share > 0 and comapny_expense <= 0:
                        total_profit = int(temp_profit + unused_share)
                    else:
                        total_profit = int(temp_profit - comapny_expense)

                    list_sales = ProjectSales.objects.filter(
                        company_code=active.company_code
                    ).order_by("-id")[:4]
                    sales_count = ProjectSales.objects.filter(
                        company_code=active.company_code
                    ).count()
                    card_exp_list = ProjectExpense.objects.filter(
                        company_code=active.company_code
                    ).order_by("-id")[:6]

                    card_invesment_list = Investor_Wallet_Details.objects.filter(
                        company_code=active.company_code
                    ).order_by("-id")[:6]

                    profit_persentage = None

                    try:
                        profit_persentage = (total_profit / totale_investor_value) * 100
                        get_profit_percentage = "{:.2f}%".format(profit_persentage)
                        if get_profit_percentage != "":
                            company_dash = True

                            context = {
                                "name": s,
                                "satus": sts,
                                "company": checkactive,
                                "total_profit": total_profit,
                                "total_sales": total_sales,
                                "list_sales": list_sales,
                                "sales_count": sales_count,
                                "card_invesment_list": card_invesment_list,
                                "card_exp_list": card_exp_list,
                                "new_projects": new_projects,
                                "total_Expenses": total_Expenses,
                                "totale_investor_value": totale_investor_value,
                                "get_profit_percentage": get_profit_percentage,
                                "total_project_value": total_project_value,
                                "company_dashboard": company_dash,
                            }
                    except:
                        if project_value.exists():
                            context = {
                                "name": s,
                                "satus": sts,
                                "company": checkactive,
                                "total_sales": total_sales,
                                "list_sales": list_sales,
                                "card_exp_list": card_exp_list,
                                "card_invesment_list": card_invesment_list,
                                "sales_count": sales_count,
                                "total_profit": total_profit,
                                "new_projects": new_projects,
                                "total_Expenses": total_Expenses,
                                "totale_investor_value": totale_investor_value,
                                "total_project_value": total_project_value,
                            }

                    if not project_value.exists():
                        context = {
                            "name": s,
                            "satus": sts,
                            "company": checkactive,
                        }

                except:
                    context = None
                    context = {
                        "name": s,
                        "satus": sts,
                        "company": checkactive,
                    }
            else:
                pass

        except Company_table.DoesNotExist:
            pass

        try:
            checkactive_Staff = Staff.objects.get(username=s)
            staff_comapny = checkactive_Staff.company_name
            staff_comapny_code = checkactive_Staff.company_code
            s = checkactive_Staff.username
            sts = "Staff"
            staff = s
            dashbord_permissions = get_object_or_404(
                Dashbord_view, staff_name=s, company_code=staff_comapny_code
            )
            project_permissions = get_object_or_404(
                Project_menu, staff_name=s, company_code=staff_comapny_code
            )
            wallet_permissions = get_object_or_404(
                Investor_wallet_menu, staff_name=s, company_code=staff_comapny_code
            )
            investor_permissions = get_object_or_404(
                Investor_menu, staff_name=s, company_code=staff_comapny_code
            )
            pro_inv_permissions = get_object_or_404(
                Project_investor_menu, staff_name=s, company_code=staff_comapny_code
            )
            pro_exp_permissions = get_object_or_404(
                Project_Exp_menu, staff_name=s, company_code=staff_comapny_code
            )
            pro_profit_permissions = get_object_or_404(
                Project_Profit_menu, staff_name=s, company_code=staff_comapny_code
            )
            settlement_permissions = get_object_or_404(
                Project_settlement_menu, staff_name=s, company_code=staff_comapny_code
            )
            Reports_permissions = get_object_or_404(
                Report_view, staff_name=s, company_code=staff_comapny_code
            )
            if dashbord_permissions.view:
                if checkactive_Staff is not None:
                    active = Company_table.objects.get(company_code=staff_comapny_code)
                    if active is not None:
                        sales_count = ProjectSales.objects.filter(
                            company_code=active.company_code
                        ).count()
                        list_sales = ProjectSales.objects.filter(
                            company_code=active.company_code
                        ).order_by("-id")[:4]
                        card_exp_list = ProjectExpense.objects.filter(
                            company_code=active.company_code
                        ).order_by("-id")[:6]

                        card_invesment_list = Investor_Wallet_Details.objects.filter(
                            company_code=active.company_code
                        ).order_by("-id")[:6]
                        project_value = Project.objects.filter(
                            company_code=active.company_code, delete_status=False
                        )
                        total_project_value = project_value.aggregate(
                            Sum("Total_share")
                        )["Total_share__sum"]

                        new_projects = Project.objects.filter(
                            company_code=active.company_code, delete_status=False
                        ).order_by("-id")[:5]

                        investor_value = Invesments_Db.objects.filter(
                            company_code=active.company_code
                        )
                        if investor_value.count() > 0:
                            totale_investor_value = int(
                                investor_value.aggregate(Sum("amount"))["amount__sum"]
                            )
                        else:
                            totale_investor_value = 0

                        Expenses = ProjectExpense.objects.filter(
                            company_code=active.company_code
                        )
                        if Expenses.count() > 0:
                            total_Expenses = Expenses.aggregate(Sum("amount"))[
                                "amount__sum"
                            ]
                        else:
                            total_Expenses = 0

                        projects = ProjectSales.objects.filter(
                            company_code=active.company_code
                        )
                        if projects.count() > 0:
                            total_sales = projects.aggregate(Sum("amount"))[
                                "amount__sum"
                            ]
                            ext_otr_expense = project_value.aggregate(
                                Sum("Other_expense")
                            )["Other_expense__sum"]
                            comapny_expense = 0
                        else:
                            total_sales = 0
                            ext_otr_expense = 0
                        unused_share = 0
                        if total_Expenses > ext_otr_expense:
                            comapny_expense = int(total_Expenses - ext_otr_expense)
                        elif total_Expenses < ext_otr_expense:
                            unused_share = int(ext_otr_expense - total_Expenses)
                        else:
                            comapny_expense = 0
                        temp_profit = int(total_sales - totale_investor_value)
                        if unused_share > 0 and comapny_expense <= 0:
                            total_profit = int(temp_profit + unused_share)
                        else:
                            total_profit = int(temp_profit - comapny_expense)

                        profit_persentage = None

                        try:
                            profit_persentage = (
                                total_profit / totale_investor_value
                            ) * 100
                            get_profit_percentage = "{:.2f}%".format(profit_persentage)
                            if get_profit_percentage != "":
                                context = {
                                    "name": s,
                                    "satus": sts,
                                    "total_profit": total_profit,
                                    "total_sales": total_sales,
                                    "list_sales": list_sales,
                                    "sales_count": sales_count,
                                    "card_invesment_list": card_invesment_list,
                                    "card_exp_list": card_exp_list,
                                    "new_projects": new_projects,
                                    "total_Expenses": total_Expenses,
                                    "totale_investor_value": totale_investor_value,
                                    "get_profit_percentage": get_profit_percentage,
                                    "total_project_value": total_project_value,
                                    "staff_comapny": staff_comapny,
                                    "staff": staff,
                                    "project_permissions": project_permissions,
                                    "investor_permissions": investor_permissions,
                                    "pro_inv_permissions": pro_inv_permissions,
                                    "pro_exp_permissions": pro_exp_permissions,
                                    "pro_profit_permissions": pro_profit_permissions,
                                    "dashbord_permissions": dashbord_permissions,
                                    "wallet_permissions": wallet_permissions,
                                    "settlement_permissions": settlement_permissions,
                                    "Reports_permissions": Reports_permissions,
                                }
                        except:
                            if project_value.exists():
                                context = {
                                    "name": s,
                                    "satus": sts,
                                    "total_sales": total_sales,
                                    "list_sales": list_sales,
                                    "sales_count": sales_count,
                                    "total_profit": total_profit,
                                    "card_invesment_list": card_invesment_list,
                                    "card_exp_list": card_exp_list,
                                    "new_projects": new_projects,
                                    "total_Expenses": total_Expenses,
                                    "totale_investor_value": totale_investor_value,
                                    "total_project_value": total_project_value,
                                    "staff_comapny": staff_comapny,
                                    "staff": staff,
                                    "project_permissions": project_permissions,
                                    "investor_permissions": investor_permissions,
                                    "pro_inv_permissions": pro_inv_permissions,
                                    "pro_exp_permissions": pro_exp_permissions,
                                    "pro_profit_permissions": pro_profit_permissions,
                                    "dashbord_permissions": dashbord_permissions,
                                    "wallet_permissions": wallet_permissions,
                                    "settlement_permissions": settlement_permissions,
                                    "Reports_permissions": Reports_permissions,
                                }
                        if not project_value.exists():
                            context = {
                                "name": s,
                                "satus": sts,
                                "staff_comapny": staff_comapny,
                                "staff": staff,
                                "project_permissions": project_permissions,
                                "investor_permissions": investor_permissions,
                                "pro_inv_permissions": pro_inv_permissions,
                                "pro_exp_permissions": pro_exp_permissions,
                                "pro_profit_permissions": pro_profit_permissions,
                                "wallet_permissions": wallet_permissions,
                                "dashbord_permissions": dashbord_permissions,
                                "settlement_permissions": settlement_permissions,
                                "Reports_permissions": Reports_permissions,
                            }
            else:
                dashbord_permissions = get_object_or_404(
                    Dashbord_view, staff_name=s, company_code=staff_comapny_code
                )
                project_permissions = get_object_or_404(
                    Project_menu, staff_name=s, company_code=staff_comapny_code
                )
                wallet_permissions = get_object_or_404(
                    Investor_wallet_menu, staff_name=s, company_code=staff_comapny_code
                )
                investor_permissions = get_object_or_404(
                    Investor_menu, staff_name=s, company_code=staff_comapny_code
                )
                pro_inv_permissions = get_object_or_404(
                    Project_investor_menu, staff_name=s, company_code=staff_comapny_code
                )
                pro_exp_permissions = get_object_or_404(
                    Project_Exp_menu, staff_name=s, company_code=staff_comapny_code
                )
                pro_profit_permissions = get_object_or_404(
                    Project_Profit_menu, staff_name=s, company_code=staff_comapny_code
                )
                settlement_permissions = get_object_or_404(
                    Project_settlement_menu,
                    staff_name=s,
                    company_code=staff_comapny_code,
                )
                Reports_permissions = get_object_or_404(
                    Report_view, staff_name=s, company_code=staff_comapny_code
                )
                context = {
                    "name": s,
                    "satus": sts,
                    "staff_comapny": staff_comapny,
                    "staff": staff,
                    "project_permissions": project_permissions,
                    "investor_permissions": investor_permissions,
                    "pro_inv_permissions": pro_inv_permissions,
                    "pro_exp_permissions": pro_exp_permissions,
                    "wallet_permissions": wallet_permissions,
                    "pro_profit_permissions": pro_profit_permissions,
                    "dashbord_permissions": dashbord_permissions,
                    "settlement_permissions": settlement_permissions,
                    "Reports_permissions": Reports_permissions,
                }
        except Staff.DoesNotExist:
            pass

        if request.user.is_superuser:
            sts = "Super Admin"
            company_count = Company_table.objects.filter(delete_status=False).count()
            invs_count = Investors.objects.count()
            staff_count = Staff.objects.count()

            context = {
                "name": s,
                "satus": sts,
                "company_count": company_count,
                "invs_count": invs_count,
                "staff_count": staff_count,
            }

        return render(request, "admin_dash_menu/pages/dashbord_content.html", context)

    elif a == 0:
        return render(
            request=request, template_name="admin_dash_menu/auth/admin_login.html"
        )


@login_required
@csrf_protect
def empty_dashboard(request):
    a = request.user.is_authenticated
    if a == 1:
        s = request.user

        get_investor = checkinvestor_name(s)
        checkactive_investor = None
        checkactive_investor = Investors.objects.filter(email_id=get_investor)
        if checkactive_investor.count() > 1:
            for ins in checkactive_investor:
                checkactive_investor = ins
                print(checkactive_investor)
                break
        else:
            checkactive_investor = Investors.objects.get(email_id=get_investor)

        investor_is_active = checkactive_investor.status
        s = checkactive_investor.first_name
        print("empty_dashboard")

        sts = "Investor"
        context = {
            "name": s,
            "satus": sts,
            "investor_is_active": investor_is_active,
            "mymodel_intences": checkactive_investor,
        }

        return render(request, "admin_dash_menu/pages/investor_dashbord.html", context)


@login_required
@csrf_protect
def investor_dashboard_login(request, code):
    a = request.user.is_authenticated
    if a == 1:
        if code != "none":
            s = request.user
            data = dict()
            try:
                check_data = Investors.objects.get(
                    email_id=request.user, company_code=code
                )
                checkactive_investor = check_data.investors_code
            except Investors.DoesNotExist:
                checkactive_investor = None

            investor_is_active = check_data.status
            s = check_data.first_name
            sts = "Investor"
            get_profit_percentage_inves = 0
            all_total_insesment_invstor = 0
            tot_profit_inv = 0
            total_projects = 0

            try:
                check_wallet = Investor_Wallet_Details.objects.get(
                    investor_id=check_data.investors_code, company_code=code
                )
                check_wallet_amount = check_wallet.total_amount
            except Investor_Wallet_Details.DoesNotExist:
                check_wallet_amount = 0
            if investor_is_active == True:
                company_code = check_data.company_code
                investor_value = Invesments_Db.objects.filter(
                    investor_name=request.user, company_code=code
                )
                investor_value_proj = Invesments_Db.objects.filter(
                    investor_name=request.user, company_code=code
                )
                investor_value_list = list(investor_value_proj.values())

                if investor_value.count() > 0:
                    total_insesment_invstor = investor_value.aggregate(Sum("amount"))[
                        "amount__sum"
                    ]
                    get_unit_buy = 0
                    totale_investor_value = 0
                    for proj_code in investor_value_proj:
                        totale_investor_value = proj_code.project_code
                        # get_investor = Invesments_Db.objects.filter(investor_code=check_data.investors_code,company_code=check_data.company_code,project_code=proj_code.project_code,status=True)
                        # get_invested_amount = int(get_investor.aggregate(Sum('amount'))['amount__sum'])
                        # get_onves_count = Invesments_Db.objects.filter(project_code=proj_code.project_code).values('investor_share_count').annotate(count=Count('investor_share_count')).count()

                        # get_unit_buy+= int(get_investor.aggregate(Sum('investor_share_count'))['investor_share_count__sum'])
                        # total_invesment=Invesments_Db.objects.filter(company_code=check_data.company_code,project_code=proj_code.project_code,status=True)
                        # totale_investor_value += int(total_invesment.aggregate(Sum('amount'))['amount__sum'])

                        # if get_unit_buy > 0:
                        #         try:
                        #             check_exp=ProjectExpense.objects.filter(project_code=proj_code.project_code).latest('id')
                        #             get_exp=ProjectExpense.objects.filter(project_code=proj_code.project_code,Second_Approved_by__isnull=False)
                        #             total_expense=get_exp.aggregate(Sum('amount'))['amount__sum']
                        #         except ProjectExpense.DoesNotExist:
                        #             expense_count=0
                        #             total_expense=0
                        #         try:
                        #             check_sale=ProjectSales.objects.filter(project_code=proj_code.project_code).latest('id')
                        #             get_sale=ProjectSales.objects.filter(project_code=proj_code.project_code,Second_Approved_by__isnull=False)
                        #             total_sale=get_sale.aggregate(Sum('amount'))['amount__sum']
                        #         except ProjectSales.DoesNotExist:
                        #             sale_count=0
                        #             total_sale=0
                        #             total_unit_sale=0
                        #         temp_profit_1=total_sale-totale_investor_value
                        #         company_share=0
                        #         unused_exp=0
                        # if total_expense > get_project_main.Other_expense:
                        #     company_share=int(total_expense-get_project_main.Other_expense)
                        #     temp_profit_1=temp_profit_1-company_share
                        # elif total_expense < get_project_main.Other_expense:
                        #     unused_share=int(get_project_main.Other_expense-total_expense)
                        #     investor_count_get=Invesments_Db.objects.filter(project_code=get_project_main.prject_key).values('investor_name').annotate(count=Count('investor_name')).count()
                        #     unused_exp=(unused_share/investor_count_get)
                        # else:
                        #     company_share=0
                        #     temp_profit_1=temp_profit_1
                        # real_profit=(get_invested_amount/totale_investor_value)*temp_profit_1
                        # if unused_exp>0:
                        #     real_profit=real_profit+unused_exp
                        # profit_amount=int(real_profit)

                    # setment_blc=0
                    # get_Settlement_blance = Projectsettlement.objects.filter(investor_code=inves_id,company_code=get_project_main.company_code,project_code=proj_id,status=True)
                    # if get_Settlement_blance.count()>0:
                    #     setment_blc=get_Settlement_blance.aggregate(Sum('amount'))['amount__sum']
                    #     avalible_amount=int(profit_amount+get_invested_amount-setment_blc)
                    #     setment_blc=avalible_amount
                    # else:
                    #     setment_blc=int(profit_amount+get_invested_amount)
                    print("get_unit_buy", get_unit_buy)
                    print("get_invested_amount", totale_investor_value)
                    # print('investor_value.count()',investor_value_proj.count())
                    # print('get_onves_count',get_onves_count)

                context = {
                    "name": s,
                    "satus": sts,
                    "investor_is_active": investor_is_active,
                    "investor_value_list": investor_value_list,
                    "total_insesment_invstor": total_insesment_invstor,
                    "company_name": check_data.company_name,
                    "tot_profit_inv": tot_profit_inv,
                    "total_projects": total_projects,
                    "check_wallet_amount": check_wallet_amount,
                }
                data = context

            else:
                context = {
                    "name": s,
                    "satus": sts,
                    "investor_is_active": investor_is_active,
                    "check_wallet_amount": check_wallet_amount,
                }
                data = context

            return JsonResponse(data)

    elif a == 0:
        return render(
            request=request, template_name="admin_dash_menu/auth/admin_login.html"
        )


def checkinvestor_name(s):
    try:
        investor = Investors.objects.filter(email_id=s, status=True)
        if investor.count() > 1:
            active_investor = investor.first()
            print(active_investor)
            return active_investor
        elif investor.count() == 1:
            active_investor = Investors.objects.get(email_id=s)
            return active_investor

    except Investors.DoesNotExist:
        return None


@login_required
def get_investors_loged_company(request):
    # print("Getting companies")
    if request.user.is_authenticated:
        try:
            current_company = Investors.objects.filter(email_id=request.user)
            if current_company.exists():
                current_companys = Investors.objects.filter(email_id=request.user)
                project_list = [
                    {
                        "id": c.company_code,
                        "name": c.company_name,
                    }
                    for c in current_companys
                ]
                return JsonResponse({"projects": project_list})
        except Investors.DoesNotExist:
            pass

    else:
        return JsonResponse({"error": "User is not authenticated"})


@login_required
def get_invested_project_name(request, comp_code):
    if request.user.is_authenticated:
        current_companys = Invesments_Db.objects.filter(
            company_code=comp_code, status=True
        )
        project_list = [
            {
                "id": c.project_code,
                "name": c.project,
            }
            for c in current_companys
        ]
        return JsonResponse({"projects": project_list})
    else:
        return JsonResponse({"error": "User is not authenticated"})


@login_required
def get_project_data(request, p_code, c_code):
    if request.user.is_authenticated:
        data = dict()
        comp_code = c_code
        proj_id = p_code
        try:
            check_data = Investors.objects.get(
                email_id=request.user, company_code=comp_code
            )
            inves_id = check_data.investors_code
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
                get_invested_amount = int(
                    get_investor.aggregate(Sum("amount"))["amount__sum"]
                )

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
                        company_share = int(
                            total_expense - get_project_main.Other_expense
                        )
                        temp_profit_1 = temp_profit_1 - company_share
                    elif total_expense < get_project_main.Other_expense:
                        unused_share = int(
                            get_project_main.Other_expense - total_expense
                        )
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
                    real_profit = (
                        get_invested_amount / totale_investor_value
                    ) * temp_profit_1
                    if unused_exp > 0:
                        real_profit = real_profit + unused_exp
                    profit_amount = int(real_profit)

            except Invesments_Db.DoesNotExist:
                get_invested_amount = 0
                get_Settlement_blance = 0
                get_unit_buy = 0
                profit_amount = 0
                totale_investor_value = 0

            data["get_invested_amount"] = get_invested_amount
            data["get_unit_buy"] = get_unit_buy
            data["totale_investor_value"] = totale_investor_value
            data["profit_amount"] = profit_amount
        except Investors.DoesNotExist:
            checkactive_investor = None
        return JsonResponse(data)

    else:
        return JsonResponse({"error": "User is not authenticated"})


@login_required
def change_dashbord(request):
    if request.method == "POST":
        email = request.user
        company_name = request.POST["company"]
        # print(company_name)

        get_company = Investors.objects.get(email_id=email, company_name=company_name)

        return get_company
