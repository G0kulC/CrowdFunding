from django.shortcuts import render, get_object_or_404, redirect
from Application.models import *
from Application.forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


@login_required
@csrf_protect
def project_list(request):
    s = request.user
    try:
        check_com = Company_table.objects.get(email_id=s, delete_status=False)
        code = check_com.company_code
        name = check_com.company_name
        sts = "Admin"
        if check_com is not None:
            my_model_instances = Project.objects.filter(
                company_code=code, delete_status=False
            )
            context = {
                "my_model_instances": my_model_instances,
                "name": name,
                "satus": sts,
                "company": name,
            }
            return render(
                request, "admin_dash_menu/pages/project/Project_tables.html", context
            )
        else:
            pass
    except Company_table.DoesNotExist:
        check = Staff.objects.get(username=s)
        code = check.company_code
        name = check.company_name
        staf_name = check.username
        my_model_instances = Project.objects.filter(
            company_code=code, delete_status=False
        )
        project_per = Project_menu.objects.get(staff_name=staf_name, company_code=code)
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

        if project_per.status:
            if (
                project_per.add
                or project_per.view
                or project_per.edit
                or project_per.can_delete
            ):
                sts = "Staff"
                staff = True
                context = {
                    "my_model_instances": my_model_instances,
                    "project_per": project_per,
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
                    "admin_dash_menu/pages/project/Project_tables.html",
                    context,
                )
            else:
                return redirect("notallowed")
        else:
            return redirect("notallowed")


@login_required
@csrf_protect
def save_project_form(request, form, template_name, pk):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            data["update"] = True
            proj = get_object_or_404(Project, pk=pk)

            project_data = {
                "company_name": proj.company_name,
                "project_name": proj.project_name,
                "Project_location": proj.Project_location,
                "Latitude": proj.Latitude,
                "Longitude": proj.Longitude,
                "Project_value": proj.Project_value,
                "Kickoff_date": proj.Kickoff_date,
                "Returns_projection_type": proj.Returns_projection_type,
                "Returns_projection_value": proj.Returns_projection_value,
                "total_unit_value": proj.total_unit_value,
                "Other_expense": proj.Other_expense,
                "Total_share": proj.Total_share,
                "Per_share_value": proj.Per_share_value,
                "share_count": proj.share_count,
                "Expected_return_date": proj.Expected_return_date,
                "status": proj.status,
            }
            project_log = ProjectLog.objects.create(
                company_name=proj.company_name,
                company_code=proj.company_code,
                project_name=proj.project_name,
                project_code=proj.prject_key,
                ip_address=request.META["REMOTE_ADDR"],
                action="Updated",
                action_data=project_data,
                user=request.user,
            )
            books = Project.objects.all()
            data["html_book_list"] = render_to_string(
                "admin_dash_menu/pages/project/Project_tables.html", {"books": books}
            )
        else:
            data["form_is_valid"] = False

    context = {
        "form": form,
    }
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def project_update(request, pk):
    book = get_object_or_404(Project, pk=pk, delete_status=False)
    if request.method == "POST":
        form = Project_create_Form(request.POST, instance=book)
    else:
        form = Project_create_Form(instance=book)
    return save_project_form(
        request, form, "admin_dash_menu/pages/project/project_edit.html", pk
    )


