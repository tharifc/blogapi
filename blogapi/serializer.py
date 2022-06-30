from rest_framework.serializers import ModelSerializer
from blogapi.models import Blogs,Comments

from rest_framework import serializers
from django.contrib.auth.models import User


class BlogsSerializer(ModelSerializer):
    id = serializers.CharField(read_only=True)
    author = serializers.CharField(read_only=True)


class BlogSerializer(ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Blogs
        exclude = ("author","liked_by")

    def create(self, validated_data):
        user = self.context.get('author')
        return Blogs.objects.create(**validated_data, author=user)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password", "email"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CommentSerializer(ModelSerializer):
    user=serializers.CharField(read_only=True)
    blog=serializers.CharField(read_only=True)

    class Meta:
        model=Comments
        fields=["blog","user","comment"]

    def create(self, validated_data):
        user=self.context.get("user")
        blog=self.context.get("blog")
        return Comments.objects.create(**validated_data,blog=blog,user=user)

