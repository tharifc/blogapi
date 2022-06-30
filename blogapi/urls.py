from django.urls import path
from blogapi import views

urlpatterns=[
    path("blogs",views.BlogsView.as_view()),
    path('blogs/<int:blog_id>',views.BlogDetails.as_view()),
    path('users/accounts/signup',views.UserCreation.as_view()),
    path('users/accounts/signin',views.SigninView.as_view()),
    path('blogs/like/<int:blog_id>',views.BlogLikeView.as_view()),
    path('blogs/comments/<int:blog_id>',views.BlogCommentsView.as_view())

]