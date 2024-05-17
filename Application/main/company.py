from django.shortcuts import render, get_object_or_404
from Application.models import *
from Application.forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required
@csrf_protect
def view_company(request, pk):
    data = dict()
    my_model_instances = get_object_or_404(Company_table, pk=pk)
    context = {"my_model_instances": my_model_instances}

    template_name = "admin_dash_menu/pages/company/company_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def get_company_name_edit(request, company_name, pk):
    data = dict()
    cmy_model_instances = Company_table.objects.get(pk=pk, delete_status=False)
    try:
        check = Company_table.objects.get(company_name=company_name)
        if check.pk == cmy_model_instances.pk:
            data["error"] = False
        else:
            data["error"] = True

    except Company_table.DoesNotExist:
        data["error"] = False

    return JsonResponse(data)


@login_required
@csrf_protect
def get_company_email_edit(request, email, pk):
    data = dict()
    cmy_model_instances = Company_table.objects.get(pk=pk, delete_status=False)
    try:
        check = Company_table.objects.get(email_id=email)
        if check.pk == cmy_model_instances.pk:
            data["error"] = False
        else:
            data["error"] = True

    except Company_table.DoesNotExist:
        data["error"] = False

    return JsonResponse(data)


@login_required
@csrf_protect
def get_company_num_edit(request, mob, pk):
    data = dict()
    cmy_model_instances = Company_table.objects.get(pk=pk, delete_status=False)
    try:
        check = Company_table.objects.get(contact_number=mob)
        if check.pk == cmy_model_instances.pk:
            data["error"] = False
        else:
            data["error"] = False

    except Company_table.DoesNotExist:
        data["error"] = False

    return JsonResponse(data)


@login_required
@csrf_protect
def get_company_email(request, company_email):
    data = dict()
    my_model_instances = Company_table.objects.filter(
        email_id=company_email, delete_status=False
    )
    if my_model_instances.exists():
        data["error"] = True
    return JsonResponse(data)


@login_required
@csrf_protect
def get_company_mobile(request, company_mobile):
    data = dict()
    cmy_model_instances = Company_table.objects.filter(
        contact_number=company_mobile, delete_status=False
    )
    if cmy_model_instances.exists():
        data["error"] = True
    return JsonResponse(data)


@login_required
@csrf_protect
def get_company_name(request, company_name):
    data = dict()
    cmy_model_instances = Company_table.objects.filter(
        company_name=company_name, delete_status=False
    )
    if cmy_model_instances.exists():
        data["error"] = True
    return JsonResponse(data)


@login_required
@csrf_protect
def company_list(request):
    s = request.user
    satus = request.user.is_staff
    admin = request.user.is_superuser
    if admin == 1:
        sts = "Super Admin"
    elif satus == 1:
        sts = "Staff"
    else:
        sts = "Investor"
    get_my_model_instances = Company_table.objects.filter(delete_status=False)
    paginator = Paginator(get_my_model_instances, 10)  # 10 items per page
    page = request.GET.get("page")
    my_model_instances = paginator.get_page(page)
    return render(
        request,
        "admin_dash_menu/pages/company/Company_tables.html",
        {"my_model_instances": my_model_instances, "name": s, "satus": sts},
    )


