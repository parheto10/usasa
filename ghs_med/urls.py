"""ghs_med URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import index, connexion, loggout
from parametres.views import faq, contact, about

admin.site.site_header = "BIENVENUS SUR GHS"
admin.site.index_title = "ADMINISTRATION GHS"

urlpatterns = [
    path('patients/', include('patients.urls')),
    path('personnels/', include('personnels.urls')),
    path('connexion/', connexion, name='connexion'),
    path('faqs/', faq, name='faq'),
    path('contact/', contact, name='contact'),
    path('apropos/', about, name='about'),
    path('logout', loggout, name='logout'),
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    # path('api/v1/', include('djoser.urls')),
    # path('api/v1/', include('djoser.urls.authtoken')),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="auth/reset_password.html"),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="auth/reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="auth/reset.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="auth/reset_password_complete.html"), name="password_reset_complete"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)