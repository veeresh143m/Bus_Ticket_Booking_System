"""
URL configuration for bus_booking_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from testapp import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Main Flow
    path('home/', views.home_view, name='home'),
    path('seat/<int:id>/', views.seat_view, name='seat'),

    # Booking Flow
    path('passenger/', views.passenger_view, name='passenger'),
    path('passenger-page/', views.passenger_page, name='passenger_page'),
    path('payment/', views.payment_view, name='payment'),

    # Success Page
    path('success/', views.success_view, name='success'),

    # API
    path('api/', include('testapp.api_urls')),
]

