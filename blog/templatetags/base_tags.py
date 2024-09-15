from django import template
from common.models import Category

register = template.Library()


@register.inclusion_tag("blog/category_navbar.html", takes_context=True)
def category_nav(context):
    user = context["user"]  # کاربر از کانتکست دریافت می‌شود
    return {
        "categories": Category.objects.all(),
        "user": user,  # کاربر را به تمپلیت ارسال می‌کنیم
    }


@register.filter
def instanceof(value, class_name):
    from django.apps import apps

    model = apps.get_model(*class_name.split("."))
    return isinstance(value, model)


@register.filter
def isinstance_of(obj, class_name):
    return obj.__class__.__name__.lower() == class_name.lower()
