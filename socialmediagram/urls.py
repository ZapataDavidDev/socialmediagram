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
    
    # Health Check
    path('test/health', views_test_connectivity.test_health_check, name='test_health'),
    
    # === ENDPOINTS SEGUROS ===
    path('test/safe/json', views_test_connectivity.test_safe_json, name='test_safe_json'),
    path('test/safe/html', views_test_connectivity.test_safe_html, name='test_safe_html'),
    path('test/safe/xml', views_test_connectivity.test_safe_xml, name='test_safe_xml'),
    path('test/safe/text', views_test_connectivity.test_safe_text, name='test_safe_text'),
    path('test/safe/large-json', views_test_connectivity.test_safe_large_json, name='test_safe_large_json'),
    
    # === ENDPOINTS DE AUTENTICACIÓN ===
    path('test/auth/basic', views_test_connectivity.test_basic_auth, name='test_basic_auth'),
    path('test/auth/bearer', views_test_connectivity.test_bearer_token, name='test_bearer_token'),
    
    # === ENDPOINTS MALICIOSOS - MALWARE ===
    path('test/malware/executable', views_test_connectivity.test_malware_executable, name='test_malware_exe'),
    path('test/malware/shellscript', views_test_connectivity.test_malware_shellscript, name='test_malware_sh'),
    path('test/malware/zip', views_test_connectivity.test_malware_zip, name='test_malware_zip'),
    path('test/malware/dll', views_test_connectivity.test_malware_dll, name='test_malware_dll'),
    path('test/malware/octet-stream', views_test_connectivity.test_malware_octet_stream, name='test_malware_octet'),
    
    # === ENDPOINTS DE DOS ===
    path('test/dos/large-response', views_test_connectivity.test_dos_large_response, name='test_dos_large'),
    path('test/dos/slow-response', views_test_connectivity.test_dos_slow_response, name='test_dos_slow'),
    path('test/dos/fast-anomaly', views_test_connectivity.test_dos_fast_anomaly, name='test_dos_fast'),
    path('test/dos/infinite-stream', views_test_connectivity.test_dos_infinite_stream, name='test_dos_infinite'),
    
    # === ENDPOINTS DE CONTENT-TYPE NO PERMITIDO ===
    path('test/disallowed/pdf', views_test_connectivity.test_disallowed_pdf, name='test_disallowed_pdf'),
    path('test/disallowed/word', views_test_connectivity.test_disallowed_word, name='test_disallowed_word'),
    path('test/disallowed/image', views_test_connectivity.test_disallowed_image, name='test_disallowed_image'),
    
    # === ENDPOINTS DE EXTENSIONES PELIGROSAS ===
    path('test/dangerous/file.exe', views_test_connectivity.test_dangerous_extension_exe, name='test_dangerous_exe'),
    path('test/dangerous/script.sh', views_test_connectivity.test_dangerous_extension_sh, name='test_dangerous_sh'),
    path('test/dangerous/library.dll', views_test_connectivity.test_dangerous_extension_dll, name='test_dangerous_dll'),
    
    # === ENDPOINTS DE VULNERABILIDAD ===
    path('test/evil/capture-credentials', views_test_connectivity.test_capture_credentials, name='test_capture_creds'),
    path('test/evil/clear-log', views_test_connectivity.clear_stolen_credentials_log, name='test_clear_log'),
    
    # === ENDPOINTS ADICIONALES ===
    path('test/redirect', views_test_connectivity.test_redirect, name='test_redirect'),
    path('test/custom-headers', views_test_connectivity.test_custom_headers, name='test_custom_headers'),


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