@login_required
@csrf_protect
def save_comapany_form(request, form, template_name, add, update):
    data = dict()
    print(add, update)
    if request.method == "POST":
        if form.is_valid():
            data["form_is_valid"] = True
            form.save()
            temp_data = Company_table.objects.get(pk=form.instance.pk)
            main_data = {}
            if add == True:
                email_id = request.POST["email_id"]
                password = request.POST["password"]
                main_data = {
                    "company_name": temp_data.company_name,
                    "email_id": temp_data.email_id,
                    "password": temp_data.password,
                    "contact_number": temp_data.contact_number,
                    "company_pan": temp_data.company_pan,
                    "gstin": temp_data.gstin,
                    "Company_addresss": temp_data.Company_addresss,
                    "City": temp_data.City,
                    "State": temp_data.State,
                    "pincode": temp_data.pincode,
                    "status": temp_data.status,
                    "created_at": str(temp_data.created_at.strftime("%Y-%m-%d")),
                }

                action = "Created"
                user = request.user
                create_log = CompanyLog.objects.create(
                    email_id=email_id,
                    password=password,
                    company=form.instance.company_name,
                    ip_address=request.META.get("REMOTE_ADDR"),
                    action=action,
                    action_data=main_data,
                    user=user,
                )
                data["add"] = True
                return JsonResponse(data)
            if update == True:
                email_id = request.POST["email_id"]
                password = request.POST["password"]
                main_data = {
                    "company_name": temp_data.company_name,
                    "email_id": temp_data.email_id,
                    "password": temp_data.password,
                    "contact_number": temp_data.contact_number,
                    "company_pan": temp_data.company_pan,
                    "gstin": temp_data.gstin,
                    "Company_addresss": temp_data.Company_addresss,
                    "City": temp_data.City,
                    "State": temp_data.State,
                    "pincode": temp_data.pincode,
                    "status": temp_data.status,
                    "created_at": str(temp_data.created_at.strftime("%Y-%m-%d")),
                }

                action = "Updated"
                user = request.user
                create_log = CompanyLog.objects.create(
                    email_id=email_id,
                    password=password,
                    company=form.instance.company_name,
                    ip_address=request.META.get("REMOTE_ADDR"),
                    action=action,
                    action_data=main_data,
                    user=user,
                )
                data["update"] = True
                return JsonResponse(data)
        else:
            data["form_is_valid"] = False
            for field_name, errors in form.errors.items():
                for error in errors:
                    print(f"Error in field '{field_name}': {error}")
            data = {"error": errors}
            return JsonResponse(data)
    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def company_create(request):
    if request.method == "POST":
        form = CompanyRegistationForm(request.POST)
        email = request.POST["email_id"]
        try:
            trash_copany = Company_table.objects.filter(
                email_id=email, delete_status=True
            )
            trash_log = CompanyLog.objects.filter(
                email_id=email, perment_delete=False, action="Deleted"
            ).latest("id")
            trash_log.perment_delete = True
            trash_log.save()
            trash_copany.delete()
        except CompanyLog.DoesNotExist:
            pass
        if form.is_valid():
            password = request.POST["password"]
            user = User.objects.create(username=email)
            user.set_password(password)
            user.save()
    else:
        form = CompanyRegistationForm()
    add = True
    update = False
    return save_comapany_form(
        request, form, "admin_dash_menu/pages/company/company_reg.html", add, update
    )


@login_required
@csrf_protect
def company_updates(request, pk):
    book = get_object_or_404(Company_table, pk=pk)
    old_username = book.email_id
    if request.method == "POST":
        email = request.POST["email_id"]
        password = request.POST["password"]
        user = User.objects.get(username=old_username)
        user.username = email
        user.set_password(password)
        user.save()
        form = CompanyRegistationForm(request.POST, instance=book)

    else:
        form = CompanyRegistationForm(instance=book)
    add = False
    update = True
    return save_comapany_form(
        request, form, "admin_dash_menu/pages/company/comapany_edit.html", add, update
    )


@login_required
@csrf_protect
def delete_comapany(request, pk):
    data = dict()
    mymodel = get_object_or_404(Company_table, pk=pk)
    trashed_data = TrashedData.objects.create(
        user=request.user,
        original_data=mymodel.__dict__,
    )
    project_delete = Project.objects.filter(company_code=mymodel.company_code)
    investor_delete = Investors.objects.filter(company_code=mymodel.company_code)
    inves_wallet_delete = Investor_Wallet_Details.objects.filter(
        company_code=mymodel.company_code
    )
    proj_inves_delete = Invesments_Db.objects.filter(company_code=mymodel.company_code)
    proj_exp = ProjectExpense.objects.filter(company_code=mymodel.company_code)
    proj_sales = ProjectSales.objects.filter(company_code=mymodel.company_code)
    proj_settlement = Projectsettlement.objects.filter(
        company_code=mymodel.company_code
    )
    comp_staff = Staff.objects.filter(company_code=mymodel.company_code)
    if (
        project_delete.count() == 0
        and investor_delete.count() == 0
        and inves_wallet_delete.count() == 0
        and proj_inves_delete.count() == 0
        and proj_exp.count() == 0
        and proj_sales.count() == 0
        and proj_settlement.count() == 0
        and comp_staff.count() == 0
    ):
        myuser = User.objects.get(username=mymodel.email_id)
        myuser.delete()
        main_data = {
            "company_name": mymodel.company_name,
            "email_id": mymodel.email_id,
            "password": mymodel.password,
            "contact_number": mymodel.contact_number,
            "company_pan": mymodel.company_pan,
            "gstin": mymodel.gstin,
            "Company_addresss": mymodel.Company_addresss,
            "City": mymodel.City,
            "State": mymodel.State,
            "pincode": mymodel.pincode,
            "status": mymodel.status,
            "created_at": str(mymodel.created_at.strftime("%Y-%m-%d")),
        }

        action = "Deleted"
        user = request.user
        create_log = CompanyLog.objects.create(
            email_id=mymodel.email_id,
            password=mymodel.password,
            company=mymodel.company_name,
            ip_address=request.META.get("REMOTE_ADDR"),
            action=action,
            action_data=main_data,
            user=user,
        )

        mymodel.delete()
        data["delete"] = True
        return JsonResponse(data)

    else:
        print("Not Deleted")
        data["data_found"] = True
        return JsonResponse(data)
