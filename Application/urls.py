from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from Application.staff import *
from Application import views
from Application import admin_dash
from Application.tables import *
from Application.logs import *
from Application.main.company import *
from Application.main.investor import *
from Application.main.project import *
from Application.main.sale_project import *
from Application.main.expense import *
from Application.main.project_inves import *
from Application.main.wallet import *
from Application.main.settlement import *


urlpatterns = (
    [
        # ====================================================Routes VIEW==================================================================
        path("investor/", admin_investors_list, name="admin_investors_list"),
        path("Staff/", admin_staff_list, name="admin_staff_list"),
        path("view_users/<int:pk>/", admin_view_investor, name="admin_view_investor"),
        # ====================================================Company VIEW==================================================================
        path("company/", company_list, name="company_list"),
        path(
            "get_company_name/<str:company_name>/",
            get_company_name,
            name="get_company_name",
        ),
        path(
            "get_company_mobile/<str:company_mobile>/",
            get_company_mobile,
            name="get_company_mobile",
        ),
        path(
            "get_company_email/<str:company_email>/",
            get_company_email,
            name="get_company_email",
        ),
        path(
            "get_company_name_edit/<str:company_name>/<int:pk>/",
            get_company_name_edit,
            name="get_company_name_edit",
        ),
        path(
            "get_company_email_edit/<str:email>/<int:pk>/",
            get_company_email_edit,
            name="get_company_email_edit",
        ),
        path(
            "get_company_num_edit/<int:mob>/<int:pk>/",
            get_company_num_edit,
            name="get_company_num_edit",
        ),
        path("view_company/<int:pk>/", view_company, name="view_company"),
        path("create_comapany/", company_create, name="company_create"),
        path("update_comapany/<int:pk>/", company_updates, name="company_update"),
        path("detele_comapany/<int:pk>/", delete_comapany, name="company_delete"),
        path(
            "get_investors_loged_company/",
            admin_dash.get_investors_loged_company,
            name="get_investors_loged_company",
        ),
        path("change_dashbord/", admin_dash.change_dashbord, name="change_dashbord"),
        # ====================================================STAFF VIEW==================================================================
        path("staff/", staff_list, name="staff_list"),
        path("view_staff/<int:pk>/", view_staff, name="view_staff"),
        path(
            "add_permisions_staff/<int:pk>/",
            add_permisions_staff,
            name="add_permisions_staff",
        ),
        path("get_company_staff/", get_company_staff, name="get_company_staff"),
        path("staff_create/", staff_create, name="staff_create"),
        path("staff_update/<int:pk>/", staff_update, name="staff_update"),
        path("delete_staff/<int:pk>/", delete_staff, name="delete_staff"),
        # =============STAFF VIEW==========================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        path(
            "view_permisions_staff/<int:pk>/",
            view_permisions_staff,
            name="view_permisions_staff",
        ),
        # ====================================================investor VIEW==================================================================
        path("investors/", investors_list, name="investors_list"),
        path("view_investor/<int:pk>/", view_investor, name="view_investor"),
        path(
            "get_company_investors/",
            get_company_investors,
            name="get_company_investors",
        ),
        path("create_investors/", investors_create, name="investors_create"),
        path("update_investors/<int:pk>/", investors_update, name="investors_update"),
        path("detele_investors/<int:pk>/", delete_investors, name="investors_delete"),
        path("investors_wallet/", investors_wallet, name="investors_wallet"),
        path("add_money_wallet/", add_money_wallet, name="add_money_wallet"),
        path(
            "get_company_investors_wallet/",
            get_company_investors_wallet,
            name="get_company_investors_wallet",
        ),
        path(
            "investors_wallet_permission/<int:pk>/",
            investors_wallet_permission,
            name="investors_wallet_permission",
        ),
        path(
            "view_investor_wallet/<int:pk>/",
            view_investor_wallet,
            name="view_investor_wallet",
        ),
        path(
            "get_investor_wallet_blance/<str:investor_name>/",
            get_investor_wallet_blance,
            name="get_investor_wallet_blance",
        ),
        path(
            "get_project_per_share_value/<str:project_name>/",
            get_project_per_share_value,
            name="get_project_per_share_value",
        ),
        path(
            "get_project_unit_value/<str:project_name>/",
            get_project_unit_value,
            name="get_project_unit_value",
        ),
        path(
            "detele_investors_wallet/<int:pk>/",
            detele_investors_wallet,
            name="detele_investors_wallet",
        ),
        path(
            "download-data/<str:investor_name>/<str:file_format>/",
            views.download_data_history_wallet,
            name="download_data",
        ),
        path(
            "download-data-company/<str:company>/<str:file_format>/",
            views.download_data_company_data,
            name="download_data_company",
        ),
        path(
            "get_company_superadmin",
            views.get_company_superadmin,
            name="get_company_superadmin",
        ),
        path(
            "download-data-sales/<str:project_name>/<str:file_format>/",
            views.download_data_history_sales,
            name="download_data_sales",
        ),
        path(
            "get_company_investors_account/<str:email>/",
            get_company_investors_account,
            name="get_company_investors_account",
        ),
        path(
            "download_data_project_all/<str:file_format>/",
            views.download_data_project_all,
            name="download_data_project_all",
        ),
        path(
            "get_company_investors_account_edit/<str:email>/<int:pk>/",
            get_company_investors_account_edit,
            name="get_company_investors_account_edit",
        ),
        # ====================================================Project VIEW==================================================================
        path("project/", project_list, name="project_list"),
        path("view_project/<int:pk>/", view_project, name="view_project"),
        path(
            "get_company_projects/", get_company_projects, name="get_company_projects"
        ),
        path(
            "get_company_projects_sales/",
            get_company_projects_sales,
            name="get_company_projects_sales",
        ),
        path("create_project/", project_create, name="project_create"),
        path("update_project/<int:pk>/", project_update, name="project_update"),
        path("detele_project/<int:pk>/", delete_project, name="project_delete"),
        path(
            "get_project_name_edit/<int:pk>/",
            get_project_name_edit,
            name="get_project_name_edit",
        ),
        path(
            "get_total_share_edit/<int:pk>/",
            get_total_share_edit,
            name="get_total_share_edit",
        ),
        path(
            "check_project_investment/<int:pk>/",
            check_project_investment,
            name="check_project_investment",
        ),
        # ====================================================Project Expences VIEW==================================================================
        path("project-expense/", project_expense_list, name="project_expense_list"),
        path(
            "get_company_projects_expences/",
            get_company_projects_expences,
            name="get_company_projects_expences",
        ),
        path(
            "get_company_projects_exp_names/",
            get_company_projects_exp_names,
            name="get_company_projects_exp_names",
        ),
        path(
            "view_project_expense/<int:pk>/",
            view_project_expense,
            name="view_project_expense",
        ),
        path(
            "create_project_expense/",
            project_expense_create,
            name="project_expense_create",
        ),
        path(
            "update_project_expense/<int:pk>/",
            project_expense_update,
            name="project_expense_update",
        ),
        path(
            "detele_project_expense/<int:pk>/",
            delete_project_expense,
            name="project_expense_delete",
        ),
        path("project-sales/", project_profit_list, name="project_profit_list"),
        path(
            "get_company_projects_project/",
            get_company_projects_project,
            name="get_company_projects_project",
        ),
        path(
            "view_project_profit/<int:pk>/",
            view_project_profit,
            name="view_project_profit",
        ),
        path(
            "project_profit_create/",
            project_profit_create,
            name="project_profit_create",
        ),
        path(
            "project_profit_update/<int:pk>/",
            project_profit_update,
            name="project_profit_update",
        ),
        path(
            "delete_project_profit/<int:pk>/",
            delete_project_profit,
            name="delete_project_profit",
        ),
        # ====================================================Project Investors VIEW==================================================================
        path(
            "project-investors/", project_investor_list, name="project_investors_list"
        ),
        path(
            "view_project_investor/<int:pk>/",
            view_project_investors,
            name="view_project_investor",
        ),
        path(
            "create_project_investors/",
            project_investor_create,
            name="project_investors_create",
        ),
        path(
            "update_project_investors/<int:pk>/",
            project_investor_update,
            name="project_investors_update",
        ),
        path(
            "detele_project_investors/<int:pk>/",
            delete_project_investor,
            name="project_investors_delete",
        ),
        # ====================================================Project Investors VIEW==================================================================
        path("settlements/", project_settlement_list, name="project_settlement_list"),
        path(
            "get_company_setletment_investors/",
            get_company_setletment_investors,
            name="get_company_setletment_investors",
        ),
        path(
            "get_company_setletment_project/<uuid:inves_id>/",
            get_company_setletment_project,
            name="get_company_setletment_project",
        ),
        path(
            "get_company_setletment_invested_amount/<uuid:inves_id>/<uuid:proj_id>/",
            get_company_setletment_invested_amount,
            name="get_company_setletment_invested_amount",
        ),
        path(
            "view_project_settlement/<int:pk>/",
            view_project_settlement,
            name="view_project_settlement",
        ),
        path(
            "project_settlement_create/",
            project_settlement_create,
            name="project_settlement_create",
        ),
        path(
            "project_settlement_update/<int:pk>/",
            project_settlement_update,
            name="project_settlement_update",
        ),
        path(
            "delete_project_settlement/<int:pk>/",
            delete_project_settlement,
            name="delete_project_settlement",
        ),
        # ====================================================#%#%#$^#$& VIEW==================================================================
        path("dashbord", admin_dash.admin_dash, name="base"),
        path(
            "get_data_company/<uuid:code>/",
            admin_dash.investor_dashboard_login,
            name="get_data_company",
        ),
        path(
            "get_invested_project_name/<uuid:comp_code>/",
            admin_dash.get_invested_project_name,
            name="get_invested_project_name",
        ),
        path(
            "get_project_data/<uuid:p_code>/<uuid:c_code>/",
            admin_dash.get_project_data,
            name="get_project_data",
        ),
        path("Dashboard", admin_dash.empty_dashboard, name="empty_dashboard"),
        path("login/", admin_dash.admin_login, name="admin_login"),
        path("logout/", admin_dash.admim_logout, name="admin_logout"),
        path("Access-Denied/", views.Notallowed, name="notallowed"),
        path("User_logs/", User_logs_view, name="User_logs_view"),
        path("Company_logs/", company_logs_view, name="company_logs_view"),
        path(
            "view_company_logs_pk/<int:pk>/",
            view_company_logs_pk,
            name="view_company_logs_pk",
        ),
        path("project_logs/", company_logs_project, name="company_logs_project"),
        path("view_project_log/<int:pk>/", view_project_log, name="view_project_log"),
        path("investor_logs/", company_logs_investor, name="company_logs_investor"),
        path(
            "view_logs_investor/<int:pk>/",
            view_logs_investor,
            name="view_logs_investor",
        ),
        path("wallet_logs/", company_logs_wallet, name="company_logs_wallet"),
        path("view_logs_wallet/<int:pk>/", view_logs_wallet, name="view_logs_wallet"),
        path(
            "investment_logs/",
            company_logs_project_investor,
            name="company_logs_project_investor",
        ),
        path(
            "view_logs_project_investor/<int:pk>/",
            view_logs_project_investor,
            name="view_logs_project_investor",
        ),
        path("expence_logs/", company_logs_expence, name="company_logs_expence"),
        path(
            "view_logs_expence/<int:pk>/", view_logs_expence, name="view_logs_expence"
        ),
        path("sales_logs/", company_logs_sales, name="company_logs_sales"),
        path("view_logs_sales/<int:pk>/", view_logs_sales, name="view_logs_sales"),
        path("staff_logs/", company_logs_staff, name="company_logs_staff"),
        path("view_logs_staff/<int:pk>/", view_logs_staff, name="view_logs_staff"),
        path(
            "view_logs_staff_permission/<int:pk>/",
            view_logs_staff_permission,
            name="view_logs_staff_permission",
        ),
        path(
            "project-report/", views.project_profit_report, name="project_profit_report"
        ),
        path(
            "project_report_data/<int:pk>/",
            views.project_report_data,
            name="project_report_data",
        ),
        path(
            "project_report_data_download/<int:pk>/",
            views.project_report_data_download,
            name="project_report_data_download",
        ),
        path(
            "settlement-logs/", company_logs_settlement, name="company_logs_settlement"
        ),
        path(
            "view_logs_settlement/<int:pk>/",
            view_logs_settlement,
            name="view_logs_settlement",
        ),
        # ====================================================End VIEW==================================================================
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
