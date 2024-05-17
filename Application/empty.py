from django.contrib.admin.models import LogEntry
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count
from .forms import CustomUserCreationForm
from .models import *
from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response


def admin_register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_login")
    else:
        form = CustomUserCreationForm()
    return render(request, "admin_dash_menu/auth/admin_register.html")


def admin_login(request):
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
                    response = redirect("base")
                    response.set_cookie("user_data")
                    return response
                else:
                    return render(
                        request,
                        "admin_dash_menu/auth/admin_login.html",
                        {"error": "Account Not Activate"},
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
                    # active_investors = Investors.objects.get(email_id=username, status=True)

                else:
                    active_investor = None
                    active_investor = Investors.objects.get(
                        email_id=username, status=True
                    )

                # checkactive_investor=Investors.objects.get(email_id=active_investor)
                # is_active=active_investor.status
                if admin is not None and active_investor is not None:
                    login(request, admin)
                    response = redirect("empty_dashboard")
                    response.set_cookie("user_data")
                    return response
                else:
                    return render(
                        request,
                        "admin_dash_menu/auth/admin_login.html",
                        {"error": "Account Not Activate"},
                    )
            except Investors.DoesNotExist:
                pass
            try:
                checkactive_staff = Staff.objects.get(username=username)
                is_active_staff = checkactive_staff.satus
                if admin is not None and is_active_staff == 1:
                    login(request, admin)
                    response = redirect("base")
                    response.set_cookie("user_data")
                    return response
                else:
                    return render(
                        request,
                        "admin_dash_menu/auth/admin_login.html",
                        {"error": "Account Not Activate"},
                    )
            except Staff.DoesNotExist:
                pass
            if admin is not None and admin.is_superuser:
                login(request, admin)
                response = redirect("base")
                response.set_cookie("user_data")
                return response

        return render(
            request,
            "admin_dash_menu/auth/admin_login.html",
            {"error": "Enter ID and Password"},
        )
    else:
        return render(
            request=request, template_name="admin_dash_menu/auth/admin_login.html"
        )


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
                        company_code=active.company_code
                    )
                    total_project_value = project_value.aggregate(Sum("Project_value"))[
                        "Project_value__sum"
                    ]
                    new_projects = Project.objects.filter(
                        company_code=active.company_code
                    ).order_by("-id")[:5]

                    investor_value = Project_Investor.objects.filter(
                        company_code=active.company_code
                    )
                    totale_investor_value = investor_value.aggregate(Sum("amount"))[
                        "amount__sum"
                    ]
                    new_projects_investors = Project_Investor.objects.filter(
                        company_code=active.company_code
                    ).order_by("-id")[:5]

                    projects = ProjectProfit.objects.filter(
                        company_code=active.company_code
                    )
                    total_profit = projects.aggregate(Sum("peofit_amount"))[
                        "peofit_amount__sum"
                    ]

                    Expenses = ProjectExpense.objects.filter(
                        company_code=active.company_code
                    )
                    total_Expenses = Expenses.aggregate(Sum("amount"))["amount__sum"]
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
                                "new_projects": new_projects,
                                "total_Expenses": total_Expenses,
                                "new_projects_investors": new_projects_investors,
                                "totale_investor_value": totale_investor_value,
                                "total_project_value": total_project_value,
                                "get_profit_percentage": get_profit_percentage,
                                "company_dashboard": company_dash,
                            }
                    except:
                        if project_value.exists():
                            context = {
                                "name": s,
                                "satus": sts,
                                "company": checkactive,
                                "total_profit": total_profit,
                                "new_projects": new_projects,
                                "total_Expenses": total_Expenses,
                                "new_projects_investors": new_projects_investors,
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
            if dashbord_permissions.view:
                if checkactive_Staff is not None:
                    active = Company_table.objects.get(company_code=staff_comapny_code)
                    if active is not None:
                        checkactive = staff_comapny
                        project_value = Project.objects.filter(
                            company_code=active.company_code
                        )
                        total_project_value = project_value.aggregate(
                            Sum("Project_value")
                        )["Project_value__sum"]
                        new_projects = Project.objects.filter(
                            company_code=active.company_code
                        ).order_by("-id")[:5]

                        investor_value = Project_Investor.objects.filter(
                            company_code=active.company_code
                        )
                        totale_investor_value = investor_value.aggregate(Sum("amount"))[
                            "amount__sum"
                        ]
                        new_projects_investors = Project_Investor.objects.filter(
                            company_code=active.company_code
                        ).order_by("-id")[:5]

                        projects = ProjectProfit.objects.filter(
                            company_code=active.company_code
                        )
                        total_profit = projects.aggregate(Sum("peofit_amount"))[
                            "peofit_amount__sum"
                        ]

                        Expenses = ProjectExpense.objects.filter(
                            company_code=active.company_code
                        )
                        total_Expenses = Expenses.aggregate(Sum("amount"))[
                            "amount__sum"
                        ]
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
                                    "company": checkactive,
                                    "total_profit": total_profit,
                                    "new_projects": new_projects,
                                    "total_Expenses": total_Expenses,
                                    "new_projects_investors": new_projects_investors,
                                    "totale_investor_value": totale_investor_value,
                                    "total_project_value": total_project_value,
                                    "get_profit_percentage": get_profit_percentage,
                                    "staff_comapny": staff_comapny,
                                    "staff": staff,
                                    "project_permissions": project_permissions,
                                    "investor_permissions": investor_permissions,
                                    "pro_inv_permissions": pro_inv_permissions,
                                    "pro_exp_permissions": pro_exp_permissions,
                                    "pro_profit_permissions": pro_profit_permissions,
                                    "dashbord_permissions": dashbord_permissions,
                                }
                        except:
                            if project_value.exists():
                                context = {
                                    "name": s,
                                    "satus": sts,
                                    "total_profit": total_profit,
                                    "new_projects": new_projects,
                                    "total_Expenses": total_Expenses,
                                    "new_projects_investors": new_projects_investors,
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
                                }
                        if not project_value.exists():
                            context = {
                                "name": s,
                                "satus": sts,
                                # 'company':checkactive,
                                "staff_comapny": staff_comapny,
                                "staff": staff,
                                "project_permissions": project_permissions,
                                "investor_permissions": investor_permissions,
                                "pro_inv_permissions": pro_inv_permissions,
                                "pro_exp_permissions": pro_exp_permissions,
                                "pro_profit_permissions": pro_profit_permissions,
                                "dashbord_permissions": dashbord_permissions,
                            }
            else:
                dashbord_permissions = get_object_or_404(
                    Dashbord_view, staff_name=s, company_code=staff_comapny_code
                )
                project_permissions = get_object_or_404(
                    Project_menu, staff_name=s, company_code=staff_comapny_code
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
                    "dashbord_permissions": dashbord_permissions,
                }
        except Staff.DoesNotExist:
            pass

        if request.user.is_superuser:
            sts = "Super Admin"
            company_count = Company_table.objects.count()
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
        }

        return render(request, "admin_dash_menu/pages/investor_dashbord.html", context)


