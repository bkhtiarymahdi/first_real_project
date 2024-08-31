from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path("api/", views.ArticleDetailView.as_view(), name="article"),
]
