from django.shortcuts import render, get_object_or_404, redirect
from Application.models import *
from Application.forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


@login_required
@csrf_protect
def view_investor(request, pk):
    data = dict()
    my_model_instances = get_object_or_404(Investors, pk=pk, delete_status=False)
    context = {"my_model_instances": my_model_instances}

    template_name = "admin_dash_menu/pages/investors/investore_view.html"
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def investors_list(request):
    try:
        s = request.user
        check_inv = Company_table.objects.get(email_id=s)
        code = check_inv.company_code
        name = check_inv.company_name
        my_model_instances = Investors.objects.filter(
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
                request, "admin_dash_menu/pages/investors/Investors.html", context
            )

        else:
            pass
    except Company_table.DoesNotExist:
        check = Staff.objects.get(username=s)
        code = check.company_code
        name = check.company_name
        staf_name = check.username
        my_model_instances = Investors.objects.filter(
            company_code=code, delete_status=False
        )

        investor_per = Investor_menu.objects.get(
            staff_name=staf_name, company_code=code
        )
        if investor_per.status:
            if (
                investor_per.add
                or investor_per.view
                or investor_per.edit
                or investor_per.can_delete
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
                    "my_model_instances": my_model_instances,
                    "investor_per": investor_per,
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
                    request, "admin_dash_menu/pages/investors/Investors.html", context
                )
            else:
                return redirect("notallowed")
        else:
            return redirect("notallowed")

    return redirect("notallowed")


@login_required
@csrf_protect
def save_investor_form(request, form, template_name, pk):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            data["update"] = True
            inves_data = get_object_or_404(Investors, pk=pk)
            investor_data = {
                "company_name": inves_data.company_name,
                "first_name": inves_data.first_name,
                "last_name": inves_data.last_name,
                "Display_name": inves_data.Display_name,
                "email_id": inves_data.email_id,
                "user_name": inves_data.user_name,
                "password": inves_data.password,
                "mobile_number": inves_data.mobile_number,
                "Pan_number": inves_data.Pan_number,
                "Aadhar_card_no": inves_data.Aadhar_card_no,
                "contact_address": inves_data.contact_address,
                "City": inves_data.City,
                "State": inves_data.State,
                "pincode": inves_data.pincode,
                "status": inves_data.status,
            }
            create_log = InvestorLog.objects.create(
                email_id=inves_data.email_id,
                password=inves_data.password,
                company_name=inves_data.company_name,
                company_code=inves_data.company_code,
                investors_code=inves_data.investors_code,
                ip_address=request.META.get("REMOTE_ADDR"),
                action="Updated",
                action_data=investor_data,
                user=request.user,
            )

            books = Investors.objects.all()
            data["html_book_list"] = render_to_string(
                "admin_dash_menu/pages/investors/Investors.html", {"books": books}
            )
        else:
            data["form_is_valid"] = False

    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@csrf_protect
def investors_create(request):
    data = dict()
    form = InvestorRegistationForm()
    if request.method == "POST":
        company_id = request.user
        try:
            email_id = request.POST["email_id"]
            get_com_name = Company_table.objects.get(email_id=company_id)
        except Company_table.DoesNotExist:
            get_com_name = None
            staff_login = Staff.objects.get(username=company_id)
            checkcompany = staff_login.company_name
            get__name = Company_table.objects.get(company_name=checkcompany)
            get_com_name = get__name
        try:
            check_data = Investors.objects.get(
                email_id=email_id,
                company_code=get_com_name.company_code,
                delete_status=False,
            )
            if check_data is not None:
                context = {"error": "☹ User id Already Exists!"}

                return JsonResponse(context, status=400)
            else:
                pass
        except Investors.DoesNotExist:
            code = get_com_name.company_code
            cmp_name = get_com_name.company_name
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            Display_name = request.POST["Display_name"]
            password = request.POST["password"]
            mobile_number = request.POST["mobile_number"]
            Pan_number = request.POST["Pan_number"]
            Aadhar_card_no = request.POST["Aadhar_card_no"]
            contact_address = request.POST["contact_address"]
            City = request.POST["City"]
            State = request.POST["State"]
            pincode = request.POST["pincode"]

            investor_save = Investors.objects.create(
                company_name=cmp_name,
                company_code=code,
                first_name=first_name,
                last_name=last_name,
                Display_name=Display_name,
                email_id=email_id,
                user_name=first_name,
                password=password,
                mobile_number=mobile_number,
                Pan_number=Pan_number,
                Aadhar_card_no=Aadhar_card_no,
                contact_address=contact_address,
                City=City,
                State=State,
                pincode=pincode,
                status=True,
            )

            try:
                user = User.objects.get(username=email_id)
            except User.DoesNotExist:
                user = User.objects.create_user(username=email_id, password=password)
            user.save()
            investor_save.save()
            investor_data = {
                "company_name": investor_save.company_name,
                "first_name": investor_save.first_name,
                "last_name": investor_save.last_name,
                "Display_name": investor_save.Display_name,
                "email_id": investor_save.email_id,
                "user_name": investor_save.user_name,
                "password": investor_save.password,
                "mobile_number": investor_save.mobile_number,
                "Pan_number": investor_save.Pan_number,
                "Aadhar_card_no": investor_save.Aadhar_card_no,
                "contact_address": investor_save.contact_address,
                "City": investor_save.City,
                "State": investor_save.State,
                "pincode": investor_save.pincode,
                "status": investor_save.status,
            }
            create_log = InvestorLog.objects.create(
                email_id=investor_save.email_id,
                password=investor_save.password,
                company_name=investor_save.company_name,
                company_code=investor_save.company_code,
                investors_code=investor_save.investors_code,
                ip_address=request.META.get("REMOTE_ADDR"),
                action="Created",
                action_data=investor_data,
                user=request.user,
            )

        data["form_is_valid"] = True
        data["add"] = True

        books = Investors.objects.all()
        data["html_book_list"] = render_to_string(
            "admin_dash_menu/pages/investors/Investors.html", {"books": books}
        )
    else:
        data["form_is_valid"] = False

    context = {"form": form}
    data["html_form"] = render_to_string(
        "admin_dash_menu/pages/investors/investor_reg.html", context, request=request
    )
    return JsonResponse(data)


