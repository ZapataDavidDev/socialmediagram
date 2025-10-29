"""socialmediagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

"""socialmediagram URLs module."""

# Django
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from socialmediagram import views as local_views
from posts import views as posts_views
from users import views as users_views
from . import views_test_connectivity



urlpatterns = [

    path('admin/', admin.site.urls),

    path('atletico-nacional/', local_views.atletico_nacional, name = 'nacional'),
    path('sorted/', local_views.sort_integers, name = 'sort'),
    path('hi/<str:name>/<str:equipo>/', local_views.say_hi, name='hi'),
    
    # Endpoints de prueba de seguridad para ConnectionServer
    path('test/status/<int:code>', views_test_connectivity.test_status, name='test_status'),
    path('test/slow', views_test_connectivity.test_slow, name='test_slow'),
    path('test/fast', views_test_connectivity.test_fast, name='test_fast'),
    path('test/large', views_test_connectivity.test_large, name='test_large'),
    path('test/content_type', views_test_connectivity.test_content_type, name='test_content_type'),
    path('test/chunked', views_test_connectivity.test_chunked, name='test_chunked'),
    path('test/auth/basic', views_test_connectivity.test_basic_auth, name='test_basic_auth'),
    path('test/redirect', views_test_connectivity.test_redirect, name='test_redirect'),
    path('test/echo', views_test_connectivity.test_echo, name='test_echo'),
    path('test/json', views_test_connectivity.test_json, name='test_json'),
    path('test/timeout', views_test_connectivity.test_timeout, name='test_timeout'),
    
    path('', include(('posts.urls', 'posts'), namespace='posts')),
    path('users/', include(('users.urls', 'users'), namespace='users')),

    # path('', posts_views.list_posts, name='feed'),
    # path('posts/new/', posts_views.create_post, name='create_post'),

    # path('users/login/', users_views.login_view, name='login'),
    # path('users/logout/', users_views.logout_view, name='logout'),
    # path('users/signup/', users_views.signup, name='signup'),
    # path('users/me/profile/', users_views.update_profile, name='update_profile'),
    # path('profile_search/', local_views.profile_search, name='profile_search'),
    # path(route='<str:username>/',view=users_views.UserDetailView.as_view(),name='detail')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