@login_required
@csrf_protect
def investor_dashboard_login(request):
    a = request.user.is_authenticated
    data = dict()
    # template_name="admin_dash_menu/pages/slect_comp.html"
    if a == 1:
        s = request.user
        get_investor = checkinvestor_name(s)
        # print(get_investor)
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
        sts = "Investor"
        get_profit_percentage = None
        investor_profit_or_loss = None
        get_profit_percentage_inves = None
        get_project = None
        real_total_profit = None
        tot_profit_inv = None
        total_projects = None
        lop = 0
        investor_total_profit_sum = 0
        investor_total_expences_sum = 0
        dasbord_company = None
        investor_company = request.POST.get("company_name", None)
        print(investor_company)
        if investor_company is not None:
            flt_dasbord_company = Company_table.objects.filter(
                company_name=investor_company
            )
            for i in flt_dasbord_company:
                data = dict()
                dasbord_company = Company_table.objects.get(
                    company_name=investor_company
                )
                investor_value = Project_Investor.objects.filter(
                    investor_name=request.user
                )
                if investor_value is not None:
                    project_value = Project.objects.filter(
                        company_code=dasbord_company.company_code
                    )
                    total_project_value = project_value.aggregate(Sum("Project_value"))[
                        "Project_value__sum"
                    ]
                    top_new_projects = Project.objects.filter(
                        company_code=dasbord_company.company_code
                    ).order_by("-id")[:5]
                    investor_value_invesment = Project_Investor.objects.filter(
                        investor_code=checkactive_investor.investors_code
                    )
                    total_insesment_invstor = investor_value_invesment.aggregate(
                        Sum("amount")
                    )["amount__sum"]

                    Expenses = ProjectExpense.objects.filter(
                        company_code=dasbord_company.company_code
                    )
                    total_Expenses = Expenses.aggregate(Sum("amount"))["amount__sum"]
                    investor_investments = Project_Investor.objects.filter(
                        investor_code=checkactive_investor.investors_code
                    )
                    total_invesment = investor_investments.aggregate(Sum("amount"))[
                        "amount__sum"
                    ]

                    projects = ProjectProfit.objects.filter(
                        company_code=dasbord_company.company_code
                    )
                    total_profit = projects.aggregate(Sum("peofit_amount"))[
                        "peofit_amount__sum"
                    ]

                    Expenses = ProjectExpense.objects.filter(
                        company_code=dasbord_company.company_code
                    )
                    total_Expenses_inv = Expenses.aggregate(Sum("amount"))[
                        "amount__sum"
                    ]

                    if projects.exists():
                        for investor in investor_investments:
                            get_project = get_object_or_404(
                                Project, prject_key=investor.project_code
                            )
                            investor_value_invesment_pp = (
                                Project_Investor.objects.filter(
                                    project_code=investor.project_code
                                )
                            )

                            net_profit = ProjectProfit.objects.filter(
                                project_code=investor.project_code
                            )

                            investor_profit_or_loss = round(
                                total_profit
                                * (investor.amount)
                                / get_project.Project_value,
                                2,
                            )

                            get_project = get_object_or_404(
                                Project, prject_key=investor.project_code
                            )
                            net_expences = ProjectExpense.objects.filter(
                                project_code=investor.project_code
                            )

                            project_count = Project_Investor.objects.filter(
                                company_code=investor.company_code,
                                investor_code=investor.investor_code,
                            ).aggregate(total_projects=Count("project"))

                            total_projects = project_count["total_projects"]

                            for net in net_profit:
                                investor_total_profit_sum += net.peofit_amount

                            for exp in net_expences:
                                investor_total_expences_sum += exp.amount

                            for aa in investor_value_invesment_pp:
                                lop += aa.amount

                            real_total_profit = (
                                total_invesment / lop
                            ) * investor_total_profit_sum

                            investor_percentage = round(
                                (real_total_profit / total_invesment) * 100, 2
                            )
                            get_profit_percentage_inves = "{:.2f}%".format(
                                investor_percentage
                            )

                        if real_total_profit is not None:
                            tot_profit_inv = total_invesment + real_total_profit
                        context = {
                            "name": s,
                            "satus": sts,
                            "investor_is_active": investor_is_active,
                            "investor_value_invesment": list(
                                investor_value_invesment.values()
                            ),
                            "total_invesment": total_invesment,
                            "tot_profit_inv": tot_profit_inv,
                            "total_projects": total_projects,
                            "investor_profit_or_loss": real_total_profit,
                            "get_profit_percentage_inves": get_profit_percentage_inves,
                            # 'get_project':get_project,
                            "total_projects": total_projects,
                        }
                        data = context
                    else:
                        context = {
                            "name": s,
                            "satus": sts,
                            "investor_is_active": investor_is_active,
                            # 'investor_value_invesment':list(investor_value_invesment.values()),
                            "total_invesment": total_invesment,
                            # 'get_project':get_project,
                            "total_Expenses": total_Expenses,
                        }
                        data = context
        else:
            context = {
                "name": s,
                "satus": sts,
                "investor_is_active": investor_is_active,
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
            # print(active_investor)
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
                        "id": c.id,
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
def change_dashbord(request):
    if request.method == "POST":
        email = request.user
        company_name = request.POST["company"]
        # print(company_name)

        get_company = Investors.objects.get(email_id=email, company_name=company_name)

        return get_company
