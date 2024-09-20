from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.contenttypes.models import ContentType

import logging
from itertools import chain
from azbankgateways.exceptions import AZBankGatewaysException
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from common.models import (
    Order,
    InPersonCourse,
    OnlineCourse,
    OrderItem,
    Pamphlets,
    Transaction,
    User_Access,
)


class ListInPersonCourse(ListView):
    queryset = InPersonCourse.objects.all()
    template_name = "E_commerce/in_person_course.html"
    context_object_name = "inpersoncourses"
    paginate_by = 4


class ListOnlineCourse(ListView):
    queryset = OnlineCourse.objects.all()
    template_name = "E_commerce/online_course.html"
    context_object_name = "onlinecourses"
    paginate_by = 4


class PamphletsLisrview(ListView):
    queryset = Pamphlets.objects.all()
    template_name = "E_commerce/pamphlets.html"
    context_object_name = "pamphlets"
    paginate_by = 4


class ListProduct(ListView):
    queryset = InPersonCourse.objects.all().order_by("-create")
    template_name = "E_commerce/products.html"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        in_person_course = InPersonCourse.objects.all().order_by("-create")
        onlinecourse = OnlineCourse.objects.all().order_by("-create")
        pamphlets = Pamphlets.objects.all().order_by("-create")
        combined = sorted(
            chain(in_person_course, onlinecourse, pamphlets), key=lambda x: x.create
        )
        context["products"] = combined
        return context


def detail_view_product(request, type, pk):
    if type == "pamphlets":
        product = get_object_or_404(Pamphlets, id=pk)
    elif type == "onlinecourse":
        product = get_object_or_404(OnlineCourse, id=pk)
    elif type == "inpersoncourse":
        product = get_object_or_404(InPersonCourse, id=pk)

    user_orders = Order.objects.filter(user=request.user, is_paid=True)
    if type == "pamphlets":
        has_purchased = OrderItem.objects.filter(
            order__in=user_orders, pamphlets=product
        ).exists()
    elif type == "onlinecourse":
        has_purchased = OrderItem.objects.filter(
            order__in=user_orders, online_course=product
        ).exists()
    elif type == "inpersoncourse":
        has_purchased = OrderItem.objects.filter(
            order__in=user_orders, in_person_course=product
        ).exists()

    context = {"object": product, "type": type, "has_purchased": has_purchased}
    return render(request, "E_commerce/detaile3model.html", context)


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
    elif item_type == "pamphlets":
        item = get_object_or_404(Pamphlets, id=item_id)
        order_item, created = OrderItem.objects.get_or_create(
            order=order, pamphlets=item
        )
    else:
        return redirect("blog/home")

    if not created:
        order_item.quantity += 1
        order_item.save()

    messages.success(request, "با موفقیت به سبد اضافه شد.")

    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    else:
        return redirect("blog/home")


@login_required
def view_cart(request):
    global total_amount
    order = Order.objects.filter(user=request.user, is_paid=False).first()

    transaction = Transaction.objects.filter(order=order).first()

    total_amount = sum(
        (item.quantity or 0) * (item.price or 0) for item in order.items.all()
    )
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

    order.total_amount = sum(
        (item.quantity or 0) * (item.price or 0) for item in order.items.all()
    )
    order.save()

    return redirect("E_commerce:view_cart")


def go_to_gateway_view(request):
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = total_amount
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    # user_mobile_number = "+989112221234"  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = (
            factory.create()
        )  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url("/callback-gateway/")
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

        for item in order.items.all():
            if hasattr(item, "in_person_course") and item.in_person_course:
                item.in_person_course.capacity -= 1
                item.in_person_course.save()

                item.in_person_course.list_of_registered_people += (
                    f"{order.user.username}\n"
                )
                item.in_person_course.save()

        messages.success(request, "پرداخت با موفقیت انجام شد.")
    else:
        messages.error(request, "پرداخت با شکست مواجه شد.")

    return redirect("blog:home")
