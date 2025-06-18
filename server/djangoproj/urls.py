"""djangoproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
        path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
        path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
        path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.templatetags.static import static as static_url
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # Serve React app for root and main frontend routes
    path('', TemplateView.as_view(template_name="Home.html")),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    
    # Dynamic Django pages
    path('dealers/', TemplateView.as_view(template_name="dealers.html")),
    path('dealer/<int:dealer_id>/', TemplateView.as_view(template_name="dealer_details.html")),
    path('add_review/', TemplateView.as_view(template_name="add_review.html")),
    path('add_review/<int:dealer_id>/', TemplateView.as_view(template_name="add_review.html")),

    # Serve static files from React build
    path('manifest.json', serve, {'path': 'frontend/build/manifest.json', 'document_root': settings.BASE_DIR}),
    path('favicon.ico', serve, {'path': 'frontend/build/favicon.ico', 'document_root': settings.BASE_DIR}),
    path('logo192.png', serve, {'path': 'frontend/build/logo192.png', 'document_root': settings.BASE_DIR}),
    path('logo512.png', serve, {'path': 'frontend/build/logo512.png', 'document_root': settings.BASE_DIR}),
    path('robots.txt', serve, {'path': 'frontend/build/robots.txt', 'document_root': settings.BASE_DIR}),

    # Catch-all route for React app
    re_path(r'^.*$', TemplateView.as_view(template_name="index.html")),
]

# Serve static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
