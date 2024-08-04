"""
URL configuration for djnago_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from shop.views import catalog, delete, delete_by_art, detail, index
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from djnago_shop.forms import LoginForm

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("catalog", catalog),
    path("product/delete/<id>", delete),
    path("product/<id>", detail, name="detail"),
    path("product/delete_by_art/", delete_by_art, name="delete_by_art"),
    path("login/", LoginView.as_view(form_class=LoginForm, success_url="/"), name="login"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
