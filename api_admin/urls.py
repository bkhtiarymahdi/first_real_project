from django.urls import path

from . import views

app_name = 'api_admin'
urlpatterns = [
    path("panel/", views.ArticleAdminList.as_view(), name='list_article'),
]
