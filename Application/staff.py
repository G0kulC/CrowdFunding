from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required
@csrf_protect
def view_staff(request, pk):
    data = dict()
    my_model_instances = get_object_or_404(Staff, pk=pk)
    context = {"my_model_instances": my_model_instances}

    template_name = "admin_dash_menu/pages/staff/staff_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def staff_list(request):
    s = request.user
    try:
        check = Company_table.objects.get(email_id=s)

        code = check.company_code
        sts = "Admin"
        name = check.company_name
        get_my_model_instances = Staff.objects.filter(company_code=code)
        paginator = Paginator(get_my_model_instances, 10)  # 10 items per page
        page = request.GET.get("page")
        my_model_instances = paginator.get_page(page)
        return render(
            request,
            "admin_dash_menu/pages/staff/staff.html",
            {
                "my_model_instances": my_model_instances,
                "name": name,
                "satus": sts,
                "company": name,
            },
        )
    except Company_table.DoesNotExist:
        return redirect("notallowed")


@login_required
@csrf_protect
def save_staff_form(request, form, template_name, pk):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            staff_data = Staff.objects.get(pk=pk)
            temp_data = {
                "company_name": staff_data.company_name,
                "username": staff_data.username,
                "password": staff_data.password,
                "created_at": str(staff_data.created_at.strftime("%d-%m-%Y")),
                "status": True,
            }
            create_log = staff_logs.objects.create(
                company_name=staff_data.company_name,
                company_code=staff_data.company_code,
                username=staff_data.username,
                password=staff_data.password,
                ip_address=request.META["REMOTE_ADDR"],
                action="Updated",
                action_data=temp_data,
                user=request.user,
            )
            data["update"] = True
            books = Staff.objects.all()
            data["html_book_list"] = render_to_string(
                "admin_dash_menu/pages/staff/staff.html", {"books": books}
            )
        else:
            data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def staff_create(request):
    data = dict()
    form = Staff_RegistationForm()
    if request.method == "POST":
        company_id = request.user
        get_com_name = Company_table.objects.get(email_id=company_id)
        code = get_com_name.company_code
        cmp_name = get_com_name.company_name
        username_staff = request.POST["username"]
        password = request.POST["password"]
        status = request.POST["satus"]
        if status == "on":
            box = True

        elif status != "on":
            box = False
        try:
            check_data = Staff.objects.get(username=username_staff)
            if check_data is not None:
                context = {"error": "☹Username or Password Already Exists!"}
                return JsonResponse(context, status=400)
        except Staff.DoesNotExist:
            if " " in username_staff:
                context = {"error": "☹Username cannot contain spaces!"}
                return JsonResponse(context, status=400)
            elif username_staff is not None and password is not None:
                user1 = User.objects.create(username=username_staff)
                user1.set_password(password)
                staff_save = Staff.objects.create(
                    company_name=cmp_name,
                    company_code=code,
                    username=username_staff,
                    password=password,
                    satus=box,
                )

                save_dashbord_permissions = Dashbord_view.objects.create(
                    staff_name=username_staff,
                    company_name=cmp_name,
                    company_code=code,
                    view=False,
                    status=False,
                )
                save_Report_permissions = Report_view.objects.create(
                    staff_name=username_staff,
                    company_name=cmp_name,
                    company_code=code,
                    view=False,
                    status=False,
                )
                save_project_permissions = Project_menu.objects.create(
                    staff_name=username_staff,
                    company_name=cmp_name,
                    company_code=code,
                    view=False,
                    add=False,
                    edit=False,
                    can_delete=False,
                    status=False,
                )
                save_investor_permissions = Investor_menu.objects.create(
                    staff_name=username_staff,
                    company_name=cmp_name,
                    company_code=code,
                    view=False,
                    add=False,
                    edit=False,
                    can_delete=False,
                    status=False,
                )
                save_wallet_permissions = Investor_wallet_menu.objects.create(
                    staff_name=username_staff,
                    company_name=cmp_name,
                    company_code=code,
                    view=False,
                    add=False,
                    edit=False,
                    can_delete=False,
                    status=False,
                )
                save_project_inv_permissions = Project_investor_menu.objects.create(
                    staff_name=username_staff,
                    company_name=cmp_name,
                    company_code=code,
                    view=False,
                    add=False,
                    edit=False,
                    can_delete=False,
                    status=False,
                )
                save_project_exp_permissions = Project_Exp_menu.objects.create(
                    staff_name=username_staff,
                    company_name=cmp_name,
                    company_code=code,
                    view=False,
                    add=False,
                    edit=False,
                    can_delete=False,
                    status=False,
                )
                save_project_profit_permissions = Project_Profit_menu.objects.create(
                    staff_name=username_staff,
                    company_name=cmp_name,
                    company_code=code,
                    view=False,
                    add=False,
                    edit=False,
                    can_delete=False,
                    status=False,
                )
                save_project_settlement_menu = Project_settlement_menu.objects.create(
                    staff_name=username_staff,
                    company_name=cmp_name,
                    company_code=code,
                    view=False,
                    add=False,
                    edit=False,
                    can_delete=False,
                    status=False,
                )
                user1.save()
                staff_save.save()
                save_dashbord_permissions.save()
                save_Report_permissions.save()
                save_project_permissions.save()
                save_investor_permissions.save()
                save_wallet_permissions.save()
                save_project_inv_permissions.save()
                save_project_exp_permissions.save()
                save_project_profit_permissions.save()
                save_project_settlement_menu.save()

                temp_data = {
                    "company_name": staff_save.company_name,
                    "username": staff_save.username,
                    "password": staff_save.password,
                    "created_at": str(staff_save.created_at.strftime("%d-%m-%Y")),
                    "status": True,
                }
                create_log = staff_logs.objects.create(
                    company_name=staff_save.company_name,
                    company_code=staff_save.company_code,
                    username=staff_save.username,
                    password=staff_save.password,
                    ip_address=request.META["REMOTE_ADDR"],
                    action="Created",
                    action_data=temp_data,
                    user=request.user,
                )

        data["form_is_valid"] = True
        data["add"] = True

        books = Staff.objects.all()
        data["html_book_list"] = render_to_string(
            "admin_dash_menu/pages/staff/staff.html", {"books": books}
        )
    else:
        data["form_is_valid"] = False

    context = {"form": form}
    data["html_form"] = render_to_string(
        "admin_dash_menu/pages/staff/staff_reg.html", context, request=request
    )
    return JsonResponse(data)


