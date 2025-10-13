
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user>", views.profile, name ="profile"),
    path("follows", views.follows, name = 'follows'),
    path("following/<str:user>", views.following_page, name = 'following'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('post/<int:post_id>/like/', views.likes, name ='likes')
]
