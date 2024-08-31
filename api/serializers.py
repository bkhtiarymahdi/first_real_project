from rest_framework import serializers

from common.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'publish', 'img', 'content')