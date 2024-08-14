"""
URL configuration for courtManagementSystem project.

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
from django.contrib import admin
from django.urls import path
from app import views
from app.views import StripeIntentView, stripe_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.booking_schedule, name='booking_schedule'), #TODO
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('payment_success/', views.payment_success, name='payment_success'),  # Add a success page view
    path('create-payment-intent/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('update_payment_intent/', views.update_payment_intent, name='update_payment_intent'),
    path('test/', views.my_view, name='test'),
]