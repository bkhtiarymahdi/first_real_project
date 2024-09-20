from django import template
from common.models import Category

register = template.Library()


@register.inclusion_tag("blog/category_navbar.html", takes_context=True)
def category_nav(context):
    user = context["user"]
    return {
        "categories": Category.objects.all(),
        "user": user,
    }


@register.filter
def instanceof(value, class_name):
    from django.apps import apps

    model = apps.get_model(*class_name.split("."))
    return isinstance(value, model)


@register.filter
def isinstance_of(obj, class_name):
    return obj.__class__.__name__.lower() == class_name.lower()


@register.filter
def get_model_type(instance):
    return instance.__class__.__name__.lower()


@register.filter
def converter_english_to_persian(instance):
    if instance == "book":
        return "کتاب ها"
    elif instance == "article":
        return "مقالات"
    elif instance == "movie":
        return "فیلم ها"
    elif instance == "voice":
        return "سخنرانی ها"
    elif instance == "shortsound":
        return "صوت های کوتاه"
    elif instance == "inpersoncourse":
        return "دوره حضوری"
    elif instance == "onlinecourse":
        return "دوره غیر حضوری"
    elif instance == "pamphlets":
        return "جزوات"


@register.filter
def specify_url(deta):
    class_name = deta.__class__.__name__.lower()

    if class_name in ["inpersoncourse", "onlinecourse", "pamphlets"]:
        return "E_commerce:detail_products"
    elif class_name in ["movie", "voice", "shortsound"]:
        return "blog:detail_multimedia"
    elif class_name in ["book", "article", "biography"]:
        return "blog:content_detail"
