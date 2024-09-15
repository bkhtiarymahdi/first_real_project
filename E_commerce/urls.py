from django.urls import path
from .views import (
    view_cart,
    add_to_cart,
    remove_from_cart,
    go_to_gateway_view,
    callback_gateway_view,
    detail_view_product,
    ListProduct,
    ListInPersonCourse,
    ListOnlineCourse,
    PamphletsLisrview,
)


app_name = "E_commerce"
urlpatterns = [
    path("add-to-cart/<str:item_type>/<int:item_id>/", add_to_cart, name="add_to_cart"),
    path("<str:type>/<int:pk>/", detail_view_product, name="detail_products"),
    path("callback_gateway/", callback_gateway_view, name="callback_gateway"),
    path("remove_from_cart/<int:item_id>", remove_from_cart, name="remove_from_cart"),
    path("view_cart/", view_cart, name="view_cart"),
    path("go_to_gateway/", go_to_gateway_view, name="go_to_gateway"),
    path("list_course/", ListProduct.as_view(), name="list_course"),
    path("pamphlets/", PamphletsLisrview.as_view(), name="pamphlets"),
    path("onlincourses/", ListOnlineCourse.as_view(), name="onlincourses"),
    path("inpersoncourses/", ListInPersonCourse.as_view(), name="inpersoncourses"),
]
