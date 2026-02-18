from rest_framework import serializers
from .models import Blog, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = "__all__"

    def get_comments_count(self, obj):
        return obj.comments.count()

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = "__all__"
