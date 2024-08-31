from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.http import HttpResponse, Http404

import logging
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from ..common.models import (
    Order,
    InPersonCourse,
    OnlineCourse,
    OrderItem,
    Article,
    Transaction,
)
from azbankgateways.exceptions import AZBankGatewaysException


class ListInPersonCourse(ListView):
    queryset = InPersonCourse.objects.all()
    template_name = "E_commerce/in_person_course.html"
    context_object_name = "inpersoncourses"
    paginate_by = 4


class ListInPersonCourse(ListView):
    queryset = OnlineCourse.objects.all()
    template_name = "E_commerce/online_course.html"
    context_object_name = "onlinecourses"
    paginate_by = 4


def course_detail_view(request, type, pk):
    if type == "movie":
        obj = get_object_or_404(InPersonCourse, pk=pk)
    elif type == "voice":
        obj = get_object_or_404(OnlineCourse, pk=pk)
    # else:
    #     return render(
    #         request, "E_commerce/404.html"
    #     )

    context = {
        "object": obj,
        "type": type,
    }
    return render(request, "E_commerce/detail_course.html", context)


@login_required
def add_to_cart(request, item_type, item_id):
    user = request.user

    order, created = Order.objects.get_or_create(user=user, is_paid=False)

    if item_type == "inpersoncourse":
        item = get_object_or_404(InPersonCourse, id=item_id)
        order_item, created = OrderItem.objects.get_or_create(
            order=order, in_person_course=item
        )
    elif item_type == "onlinecourse":
        item = get_object_or_404(OnlineCourse, id=item_id)
        order_item, created = OrderItem.objects.get_or_create(
            order=order, online_course=item
        )
    elif item_type == "article":
        item = get_object_or_404(Article, id=item_id)
        order_item, created = OrderItem.objects.get_or_create(order=order, article=item)
    else:
        return redirect("home")

    if not created:
        order_item.quantity += 1
        order_item.save()

    messages.success(request, "با موفقیت به سبد اضافه شد.")

    return redirect("cart_view")


@login_required
def view_cart(request):
    global total_amount
    order = Order.objects.filter(user=request.user, is_paid=False).first()

    if not order:
        return redirect("home")

    transaction = Transaction.objects.filter(order=order).first()

    total_amount = sum(item.quantity * item.price for item in order.items.all())
    order.total_amount = total_amount
    order.save()

    if transaction:
        transaction.amount = total_amount
        transaction.save()

    context = {
        "order": order,
        "order_items": order.items.all(),
        "transaction": transaction,
    }

    return render(request, "E_commerce/view_cart.html", context)


@login_required
def remove_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    order = order_item.order

    order_item.delete()

    order.total_amount = sum(item.quantity * item.price for item in order.items.all())
    order.save()

    return redirect("cart_view")


def go_to_gateway_view(request):
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = total_amount
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    # user_mobile_number = "+989112221234"  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = (
            factory.auto_create()
        )  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse("callback-gateway"))
        # bank.set_mobile_number(user_mobile_number)  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()

        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    if bank_record.is_success:
        order = get_object_or_404(Order, user=request.user, is_paid=False)

        order.is_paid = True
        order.save()

        transaction = Transaction.objects.create(
            user=request.user,
            order=order,
            amount=bank_record.amount,
            status="completed",
            tracking_code=tracking_code,
        )

        for item in order.items.all():
            if item.in_person_course:
                item.in_person_course.activate_for_user(request.user)
            elif item.online_course:
                item.online_course.activate_for_user(request.user)
            elif item.article:
                item.article.activate_for_user(request.user)

        messages.success(request, "پرداخت با موفقیت انجام شد.")
    else:
        messages.error(request, "پرداخت با شکست مواجه شد.")

    return redirect("blog/home")