@login_required
@csrf_protect
def project_create(request):
    data = dict()
    form = Project_create_Form()
    get_com_name = None
    if request.method == "POST":
        try:
            get_com_name = Company_table.objects.get(email_id=request.user)
            if get_com_name is not None:
                code = get_com_name.company_code

                cmp_name = get_com_name.company_name
            else:
                pass
        except Company_table.DoesNotExist:
            get_com_name = None
            get_com_name = Staff.objects.get(username=request.user)
            if get_com_name is not None:
                code = get_com_name.company_code
                cmp_name = get_com_name.company_name
        try:
            project_name = request.POST["project_name"]
            check_data = Project.objects.get(
                project_name=project_name, company_code=code, delete_status=False
            )
            if check_data is not None:
                data["error_message"] = "Project name already exists"
                return JsonResponse(data)

        except Project.DoesNotExist:
            Project_location = request.POST.get("Project_location")
            Latitude = request.POST.get("Latitude")
            Longitude = request.POST.get("Longitude")
            try:
                Project_value = int(request.POST.get("Project_value"))
            except (ValueError, TypeError):
                Project_value = 0

            try:
                Kickoff_date = request.POST.get("Kickoff_date")
            except (ValueError, TypeError):
                Kickoff_date = None

            try:
                returns_projection_type = request.POST.get("Returns_projection_type")
                if returns_projection_type == "":
                    returns_projection_type = 0
                else:
                    returns_projection_type = returns_projection_type
            except (ValueError, TypeError):
                returns_projection_type = 0

            try:
                returns_projection_value = int(
                    request.POST.get("Returns_projection_value")
                )
                if returns_projection_value == "":
                    returns_projection_value = 0
                else:
                    returns_projection_value = returns_projection_value
            except (ValueError, TypeError):
                returns_projection_value = 0

            try:
                total_unit_value = int(request.POST.get("total_unit_value"))
            except (ValueError, TypeError):
                total_unit_value = 0

            try:
                other_expense = int(request.POST.get("Other_expense"))
            except (ValueError, TypeError):
                other_expense = 0

            try:
                total_share = int(request.POST.get("Total_share"))
            except (ValueError, TypeError):
                total_share = 0

            try:
                per_share_value = int(request.POST.get("Per_share_value"))
            except (ValueError, TypeError):
                per_share_value = 0

            try:
                share_count = int(request.POST.get("share_count"))
            except (ValueError, TypeError):
                share_count = 0

            try:
                expected_return_date = request.POST.get("Expected_return_date")
            except (ValueError, TypeError):
                expected_return_date = 0

            status = request.POST.get("status", False)

            project_save = Project.objects.create(
                company_name=cmp_name,
                company_code=code,
                project_name=project_name,
                Project_location=Project_location,
                Latitude=Latitude,
                Longitude=Longitude,
                Project_value=Project_value,
                Kickoff_date=Kickoff_date,
                Returns_projection_type=returns_projection_type,
                Returns_projection_value=returns_projection_value,
                total_unit_value=total_unit_value,
                Other_expense=other_expense,
                Total_share=total_share,
                Per_share_value=per_share_value,
                share_count=share_count,
                Expected_return_date=expected_return_date,
                status=status,
            )
            project_data = {
                "company_name": project_save.company_name,
                "project_name": project_save.project_name,
                "Project_location": project_save.Project_location,
                "Latitude": project_save.Latitude,
                "Longitude": project_save.Longitude,
                "Project_value": project_save.Project_value,
                "Kickoff_date": project_save.Kickoff_date,
                "Returns_projection_type": project_save.Returns_projection_type,
                "Returns_projection_value": project_save.Returns_projection_value,
                "total_unit_value": project_save.total_unit_value,
                "Other_expense": project_save.Other_expense,
                "Total_share": project_save.Total_share,
                "Per_share_value": project_save.Per_share_value,
                "share_count": project_save.share_count,
                "Expected_return_date": project_save.Expected_return_date,
                "status": project_save.status,
            }

            project_log = ProjectLog.objects.create(
                company_name=cmp_name,
                company_code=code,
                project_name=project_name,
                project_code=project_save.prject_key,
                ip_address=request.META["REMOTE_ADDR"],
                action="Created",
                action_data=project_data,
                user=request.user,
            )
            project_save.save()

        data["form_is_valid"] = True
        data["add"] = True
        books = Project.objects.all()
        data["html_book_list"] = render_to_string(
            "admin_dash_menu/pages/project/Project_tables.html", {"books": books}
        )
    else:
        data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(
        "admin_dash_menu/pages/project/project_reg.html", context, request=request
    )
    return JsonResponse(data)


