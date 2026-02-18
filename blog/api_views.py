from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Blog, Category, Comment
from .serializers import BlogSerializer, CategorySerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def blog_list_api(request):
    blogs = Blog.objects.all().order_by("-created_at")
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def blog_detail_api(request, id):
    blog = get_object_or_404(Blog, id=id)
    serializer = BlogSerializer(blog)
    return Response(serializer.data)

@api_view(["GET"])
def category_list_api(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def category_blogs_api(request, id):
    blogs = Blog.objects.filter(category_id=id)
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def blog_comment_api(request, id):
    blog = get_object_or_404(Blog, id=id)
    Comment.objects.create(
        blog=blog,
        user=request.user,
        text=request.data.get("text")
    )
    return Response({"message": "Comment added successfully"})

