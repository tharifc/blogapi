from django.shortcuts import render
from rest_framework.views import APIView
from blogapi.models import Blogs, UserProfile
from rest_framework.response import Response
from rest_framework import status
from blogapi.serializer import BlogSerializer, UserSerializer, LoginSerializer, CommentSerializer
from django.contrib.auth import authenticate, login
from rest_framework import authentication, permissions
from blogapi.models import Comments


# Create your views here.

class BlogsView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        qs = Blogs.objects.all()
        serializer = BlogSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data, context={'author': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class BlogLikeView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class BlogDetails(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("blog_id")
        blog = Blogs.objects.get(id=id)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        blog_id = kwargs.get("blog_id")
        blog = Blogs.objects.get(id=blog_id)
        serializer = BlogSerializer(instance=blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        blog_id = kwargs.get("blog_id")
        blog = Blogs.objects.get(id=blog_id)
        blog.delete()
        return Response({"msg": "deleted"})


class UserCreation(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    def post(self, request, *ars, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            uname = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = authenticate(request, username=uname, password=password)
            print(user)
            if user:
                login(request, user)
                return Response({"msg": "login success"})
            else:
                return Response({"msg": "invalid credentials"})


class BlogLikeView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        blog_id = kwargs.get("blog_id")
        blog = Blogs.objects.get(id=blog_id)
        blog.liked_by.add(request.user)
        # likes = blog.liked_by.all()
        total_likes = blog.liked_by.all().count()
        return Response({"likedcount": total_likes})


class BlogCommentsView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        blog_id = kwargs.get("blog_id")
        print(blog_id)
        blog = Blogs.objects.get(id=blog_id)
        print("66", blog)
        serializer = CommentSerializer(data=request.data, context={"blog": blog, "user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
