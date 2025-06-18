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
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # Home page
    path('', TemplateView.as_view(template_name="Home.html")),

    # About Us page
    path('about/', TemplateView.as_view(template_name="About.html")),
      # Contact Us page
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
]

# Serve static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
