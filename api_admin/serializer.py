from rest_framework import serializers

from common.models import Article


class ArticleAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = [
            "publish",
            "title",
            "content",
            "status",
            "img",
            "category",
            "word",
            "pdf",
            "tag",
        ]