@login_required
@csrf_protect
def investors_update(request, pk):
    book = get_object_or_404(Investors, pk=pk)
    old_username = book.email_id
    if request.method == "POST":
        email = request.POST["email_id"]
        password = request.POST["password"]
        if old_username != email:
            user = User.objects.get(username=old_username)
            user.username = email
            user.set_password(password)
            user.save()
        form = InvestorRegistationForm(request.POST, instance=book)
    else:
        form = InvestorRegistationForm(instance=book)
    return save_investor_form(
        request, form, "admin_dash_menu/pages/investors/investor_edit.html", pk
    )


@login_required
@csrf_protect
def delete_investors(request, pk):
    mymodel = Investors.objects.get(pk=pk)
    check_data = Invesments_Db.objects.filter(investor_code=mymodel.investors_code)
    if check_data.exists():
        context = {
            "error": "☹ This Investor has started  Invesment,So you can not delete!"
        }
        return JsonResponse(context, status=400)
    elif not check_data.exists():
        check_wallet = Investor_Wallet_Details.objects.filter(
            investor_id=mymodel.investors_code
        )
        if check_wallet.exists():
            context = {"error": "☹ This Investor has Wallet,So you can not delete!"}
            return JsonResponse(context, status=400)
        elif not check_wallet.exists():
            if check_data.count() == 1:
                mymodel_user = User.objects.get(username=mymodel.email_id)
                trashed_data = TrashedData.objects.create(
                    user=request.user,
                    original_data=mymodel.__dict__,
                )

                investor_data = {
                    "company_name": mymodel.company_name,
                    "first_name": mymodel.first_name,
                    "last_name": mymodel.last_name,
                    "Display_name": mymodel.Display_name,
                    "email_id": mymodel.email_id,
                    "user_name": mymodel.user_name,
                    "password": mymodel.password,
                    "mobile_number": mymodel.mobile_number,
                    "Pan_number": mymodel.Pan_number,
                    "Aadhar_card_no": mymodel.Aadhar_card_no,
                    "contact_address": mymodel.contact_address,
                    "City": mymodel.City,
                    "State": mymodel.State,
                    "pincode": mymodel.pincode,
                    "status": mymodel.status,
                }
                create_log = InvestorLog.objects.create(
                    email_id=mymodel.email_id,
                    password=mymodel.password,
                    company_name=mymodel.company_name,
                    company_code=mymodel.company_code,
                    investors_code=mymodel.investors_code,
                    ip_address=request.META.get("REMOTE_ADDR"),
                    action="Deleted",
                    action_data=investor_data,
                    user=request.user,
                )
                mymodel.delete()
                mymodel_user.delete()
            else:
                investor_data = {
                    "company_name": mymodel.company_name,
                    "first_name": mymodel.first_name,
                    "last_name": mymodel.last_name,
                    "Display_name": mymodel.Display_name,
                    "email_id": mymodel.email_id,
                    "user_name": mymodel.user_name,
                    "password": mymodel.password,
                    "mobile_number": mymodel.mobile_number,
                    "Pan_number": mymodel.Pan_number,
                    "Aadhar_card_no": mymodel.Aadhar_card_no,
                    "contact_address": mymodel.contact_address,
                    "City": mymodel.City,
                    "State": mymodel.State,
                    "pincode": mymodel.pincode,
                    "status": mymodel.status,
                }
                create_log = InvestorLog.objects.create(
                    email_id=mymodel.email_id,
                    password=mymodel.password,
                    company_name=mymodel.company_name,
                    company_code=mymodel.company_code,
                    investors_code=mymodel.investors_code,
                    ip_address=request.META.get("REMOTE_ADDR"),
                    action="Deleted",
                    action_data=investor_data,
                    user=request.user,
                )
                mymodel.delete()

            return JsonResponse({"status": "ok"})