@login_required
@csrf_protect
def staff_update(request, pk):
    book = get_object_or_404(Staff, pk=pk)
    old_user = book.username
    if request.method == "POST":
        username_staff = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.get(username=old_user)
        user.username = username_staff
        user.set_password(password)
        user.save()

        form = Staff_RegistationForm(request.POST, instance=book)
    else:
        form = Staff_RegistationForm(instance=book)
    return save_staff_form(
        request, form, "admin_dash_menu/pages/staff/staff_edit.html", pk
    )


@login_required
@csrf_protect
def delete_staff(request, pk):
    mymodel = get_object_or_404(Staff, pk=pk)

    get_user_name = mymodel.username
    trashed_data = TrashedData.objects.create(
        user=request.user,
        original_data=mymodel.__dict__,
    )
    project_menu_delete = Project_menu.objects.get(staff_name=mymodel.username)
    Dashbord_view_delete = Dashbord_view.objects.get(staff_name=mymodel.username)
    Investor_menu_delete = Investor_menu.objects.get(staff_name=mymodel.username)
    project_Investor_menu_delete = Project_investor_menu.objects.get(
        staff_name=mymodel.username
    )
    Investor_wallet_menu_delete = Investor_wallet_menu.objects.get(
        staff_name=mymodel.username
    )
    Project_Exp_menu_delete = Project_Exp_menu.objects.get(staff_name=mymodel.username)
    Project_Profit_menu_delete = Project_Profit_menu.objects.get(
        staff_name=mymodel.username
    )
    settlement_permissions_delete = get_object_or_404(
        Project_settlement_menu, staff_name=mymodel.username
    )
    Reports_permissions_delete = get_object_or_404(
        Report_view, staff_name=mymodel.username
    )

    user_to_delete = User.objects.get(username=get_user_name)
    project_menu_delete.delete()
    Dashbord_view_delete.delete()
    project_Investor_menu_delete.delete()
    Investor_menu_delete.delete()
    Investor_wallet_menu_delete.delete()
    Project_Exp_menu_delete.delete()
    Project_Profit_menu_delete.delete()
    settlement_permissions_delete.delete()
    Reports_permissions_delete.delete()

    temp_data = {
        "company_name": mymodel.company_name,
        "username": mymodel.username,
        "password": mymodel.password,
        "created_at": str(mymodel.created_at.strftime("%d-%m-%Y")),
        "status": True,
    }
    create_log = staff_logs.objects.create(
        company_name=mymodel.company_name,
        company_code=mymodel.company_code,
        username=mymodel.username,
        password=mymodel.password,
        ip_address=request.META["REMOTE_ADDR"],
        action="Deleted",
        action_data=temp_data,
        user=request.user,
    )
    user_to_delete.delete()
    mymodel.delete()
    return JsonResponse({"status": "ok"})


