from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from .serializers import ArticleSerializer
from common.models import Article


class ArticleDetailView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blog/home.html"

    def get(self, request):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True).data
        return Response({"articles": serializer})
