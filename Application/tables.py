import datetime
from django.shortcuts import render, get_object_or_404, redirect
import ast
from .models import *
from .forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum


@login_required
@csrf_protect
def admin_view_investor(request, pk):
    if request.user.is_superuser:
        data = dict()
        my_model_instances = get_object_or_404(Investors, pk=pk)
        context = {"my_model_instances": my_model_instances}

        template_name = "admin_dash_menu/pages/admin_v_users/admin_investore_view.html"
        data["html_form"] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return redirect("notallowed")


@login_required
@csrf_protect
def admin_investors_list(request):
    admin = request.user.is_superuser
    if admin == 1:
        sts = "Super Admin"
        my_model_instances = Investors.objects.all()
        return render(
            request,
            "admin_dash_menu/pages/admin_v_users/admin_Investors.html",
            {
                "my_model_instances": my_model_instances,
                "name": request.user,
                "satus": sts,
            },
        )
    else:
        return redirect("notallowed")


@login_required
@csrf_protect
def admin_staff_list(request):
    admin = request.user.is_superuser
    if admin == 1:
        sts = "Super Admin"
        my_model_instances = Staff.objects.all()
        return render(
            request,
            "admin_dash_menu/pages/admin_v_users/admin_staff.html",
            {
                "my_model_instances": my_model_instances,
                "name": request.user,
                "satus": sts,
            },
        )
    else:
        return redirect("notallowed")