@login_required
@csrf_protect
def delete_project(request, pk):
    mymodel = get_object_or_404(Project, pk=pk)
    trashed_data = TrashedData.objects.create(
        user=request.user,
        original_data=mymodel.__dict__,
    )
    try:
        check_invesment = Invesments_Db.objects.filter(
            project_code=mymodel.prject_key, company_code=mymodel.company_code
        ).latest("id")
        if check_invesment is not None:
            context = {"error": "☹ Sorry! This project has Invesments."}
        return JsonResponse(context, status=400)
    except Invesments_Db.DoesNotExist:
        pass

    try:
        check_exp = ProjectExpense.objects.filter(
            project_code=mymodel.prject_key, company_code=mymodel.company_code
        ).latest("id")
        if check_exp is not None:
            context = {"error": "☹ Sorry! This project has Expenses."}
        return JsonResponse(context, status=400)
    except ProjectExpense.DoesNotExist:
        pass
    try:
        check_log = ProjectSales.objects.filter(
            project_code=mymodel.prject_key, company_code=mymodel.company_code
        ).latest("id")
        if check_log is not None:
            context = {"error": "☹ Sorry! This project has Sales."}
        return JsonResponse(context, status=400)
    except ProjectSales.DoesNotExist:
        project_data = {
            "company_name": mymodel.company_name,
            "project_name": mymodel.project_name,
            "Project_location": mymodel.Project_location,
            "Latitude": mymodel.Latitude,
            "Longitude": mymodel.Longitude,
            "Project_value": mymodel.Project_value,
            "Kickoff_date": mymodel.Kickoff_date,
            "Returns_projection_type": mymodel.Returns_projection_type,
            "Returns_projection_value": mymodel.Returns_projection_value,
            "total_unit_value": mymodel.total_unit_value,
            "Other_expense": mymodel.Other_expense,
            "Total_share": mymodel.Total_share,
            "Per_share_value": mymodel.Per_share_value,
            "share_count": mymodel.share_count,
            "Expected_return_date": mymodel.Expected_return_date,
            "status": mymodel.status,
        }
        project_log = ProjectLog.objects.create(
            company_name=mymodel.company_name,
            company_code=mymodel.company_code,
            project_name=mymodel.project_name,
            project_code=mymodel.prject_key,
            ip_address=request.META["REMOTE_ADDR"],
            action="Deleted",
            action_data=project_data,
            user=request.user,
        )
        # mymodel.delete_status = True
        mymodel.delete()
        return JsonResponse({"status": "ok"})


@login_required
@csrf_protect
def view_project(request, pk):
    data = dict()
    my_model_instances = get_object_or_404(Project, pk=pk, delete_status=False)
    context = {
        "my_model_instances": my_model_instances,
    }

    template_name = "admin_dash_menu/pages/project/project_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def get_project_name_edit(request, pk):
    data = dict()
    cmy_model_instances = Project.objects.get(pk=pk, delete_status=False)
    get_code = cmy_model_instances.prject_key
    try:
        check = Invesments_Db.objects.filter(project_code=get_code).latest("id")
        if check is not None:
            data["investment"] = True
            return JsonResponse(data)
    except Invesments_Db.DoesNotExist:
        data["investment"] = False
        return JsonResponse(data)

    try:
        check_exp = ProjectExpense.objects.filter(project_code=get_code).latest("id")
        if check_exp is not None:
            data["Expense"] = True
            return JsonResponse(data)
    except ProjectExpense.DoesNotExist:
        data["Expense"] = False
        return JsonResponse(data)

    try:
        check_sales = ProjectSales.objects.filter(project_code=get_code).latest("id")
        if check_sales is not None:
            data["sales"] = True
            return JsonResponse(data)
    except ProjectSales.DoesNotExist:
        data["sales"] = False
        return JsonResponse(data)


@login_required
@csrf_protect
def get_total_share_edit(request, pk):
    data = dict()
    cmy_model_instances = Project.objects.get(pk=pk, delete_status=False)
    get_code = cmy_model_instances.prject_key
    try:
        check = Invesments_Db.objects.filter(project_code=get_code).latest("id")
        if check is not None:
            if cmy_model_instances.share_count == 0:
                data["investment"] = True
    except Invesments_Db.DoesNotExist:
        data["investment"] = False
    return JsonResponse(data)


@login_required
@csrf_protect
def check_project_investment(request, pk):
    data = dict()
    cmy_model_instances = Project.objects.get(pk=pk, delete_status=False)
    get_code = cmy_model_instances.prject_key
    try:
        check = Invesments_Db.objects.filter(project_code=get_code).latest("id")
        if check is not None:
            data["investment"] = True
    except Invesments_Db.DoesNotExist:
        data["investment"] = False
    return JsonResponse(data)
