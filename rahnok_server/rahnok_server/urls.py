"""rahnok_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from auth_service.views import auth_token_login_view, auth_token_logout_view, auth_token_verify_view

urlpatterns = [
    path('auth-token/', auth_token_login_view),
    path('auth-token/<slug:uuid>/', auth_token_logout_view),
    path('auth-token-verify/', auth_token_verify_view),
    path('admin/', admin.site.urls, name='api_token_auth'),
]
