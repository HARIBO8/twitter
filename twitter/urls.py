"""
URL configuration for twitter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from core import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('tweet/new/', views.create_tweet, name='create_tweet'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:user_id>/', views.profile_view, name='user_profile'),
    path('like/<int:tweet_id>/', views.toggle_like, name='toggle_like'),
    path('reply/<int:tweet_id>/', views.reply_tweet, name='reply_tweet'),
    path('retweet/<int:tweet_id>/', views.retweet, name='retweet'),
    path('search/', views.search, name='search'),
    path('retweet_toggle/<int:tweet_id>/', views.toggle_retweet, name='toggle_retweet'),
    path('tweet/<int:tweet_id>/edit/', views.edit_tweet, name='edit_tweet'),
    path('tweet/<int:tweet_id>/delete/', views.delete_tweet, name='delete_tweet'),
    path('tweet/<int:tweet_id>/', views.tweet_detail, name='tweet_detail'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.urls import path
from core import views

urlpatterns += [
    path('follow-toggle/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('followers/<int:user_id>/', views.get_followers, name='get_followers'),
    path('following/<int:user_id>/', views.get_following, name='get_following'),
]