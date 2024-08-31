from django.urls import path
from .views import (
    add_to_cart,
    remove_from_cart,
    go_to_gateway_view,
    callback_gateway_view,
    ListInPersonCourse,
    course_detail_view,
)


app_name = "E_commerce"
urlpatterns = [
    path("add-to-cart/<str:item_type>/<int:item_id>/", add_to_cart, name="add_to_cart"),
    path("inpersoncourses/", ListInPersonCourse.as_view(), name="inpersoncourses"),
    path("<str:type>/<int:pk>/", course_detail_view, name="detail_multimedia"),
    path("remove_from_cart/", remove_from_cart, name="remove_from_cart"),
    path("callback_gateway/", callback_gateway_view, name="callback_gateway"),
    path("onlincourses/", ListInPersonCourse.as_view(), name="onlincourses"),
    path("go_to_gateway/", go_to_gateway_view, name="go_to_gateway"),
]