def add_permisions_staff(request, pk):
    data = dict()
    if request.method == "POST":
        company_id = request.user
        get_com_name = Company_table.objects.get(email_id=company_id)
        code = get_com_name.company_code
        cmp_name = get_com_name.company_name
        username_staff = request.POST["staff_name"]
        view_p = request.POST.get("project_view", False)
        add_p = request.POST.get("project_add", False)
        edit_p = request.POST.get("project_edit", False)
        delete_p = request.POST.get("project_delete", False)

        status_per = request.POST.get("per_satus", False)

        dash_view = request.POST.get("dash_view", False)
        try:
            staff_permissions01 = Dashbord_view.objects.get(
                staff_name=username_staff, company_code=code
            )
            staff_permissions01.view = dash_view
            staff_permissions01.status = status_per
            staff_permissions01.save()
        except Dashbord_view.DoesNotExist:
            save_dash_permissions = Dashbord_view.objects.create(
                staff_name=username_staff,
                company_code=code,
                view=dash_view,
                status=status_per,
            )
            save_dash_permissions.save()

        report_view = request.POST.get("report_view", False)
        try:
            staff_permissionsReport_view = Report_view.objects.get(
                staff_name=username_staff, company_code=code
            )
            staff_permissionsReport_view.view = report_view
            staff_permissionsReport_view.status = status_per
            staff_permissionsReport_view.save()
        except Report_view.DoesNotExist:
            staff_permissionsReport_view = None
            staff_permissionsReport_view = Report_view.objects.create(
                staff_name=username_staff,
                company_code=code,
                view=report_view,
                status=status_per,
            )
            staff_permissionsReport_view.save()
        try:
            staff_permissions = Project_menu.objects.get(
                staff_name=username_staff, company_code=code
            )
            staff_permissions.view = view_p
            staff_permissions.add = add_p
            staff_permissions.edit = edit_p
            staff_permissions.can_delete = delete_p
            staff_permissions.status = status_per
            staff_permissions.save()
        except Project_menu.DoesNotExist:
            save_project_permissions = Project_menu.objects.create(
                staff_name=username_staff,
                company_code=code,
                view=view_p,
                add=add_p,
                edit=edit_p,
                can_delete=delete_p,
                status=status_per,
            )
            save_project_permissions.save()

        view_inv = request.POST.get("investor_view", False)
        add_inv = request.POST.get("investor_add", False)
        edit_inv = request.POST.get("investor_edit", False)
        delete_inv = request.POST.get("investor_delete", False)
        try:
            staff_permissions1 = Investor_menu.objects.get(
                staff_name=username_staff, company_code=code
            )
            staff_permissions1.view = view_inv
            staff_permissions1.add = add_inv
            staff_permissions1.edit = edit_inv
            staff_permissions1.can_delete = delete_inv
            staff_permissions1.status = status_per
            staff_permissions1.save()
        except Investor_menu.DoesNotExist:
            save_investor_permissions = Investor_menu.objects.create(
                staff_name=username_staff,
                company_code=code,
                view=view_inv,
                add=add_inv,
                edit=edit_inv,
                can_delete=delete_inv,
                status=status_per,
            )
            save_investor_permissions.save()

        viewwallet = request.POST.get("wallet_view", False)
        addwallet = request.POST.get("wallet_add", False)
        editwallet = request.POST.get("wallet_edit", False)
        deletewallet = request.POST.get("wallet_delete", False)

        try:
            staff_permissionswallet = Investor_wallet_menu.objects.get(
                staff_name=username_staff, company_code=code
            )
            staff_permissionswallet.view = viewwallet
            staff_permissionswallet.add = addwallet
            staff_permissionswallet.edit = editwallet
            staff_permissionswallet.can_delete = deletewallet
            staff_permissionswallet.status = status_per
            staff_permissionswallet.save()
        except Investor_wallet_menu.DoesNotExist:
            savewallet_permissions = Investor_wallet_menu.objects.create(
                staff_name=username_staff,
                company_code=code,
                view=viewwallet,
                add=addwallet,
                edit=editwallet,
                can_delete=deletewallet,
                status=status_per,
            )
            savewallet_permissions.save()

        view_proj_inv = request.POST.get("pro_inv_view", False)
        add_proj_inv = request.POST.get("pro_inv_add", False)
        edit_proj_inv = request.POST.get("pro_inv_edit", False)
        delete_proj_inv = request.POST.get("pro_inv_delete", False)
        try:
            staff_permissions2 = Project_investor_menu.objects.get(
                staff_name=username_staff, company_code=code
            )
            staff_permissions2.view = view_proj_inv
            staff_permissions2.add = add_proj_inv
            staff_permissions2.edit = edit_proj_inv
            staff_permissions2.can_delete = delete_proj_inv
            staff_permissions2.status = status_per
            staff_permissions2.save()
        except Project_investor_menu.DoesNotExist:
            save_proj_investor_permissions = Project_investor_menu.objects.create(
                staff_name=username_staff,
                company_code=code,
                view=view_proj_inv,
                add=add_proj_inv,
                edit=edit_proj_inv,
                can_delete=delete_proj_inv,
                status=status_per,
            )
            save_proj_investor_permissions.save()

        view_proj_exp = request.POST.get("pro_exp_view", False)
        add_proj_exp = request.POST.get("pro_exp_add", False)
        edit_proj_exp = request.POST.get("pro_exp_edit", False)
        delete_proj_exp = request.POST.get("pro_exp_delete", False)
        try:
            staff_permissions3 = Project_Exp_menu.objects.get(
                staff_name=username_staff, company_code=code
            )
            staff_permissions3.view = view_proj_exp
            staff_permissions3.add = add_proj_exp
            staff_permissions3.edit = edit_proj_exp
            staff_permissions3.can_delete = delete_proj_exp
            staff_permissions3.status = status_per
            staff_permissions3.save()
        except Project_Exp_menu.DoesNotExist:
            save_proj_exp_permissions = Project_Exp_menu.objects.create(
                staff_name=username_staff,
                company_code=code,
                view=view_proj_exp,
                add=add_proj_exp,
                edit=edit_proj_exp,
                can_delete=delete_proj_exp,
                status=status_per,
            )
            save_proj_exp_permissions.save()

        view_proj_profit = request.POST.get("pro_profit_view", False)
        add_proj_profit = request.POST.get("pro_profit_add", False)
        edit_proj_profit = request.POST.get("pro_profit_edit", False)
        delete_proj_profit = request.POST.get("pro_profit_delete", False)
        try:
            staff_permissions4 = Project_Profit_menu.objects.get(
                staff_name=username_staff, company_code=code
            )
            staff_permissions4.view = view_proj_profit
            staff_permissions4.add = add_proj_profit
            staff_permissions4.edit = edit_proj_profit
            staff_permissions4.can_delete = delete_proj_profit
            staff_permissions4.status = status_per
            staff_permissions4.save()
        except Project_Profit_menu.DoesNotExist:
            save_proj_profit_permissions = Project_Profit_menu.objects.create(
                staff_name=username_staff,
                company_code=code,
                view=view_proj_profit,
                add=add_proj_profit,
                edit=edit_proj_profit,
                can_delete=delete_proj_profit,
                status=status_per,
            )
            save_proj_profit_permissions.save()

        view_proj_setle = request.POST.get("settlement_view", False)
        add_proj_setle = request.POST.get("settlement_add", False)
        edit_proj_setle = request.POST.get("settlement_edit", False)
        delete_proj_setle = request.POST.get("settlement_delete", False)
        try:
            save_proj_setle_permissions = Project_settlement_menu.objects.get(
                staff_name=username_staff, company_code=code
            )
            save_proj_setle_permissions.view = view_proj_setle
            save_proj_setle_permissions.add = add_proj_setle
            save_proj_setle_permissions.edit = edit_proj_setle
            save_proj_setle_permissions.can_delete = delete_proj_setle
            save_proj_setle_permissions.status = status_per
            save_proj_setle_permissions.save()
        except Project_settlement_menu.DoesNotExist:
            save_proj_setle_permissions = None
            save_proj_setle_permissions = Project_settlement_menu.objects.create(
                staff_name=username_staff,
                company_code=code,
                view=view_proj_setle,
                add=add_proj_setle,
                edit=edit_proj_setle,
                can_delete=delete_proj_setle,
                status=status_per,
            )
            save_proj_setle_permissions.save()

        temp_data = {
            "company_name": cmp_name,
            "username": username_staff,
            "dash_view": dash_view,
            "report_view": report_view,
            "proj_view": view_p,
            "proj_add": add_p,
            "proj_edit": edit_p,
            "proj_can_delete": delete_p,
            "inves_view": view_inv,
            "inves_add": add_inv,
            "inves_edit": edit_inv,
            "inves_can_delete": delete_inv,
            "proj_wall_view": viewwallet,
            "proj_wall_add": addwallet,
            "proj_wall_edit": editwallet,
            "proj_wall_can_delete": deletewallet,
            "proj_inves_view": view_proj_inv,
            "proj_inves_add": add_proj_inv,
            "proj_inves_edit": edit_proj_inv,
            "proj_inves_can_delete": delete_proj_inv,
            "proj_exp_view": view_proj_exp,
            "proj_exp_add": add_proj_exp,
            "proj_exp_edit": edit_proj_exp,
            "proj_exp_can_delete": delete_proj_exp,
            "proj_sales_view": view_proj_profit,
            "proj_sales_add": add_proj_profit,
            "proj_sales_edit": edit_proj_profit,
            "proj_sales_can_delete": delete_proj_profit,
            "proj_settlement_view": view_proj_setle,
            "proj_settlement_add": add_proj_setle,
            "proj_settlement_edit": edit_proj_setle,
            "proj_settlement_can_delete": delete_proj_setle,
            "status": status_per,
        }
        create_log = staff_logs.objects.create(
            company_name=cmp_name,
            company_code=code,
            username=username_staff,
            password="******",
            ip_address=request.META["REMOTE_ADDR"],
            action="Permissions",
            action_data=temp_data,
            user=request.user,
        )

        data["form_is_valid"] = True
        data["permissions"] = True

        books = Staff.objects.all()
        data["html_book_list"] = render_to_string(
            "admin_dash_menu/pages/staff/staff.html", {"books": books}
        )
    mymodel = get_object_or_404(Staff, pk=pk)
    name_of_staff = mymodel.username
    name_of_code = mymodel.company_code
    name_of_comapny = mymodel.company_name
    project_permissions = get_object_or_404(
        Project_menu, staff_name=name_of_staff, company_code=name_of_code
    )
    investor_permissions = get_object_or_404(
        Investor_menu, staff_name=name_of_staff, company_code=name_of_code
    )
    wallet_permissions = get_object_or_404(
        Investor_wallet_menu, staff_name=name_of_staff, company_code=name_of_code
    )
    pro_inv_permissions = get_object_or_404(
        Project_investor_menu, staff_name=name_of_staff, company_code=name_of_code
    )
    pro_exp_permissions = get_object_or_404(
        Project_Exp_menu, staff_name=name_of_staff, company_code=name_of_code
    )
    pro_profit_permissions = get_object_or_404(
        Project_Profit_menu, staff_name=name_of_staff, company_code=name_of_code
    )
    dashbord_permissions = get_object_or_404(
        Dashbord_view, staff_name=name_of_staff, company_code=name_of_code
    )
    settlement_permissions = get_object_or_404(
        Project_settlement_menu, staff_name=name_of_staff, company_code=name_of_code
    )
    Reports_permissions = get_object_or_404(
        Report_view, staff_name=name_of_staff, company_code=name_of_code
    )

    context = {
        "mymodel": mymodel,
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
    data["html_form"] = render_to_string(
        "admin_dash_menu/pages/staff/add_per.html", context, request=request
    )
    return JsonResponse(data)


@login_required
def get_company_staff(request):
    if request.user.is_authenticated:
        current_company = Company_table.objects.get(email_id=request.user)
        comp_name = current_company.company_name
        comp_code = current_company.company_code
        current_projects = Staff.objects.filter(company_code=comp_code, satus=True)
        project_list = [{"invs_name": p.username} for p in current_projects]
        return JsonResponse({"projects": project_list})
    else:
        return JsonResponse({"error": "User is not authenticated"})


@login_required
@csrf_protect
def view_permisions_staff(request, pk):
    data = dict()
    my_model_instances = get_object_or_404(Staff, pk=pk)
    staffname = my_model_instances.username
    company_code = my_model_instances.company_code
    project_per = get_object_or_404(
        Project_menu, staff_name=staffname, company_code=company_code
    )
    investor_permissions = get_object_or_404(
        Investor_menu, staff_name=staffname, company_code=company_code
    )
    wallet_permissions = get_object_or_404(
        Investor_wallet_menu, staff_name=staffname, company_code=company_code
    )
    pro_inv_permissions = get_object_or_404(
        Project_investor_menu, staff_name=staffname, company_code=company_code
    )
    pro_exp_permissions = get_object_or_404(
        Project_Exp_menu, staff_name=staffname, company_code=company_code
    )
    pro_profit_permissions = get_object_or_404(
        Project_Profit_menu, staff_name=staffname, company_code=company_code
    )
    dashbord_permissions = get_object_or_404(
        Dashbord_view, staff_name=staffname, company_code=company_code
    )
    settlement_permissions = get_object_or_404(
        Project_settlement_menu, staff_name=staffname, company_code=company_code
    )
    Reports_permissions = get_object_or_404(
        Report_view, staff_name=staffname, company_code=company_code
    )

    context = {
        "my_model_instances": my_model_instances,
        "project_per": project_per,
        "investor_permissions": investor_permissions,
        "wallet_permissions": wallet_permissions,
        "pro_inv_permissions": pro_inv_permissions,
        "pro_exp_permissions": pro_exp_permissions,
        "pro_profit_permissions": pro_profit_permissions,
        "dashbord_permissions": dashbord_permissions,
        "settlement_permissions": settlement_permissions,
        "Reports_permissions": Reports_permissions,
    }

    template_name = "admin_dash_menu/pages/staff/view_per.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# ------------------------------------------------- Staff LOG ------------------------------------------------


@login_required
@csrf_protect
def company_logs_staff(request):
    s = request.user
    try:
        check_com = Company_table.objects.get(email_id=s, delete_status=False)
        code = check_com.company_code
        name = check_com.company_name
        sts = "Admin"
        proj_log = staff_logs.objects.filter(company_code=code)
        context = {"name": name, "satus": sts, "proj_logs": proj_log, "company": name}
        return render(request, "admin_dash_menu/pages/logs/staff_log.html", context)
    except Company_table.DoesNotExist:
        return redirect("notallowed")


@login_required
@csrf_protect
def view_logs_staff(request, pk):
    data = dict()
    mydata = staff_logs.objects.get(pk=pk)
    my_model_instances = mydata.action_data
    context = {
        "my_model_instances": my_model_instances,
    }
    template_name = "admin_dash_menu/pages/logs/staff_log_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def view_logs_staff_permission(request, pk):
    data = dict()
    mydata = staff_logs.objects.get(pk=pk)
    my_model_instances = mydata.action_data

    print(my_model_instances)
    context = {
        "my_model_instances": my_model_instances,
    }
    template_name = "admin_dash_menu/pages/logs/staff_log_view_per.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
