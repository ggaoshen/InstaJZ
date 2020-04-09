"""InstaJZ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from Insta.views import HelloWorld, PostsView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, addLike, addComment, UserDetailView, UserUpdateView, addFollow, ExploreView, SignUp

urlpatterns = [
    path('', HelloWorld.as_view(), name='helloworld'), 
    path('posts/', PostsView.as_view(), name='posts'), 
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'), 
    path('posts/new/', PostCreateView.as_view(), name='make_post'), 
    path('posts/update/<int:pk>', PostUpdateView.as_view(), name='post_update'), 
    path('posts/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'), 
    path('auth/signup', SignUp.as_view(), name='signup'),
    path('user/<int:pk>', UserDetailView.as_view(), name='user_detail'), 
    path('user/update/<int:pk>', UserUpdateView.as_view(), name='edit_profile'), 
    path('like', addLike, name='addLike'), 
    path('comment', addComment, name='addComment'), 
    path('togglefollow', addFollow, name='addFollow'), 
    path('explore', ExploreView.as_view(), name='explore'),
]

# '' means don't input anything, url as is
# as_view() function is a TemplateView default method
# TemplateView details: https://ccbv.co.uk/projects/Django/3.0/django.views.generic.base/TemplateView/