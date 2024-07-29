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
from app.views import StripeIntentView, ProductLandingPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.booking_schedule, name='booking_schedule'), #TODO
    path('book/', views.book_slot, name='book_slot'),
    path('payment_form/', views.payment_form, name='payment_form'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),  # Add a success page view
    #path('checkout/', views.create_payment, name='create-payment-intent'),

    path('checkout/', ProductLandingPageView.as_view(), name='checkout'),
    path('create-payment-intent/', StripeIntentView.as_view(), name='create-payment-intent')
]