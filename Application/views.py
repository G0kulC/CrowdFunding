from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from Application.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.db.models import Count
import csv
from django.http import HttpResponse
import xlwt
import io
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


def handler404(request, exception):
    b = request.user.is_authenticated
    if b == 0:
        return redirect("admin_login")
    elif b == True:
        return redirect("base")


def handler500(request, *args, **argv):
    return render(request, "admin_dash_menu/error/404.html", status=500)


def Notallowed(request):
    return render(request, "admin_dash_menu/error/not.html")


@login_required
@csrf_protect
def download_data_history_sales(request, project_name, file_format):
    if request.user.is_authenticated:
        company_id = request.user
        try:
            get_com_name = Company_table.objects.get(email_id=company_id)
            code = get_com_name.company_code
            cmp_name = get_com_name.company_name
        except Company_table.DoesNotExist:
            get_com_name = Staff.objects.get(username=company_id)
            code = get_com_name.company_code
            cmp_name = get_com_name.company_name
        try:
            check = ProjectSales.objects.filter(
                project_name=project_name, company_code=code
            ).latest("sales_date")
            project_sales_history = ProjectSales.objects.filter(
                project_code=check.project_code, company_code=code
            )
        except ProjectSales.DoesNotExist:
            project_sales_history = []
        if file_format == "xls":
            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("Project Sales History")
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = [
                "Project Name",
                "Unit of Sales",
                "Selled Amount",
                "Approved",
                "Selled Date",
            ]
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            for row in project_sales_history:
                row_num += 1
                ws.write(row_num, 0, row.project_name)
                ws.write(row_num, 1, row.unit_sold)
                ws.write(row_num, 2, row.amount)
                ws.write(row_num, 3, row.company_name)
                ws.write(row_num, 4, row.sales_date.strftime("%d-%m-%Y"))
            wb.save("Sales_report.xls")
            response = HttpResponse(content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = 'attachment; filename="Sales_report.xls"'
            with open("Sales_report.xls", "rb") as f:
                response.write(f.read())

        elif file_format == "pdf":
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="Sales_report.pdf"'
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                response, pagesize=letter, topMargin=10, bottomMargin=10
            )
            doc.title = "Project Sales History"
            data = [
                [
                    "Project Name",
                    "Unit of Sales",
                    "Selled Amount",
                    "Approved",
                    "Selled Date",
                ]
            ]
            for row in project_sales_history:
                data.append(
                    [
                        row.project_name,
                        row.unit_sold,
                        row.amount,
                        row.company_name,
                        row.sales_date.strftime("%d-%m-%Y"),
                    ]
                )
            table = Table(data)
            table.setStyle(
                TableStyle(
                    [
                        ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
                        ("BACKGROUND", (0, 0), (-1, 0), "white"),
                        ("TEXTCOLOR", (0, 0), (-1, 0), "black"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("GRID", (0, 0), (-1, -1), 0.5, "black"),
                        ("TOPPADDING", (0, 0), (-1, -1), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ]
                )
            )
            elements = [table]
            doc.build(elements)
            pdf_data = buffer.getvalue()
            buffer.close()
            response.write(pdf_data)

        elif file_format == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="Sales_report.csv"'
            writer = csv.writer(response)
            writer.writerow(
                [
                    "Project Name",
                    "Unit of Sales",
                    "Selled Amount",
                    "Approved",
                    "Selled Date",
                ]
            )
            for row in project_sales_history:
                writer.writerow(
                    [
                        row.project_name,
                        row.unit_sold,
                        row.amount,
                        row.company_name,
                        row.sales_date.strftime("%d-%m-%Y"),
                    ]
                )

        return response


@login_required
@csrf_protect
def download_data_history_wallet(request, investor_name, file_format):
    if request.user.is_authenticated:
        company_id = request.user
        try:
            get_com_name = Company_table.objects.get(email_id=company_id)
            code = get_com_name.company_code
            cmp_name = get_com_name.company_name
        except Company_table.DoesNotExist:
            get_com_name = Staff.objects.get(username=company_id)
            code = get_com_name.company_code
            cmp_name = get_com_name.company_name
        try:
            get_inves_name = Investors.objects.get(
                email_id=investor_name, company_code=code, delete_status=False
            )
            get_wallet_key = Investor_Wallet_Details.objects.get(
                investor_id=get_inves_name.investors_code
            )
            investor_wallet_details = Investor_Wallet_History_Details.objects.filter(
                wallet_key=get_wallet_key.wallet_key
            )

            if file_format == "xls":
                wb = xlwt.Workbook(encoding="utf-8")
                ws = wb.add_sheet("Investor Wallet History")
                row_num = 0
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                columns = [
                    "Investor Name",
                    "Reason",
                    "Credited Amount",
                    "Credited Time",
                    "Debited Amount",
                    "Debited Date",
                    "Total Balance",
                ]
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)
                for row in investor_wallet_details:
                    row_num += 1
                    ws.write(row_num, 0, row.investor_name)
                    ws.write(row_num, 1, row.reason)
                    ws.write(row_num, 2, row.credited_amount)
                    ws.write(row_num, 3, row.credited_time)
                    ws.write(row_num, 4, row.debited_amount)
                    ws.write(row_num, 5, row.debited_date)
                    ws.write(row_num, 6, row.total_amount)
                wb.save("wallet_history.xls")
                response = HttpResponse(content_type="application/vnd.ms-excel")
                response[
                    "Content-Disposition"
                ] = 'attachment; filename="wallet_history.xls"'
                with open("wallet_history.xls", "rb") as f:
                    response.write(f.read())

            elif file_format == "pdf":
                response = HttpResponse(content_type="application/pdf")
                response[
                    "Content-Disposition"
                ] = f'attachment; filename="wallet_history.pdf"'
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(
                    response,
                    pagesize=landscape(letter),
                    rightpadding=10,
                    leftpadding=10,
                    topMargin=10,
                    bottomMargin=10,
                )
                doc.title = "Investor Wallet History"
                data = [
                    [
                        "Investor Name",
                        "Reason",
                        "Credited Amount",
                        "Credited Time",
                        "Debited Amount",
                        "Debited Date",
                        "Total Balance",
                    ]
                ]
                for row in investor_wallet_details:
                    data.append(
                        [
                            row.investor_name,
                            row.reason,
                            row.credited_amount,
                            row.credited_time.strftime("%d-%m-%Y"),
                            row.debited_amount,
                            row.debited_date.strftime("%d-%m-%Y"),
                            row.total_amount,
                        ]
                    )
                table = Table(data)
                table.setStyle(
                    TableStyle(
                        [
                            ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
                            ("BACKGROUND", (0, 0), (-1, 0), "white"),
                            ("TEXTCOLOR", (0, 0), (-1, 0), "black"),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("GRID", (0, 0), (-1, -1), 0.5, "black"),
                            ("TOPPADDING", (0, 0), (-1, -1), 10),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                        ]
                    )
                )
                elements = [table]
                doc.build(elements)
                pdf_data = buffer.getvalue()
                buffer.close()
                response.write(pdf_data)

            elif file_format == "csv":
                response = HttpResponse(content_type="text/csv")
                response[
                    "Content-Disposition"
                ] = 'attachment; filename="wallet_history.csv"'
                writer = csv.writer(response)
                writer.writerow(
                    [
                        "Investor Name",
                        "Reason",
                        "Credited Amount",
                        "Credited Time",
                        "Debited Amount",
                        "Debited Date",
                        "Total Balance",
                    ]
                )
                for row in investor_wallet_details:
                    writer.writerow(
                        [
                            row.investor_name,
                            row.reason,
                            row.credited_amount,
                            row.credited_time.strftime("%d-%m-%Y"),
                            row.debited_amount,
                            row.debited_date.strftime("%d-%m-%Y"),
                            row.total_amount,
                        ]
                    )
            return response
        except Investor_Wallet_Details.DoesNotExist:
            return redirect("investors_wallet")


@login_required
def get_company_superadmin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        comp_name = Company_table.objects.filter(delete_status=False)
        project_list = [{"name": p.company_name} for p in comp_name]
        return JsonResponse({"projects": project_list})
    else:
        return JsonResponse({"error": "User is not authenticated"})


@login_required
@csrf_protect
def download_data_company_data(request, company, file_format):
    if request.user.is_authenticated and request.user.is_superuser:
        comany_data = None
        if company == "all":
            print(company)
            comany_data = Company_table.objects.filter(delete_status=False)
        else:
            comany_data = None
            comany_data = Company_table.objects.filter(
                company_name=company, delete_status=False
            )

        if file_format == "xls":
            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("Investor Wallet History")
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = [
                "Company Name",
                "Email ID",
                "Contact Number",
                "Company Pan",
                "GST",
                "State",
                "City",
                "Pincode",
            ]
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            for row in comany_data:
                row_num += 1
                ws.write(row_num, 0, row.company_name)
                ws.write(row_num, 1, row.email_id)
                ws.write(row_num, 2, row.contact_number)
                ws.write(row_num, 3, row.company_pan)
                ws.write(row_num, 4, row.gstin)
                ws.write(row_num, 5, row.State)
                ws.write(row_num, 6, row.City)
                ws.write(row_num, 7, row.pincode)

            wb.save("company_data.xls")
            response = HttpResponse(content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = 'attachment; filename="company_data.xls"'
            with open("company_data.xls", "rb") as f:
                response.write(f.read())

        elif file_format == "pdf":
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="company_data.pdf"'
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                response,
                pagesize=landscape(letter),
                rightpadding=10,
                leftpadding=10,
                topMargin=10,
                bottomMargin=10,
            )
            doc.title = "Investor Wallet History"
            data = [
                [
                    "Company Name",
                    "Email ID",
                    "Contact Number",
                    "Company Pan",
                    "GST",
                    "State",
                    "City",
                    "Pincode",
                ]
            ]
            for row in comany_data:
                data.append(
                    [
                        row.company_name,
                        row.email_id,
                        row.contact_number,
                        row.company_pan,
                        row.gstin,
                        row.State,
                        row.City,
                        row.pincode,
                    ]
                )
            table = Table(data)
            table.setStyle(
                TableStyle(
                    [
                        ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
                        ("BACKGROUND", (0, 0), (-1, 0), "white"),
                        ("TEXTCOLOR", (0, 0), (-1, 0), "black"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("GRID", (0, 0), (-1, -1), 0.5, "black"),
                        ("TOPPADDING", (0, 0), (-1, -1), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ]
                )
            )
            elements = [table]
            doc.build(elements)
            pdf_data = buffer.getvalue()
            buffer.close()
            response.write(pdf_data)

        elif file_format == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="company_data.csv"'
            writer = csv.writer(response)
            writer.writerow(
                [
                    "Company Name",
                    "Email ID",
                    "Contact Number",
                    "Company Pan",
                    "GST",
                    "State",
                    "City",
                    "Pincode",
                ]
            )
            for row in comany_data:
                writer.writerow(
                    [
                        row.company_name,
                        row.email_id,
                        row.contact_number,
                        row.company_pan,
                        row.gstin,
                        row.State,
                        row.City,
                        row.pincode,
                    ]
                )

        return response


@login_required
def project_profit_report(request):
    try:
        s = request.user
        check_inv = Company_table.objects.get(email_id=s)
        code = check_inv.company_code
        name = check_inv.company_name
        my_model_instances = ProjectSales.objects.filter(company_code=code)
        sts = "Admin"
        if check_inv is not None:
            if request.method == "POST":
                get_name = request.POST.get("name")
                context = {
                    "my_model_instances": my_model_instances,
                    "name": name,
                    "satus": sts,
                    "company": name,
                }
            context = {
                "my_model_instances": my_model_instances,
                "name": name,
                "satus": sts,
                "company": name,
            }
            return render(
                request,
                "admin_dash_menu/pages/report/project_profit_report.html",
                context,
            )

        else:
            pass
    except Company_table.DoesNotExist:
        check = Staff.objects.get(username=s)
        code = check.company_code
        name = check.company_name
        staf_name = check.username
        my_model_instances1 = ProjectSales.objects.filter(company_code=code)
        proj_inv_per = Report_view.objects.get(staff_name=staf_name, company_code=code)
        if proj_inv_per.status:
            if proj_inv_per.view:
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
                    request,
                    "admin_dash_menu/pages/report/project_profit_report.html",
                    context,
                )
            else:
                return redirect("notallowed")
        else:
            return redirect("notallowed")

    else:
        return redirect("notallowed")


@login_required
@csrf_protect
def project_report_data(request, pk):
    data = dict()
    get_project = Project.objects.get(pk=pk)
    sent_share_value = get_project.Total_share
    try:
        check = Invesments_Db.objects.filter(project=get_project.project_name).latest(
            "id"
        )
        get_investor = Invesments_Db.objects.filter(project=get_project.project_name)
        get_onves_count = (
            Invesments_Db.objects.filter(project=get_project.project_name)
            .values("investor_name")
            .annotate(count=Count("investor_name"))
            .count()
        )
        get_total_invesment = get_investor.aggregate(Sum("amount"))["amount__sum"]
        get_total_share_count = get_investor.aggregate(Sum("investor_share_count"))[
            "investor_share_count__sum"
        ]
        avalible_share = get_project.share_count
    except Invesments_Db.DoesNotExist:
        get_total_invesment = 0
        get_total_share_count = 0
        get_onves_count = 0
        avalible_share = 0
    other_expense = 0
    expense_count = 0
    try:
        check_exp = ProjectExpense.objects.filter(
            project_name=get_project.project_name
        ).latest("id")
        get_exp = ProjectExpense.objects.filter(project_name=get_project.project_name)
        expense_count = get_exp.count()
        total_expense = get_exp.aggregate(Sum("amount"))["amount__sum"]
        other_expense = get_project.Other_expense
    except ProjectExpense.DoesNotExist:
        expense_count = 0
        total_expense = 0

    try:
        check_sale = ProjectSales.objects.filter(
            project_name=get_project.project_name
        ).latest("id")
        get_sale = ProjectSales.objects.filter(
            project_name=get_project.project_name, Second_Approved_by__isnull=False
        )
        sale_count = get_sale.count()
        total_sale = get_sale.aggregate(Sum("amount"))["amount__sum"]
        total_unit_sale = get_sale.aggregate(Sum("unit_sold"))["unit_sold__sum"]
    except ProjectSales.DoesNotExist:
        sale_count = 0
        total_sale = 0
        total_unit_sale = 0

    prof_condition = get_project.Per_share_value * (get_total_share_count - 1)

    data["project_name"] = get_project.project_name
    data["project_value"] = get_project.Project_value

    data["total_share_value"] = sent_share_value
    data["prof_condition"] = prof_condition

    data["total_invesment"] = get_total_invesment
    data["investors_count"] = get_onves_count
    data["total_share_selled"] = get_total_share_count
    data["total_share_available"] = avalible_share

    data["get_project_name_exp"] = get_project.project_name
    data["total_share_value_exp"] = sent_share_value
    data["total_expense"] = total_expense
    data["expense_count"] = expense_count
    data["other_expense"] = other_expense

    data["get_project_name_sale"] = get_project.project_name
    data["total_share_value_sale"] = sent_share_value
    data["sale_count"] = sale_count
    data["total_sale"] = total_sale
    data["total_unit_sale"] = total_unit_sale

    return JsonResponse(data)


@login_required
@csrf_protect
def project_report_data_download(request, pk):
    data = dict()
    get_project = Project.objects.get(pk=pk)
    sent_share_value = get_project.Total_share
    try:
        check = Invesments_Db.objects.filter(project=get_project.project_name).latest(
            "id"
        )
        get_investor = Invesments_Db.objects.filter(project=get_project.project_name)
        get_onves_count = (
            Invesments_Db.objects.filter(project=get_project.project_name)
            .values("investor_name")
            .annotate(count=Count("investor_name"))
            .count()
        )
        get_total_invesment = get_investor.aggregate(Sum("amount"))["amount__sum"]
        get_total_share_count = get_investor.aggregate(Sum("investor_share_count"))[
            "investor_share_count__sum"
        ]
        avalible_share = get_project.share_count
    except Invesments_Db.DoesNotExist:
        get_total_invesment = 0
        get_total_share_count = 0
        get_onves_count = 0
        avalible_share = 0
    other_expense = 0
    expense_count = 0
    try:
        check_exp = ProjectExpense.objects.filter(
            project_name=get_project.project_name
        ).latest("id")
        get_exp = ProjectExpense.objects.filter(project_name=get_project.project_name)
        expense_count = get_exp.count()
        total_expense = get_exp.aggregate(Sum("amount"))["amount__sum"]
        other_expense = get_project.Other_expense
    except ProjectExpense.DoesNotExist:
        expense_count = 0
        total_expense = 0

    try:
        check_sale = ProjectSales.objects.filter(
            project_name=get_project.project_name
        ).latest("id")
        get_sale = ProjectSales.objects.filter(
            project_name=get_project.project_name, Second_Approved_by__isnull=False
        )
        sale_count = get_sale.count()
        total_sale = get_sale.aggregate(Sum("amount"))["amount__sum"]
        total_unit_sale = get_sale.aggregate(Sum("unit_sold"))["unit_sold__sum"]
    except ProjectSales.DoesNotExist:
        sale_count = 0
        total_sale = 0
        total_unit_sale = 0

    profit = 0
    temp_profit_1 = total_sale - get_total_invesment
    company_share = 0
    unused_exp = 0
    if total_expense > other_expense:
        company_share = int(total_expense - other_expense)
        temp_profit_1 = temp_profit_1 - company_share
    elif total_expense < other_expense:
        unused_share = int(other_expense - total_expense)
        unused_exp = unused_share
    else:
        company_share = 0
        temp_profit_1 = temp_profit_1
    real_profit = (get_total_invesment / sent_share_value) * temp_profit_1
    if unused_exp > 0:
        real_profit = real_profit

    profit = int(real_profit)

    data["project_name"] = get_project.project_name
    data["total_share_value"] = sent_share_value
    data["total_invesment"] = get_total_invesment
    data["investors_count"] = get_onves_count
    data["total_share_selled"] = get_total_share_count
    data["total_share_available"] = avalible_share

    data["get_project_name_exp"] = get_project.project_name
    data["total_share_value_exp"] = sent_share_value
    data["total_expense"] = total_expense
    data["expense_count"] = expense_count
    data["other_expense"] = other_expense

    data["get_project_name_sale"] = get_project.project_name
    data["total_share_value_sale"] = sent_share_value
    data["sale_count"] = sale_count
    data["total_sale"] = total_sale
    data["total_unit_sale"] = total_unit_sale

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="project_data.pdf"'
    buffer = io.BytesIO()
    elements = []
    doc = SimpleDocTemplate(response, pagesize=letter, topMargin=10, bottomMargin=10)
    doc.title = get_project.project_name

    styles = getSampleStyleSheet()
    project_name = Paragraph(
        "Project Name: {}".format(get_project.project_name), styles["Heading1"]
    )
    total_share = Paragraph(
        "Total Share: {} INR".format(sent_share_value), styles["Heading2"]
    )
    investment = Paragraph(
        "Investment: {} INR".format(get_total_invesment), styles["Heading2"]
    )
    investors = Paragraph("Investors: {}".format(get_onves_count), styles["Heading2"])
    sold_share = Paragraph(
        "Sold Share: {} ".format(get_total_share_count), styles["Heading2"]
    )
    avalible_share_a = Paragraph(
        "Available Share: {}".format(avalible_share), styles["Heading2"]
    )
    expense = Paragraph("Expense: {} INR".format(total_expense), styles["Heading2"])
    if unused_exp > 0:
        unused_exp_prrit = Paragraph(
            "Unused Expense: {} INR".format(unused_exp), styles["Heading2"]
        )
    else:
        unused_exp_prrit = Paragraph(
            "Unused Expense: {} INR".format(unused_exp), styles["Heading2"]
        )
    if company_share > 0:
        company_share_prrit = Paragraph(
            "Company Share: {} INR".format(company_share), styles["Heading2"]
        )
    else:
        company_share_prrit = Paragraph(
            "Company Share: {} INR".format(company_share), styles["Heading2"]
        )
    ex_count = Paragraph("Expense Count: {}".format(expense_count), styles["Heading2"])
    otr_exp = Paragraph(
        "Other Expense: {} INR".format(other_expense), styles["Heading2"]
    )
    sales = Paragraph("Sales: {} INR".format(total_sale), styles["Heading2"])
    sales_count = Paragraph("Sales Count: {}".format(sale_count), styles["Heading2"])
    sold_unit = Paragraph("Sold Unit: {}".format(total_unit_sale), styles["Heading2"])
    profir_p = Paragraph("Profit: {} INR".format(profit), styles["Heading2"])

    elements.extend(
        [
            project_name,
            total_share,
            investment,
            investors,
            sold_share,
            avalible_share_a,
            expense,
            unused_exp_prrit,
            company_share_prrit,
            ex_count,
            otr_exp,
            sales,
            sales_count,
            sold_unit,
            profir_p,
        ]
    )

    doc.build(elements)
    pdf_data = buffer.getvalue()
    buffer.close()
    response.write(pdf_data)

    return response


@login_required
@csrf_protect
def download_data_project_all(request, file_format):
    if request.user.is_authenticated:
        company_id = request.user
        try:
            get_com_name = Company_table.objects.get(email_id=company_id)
            code = get_com_name.company_code
            cmp_name = get_com_name.company_name
        except Company_table.DoesNotExist:
            get_com_name = Staff.objects.get(username=company_id)
            code = get_com_name.company_code
            cmp_name = get_com_name.company_name
        try:
            check = Project.objects.filter(company_code=code)
            project_sales_history = Project.objects.filter(company_code=code)
        except Project.DoesNotExist:
            project_sales_history = []
        if file_format == "xls":
            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("Project Data")
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = [
                "Project Name",
                "Location",
                "Latitude",
                "Longitude",
                "Project Value",
                "Kickoff Date",
                "Returns Type",
                "Returns Value",
                "Other Expense",
                "Total Share",
                "Share Value",
                "Share Count",
                "Expected Return Date",
                "Created Date",
            ]
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            for row in project_sales_history:
                row_num += 1
                ws.write(row_num, 0, row.project_name)
                ws.write(row_num, 1, row.Project_location)
                ws.write(row_num, 2, row.Latitude)
                ws.write(row_num, 3, row.Longitude)
                ws.write(row_num, 4, row.Project_value)
                ws.write(row_num, 5, row.Kickoff_date)
                ws.write(row_num, 6, row.Returns_projection_type)
                ws.write(row_num, 7, row.Returns_projection_value)
                ws.write(row_num, 8, row.Other_expense)
                ws.write(row_num, 9, row.Total_share)
                ws.write(row_num, 10, row.Per_share_value)
                ws.write(row_num, 11, row.share_count)
                ws.write(row_num, 12, row.Expected_return_date)
                ws.write(row_num, 13, row.Created_datetime.strftime("%d-%m-%Y"))
            wb.save("project_data.xls")
            response = HttpResponse(content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = 'attachment; filename="project_data.xls"'
            with open("project_data.xls", "rb") as f:
                response.write(f.read())

        elif file_format == "pdf":
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="project_data.pdf"'
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                response, pagesize=landscape(letter), topMargin=10, bottomMargin=10
            )
            doc.title = "Project Data"
            data = [
                [
                    "Project Name",
                    "Location",
                    "Latitude",
                    "Longitude",
                    "Project Value",
                    "Kickoff Date",
                    "Returns Type",
                    "Returns Value",
                    "Other Expense",
                    "Total Share",
                    "Share Value",
                    "Share Count",
                    "Expected Return Date",
                    "Created Date",
                ]
            ]
            for row in project_sales_history:
                data.append(
                    [
                        row.project_name,
                        row.Project_location,
                        row.Latitude,
                        row.Longitude,
                        row.Project_value,
                        row.Kickoff_date,
                        row.Returns_projection_type,
                        row.Returns_projection_value,
                        row.Other_expense,
                        row.Total_share,
                        row.Per_share_value,
                        row.share_count,
                        row.Expected_return_date,
                        row.Created_datetime.strftime("%d-%m-%Y"),
                    ]
                )
            table = Table(data)

            table.setStyle(
                TableStyle(
                    [
                        ("FONT", (0, 0), (-1, -1), "Helvetica", 7),
                        ("BACKGROUND", (0, 0), (-1, 0), "white"),
                        ("TEXTCOLOR", (0, 0), (-1, 0), "black"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("GRID", (0, 0), (-1, -1), 0.5, "black"),
                        ("TOPPADDING", (0, 0), (-1, -1), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ]
                )
            )
            elements = [table]
            doc.build(elements)
            pdf_data = buffer.getvalue()
            buffer.close()
            response.write(pdf_data)

        elif file_format == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="project_data.csv"'
            writer = csv.writer(response)
            writer.writerow(
                [
                    "Project Name",
                    "Location",
                    "Latitude",
                    "Longitude",
                    "Project Value",
                    "Kickoff Date",
                    "Returns Type",
                    "Returns Value",
                    "Other Expense",
                    "Total Share",
                    "Share Value",
                    "Share Count",
                    "Expected Return Date",
                    "Created Date",
                ]
            )
            for row in project_sales_history:
                writer.writerow(
                    [
                        row.project_name,
                        row.Project_location,
                        row.Latitude,
                        row.Longitude,
                        row.Project_value,
                        row.Kickoff_date,
                        row.Returns_projection_type,
                        row.Returns_projection_value,
                        row.Other_expense,
                        row.Total_share,
                        row.Per_share_value,
                        row.share_count,
                        row.Expected_return_date,
                        row.Created_datetime.strftime("%d-%m-%Y"),
                    ]
                )

        return response
