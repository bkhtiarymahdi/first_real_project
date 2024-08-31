from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .serializer import ArticleAdminSerializer
from common.models import Article


class ArticleAdminList(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "admin/panel.html"

    def get(self, request):
        queryset = Article.objects.all()
        serializer = ArticleAdminSerializer(queryset, many=True).data
        return Response({'articls':serializer})

