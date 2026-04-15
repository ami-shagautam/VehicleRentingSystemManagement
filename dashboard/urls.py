
from django.urls import path,include
from . import views


urlpatterns = [
path('',views.dashboard,name='dashboard'),
path('dashboard/', views.dashboard_overview, name='dashboard_overview' ),

path('bookings/', views.booking_dashboard, name='booking_list'),
path('bookings/add/', views.booking_form, name='booking_form'),
path('bookings/delete/<int:pk>/', views.booking_delete, name='booking_delete'),

path('payments/', views.payment_dashboard, name='payment_dashboard'),
path('payments/add/', views.payment_form, name='payment_form'),
path('payments/delete/<int:pk>/', views.payment_delete, name='payment_delete'),

path('vehicles/', views.vehicle_dashboard, name='vehicle_dashboard'),
path('vehicles/add/', views.vehicle_form, name='vehicle_form'),
path('vehicles/edit/<int:pk>/', views.vehicle_update, name='vehicle_update'),
path('vehicles/delete/<int:pk>/', views.vehicle_delete, name='vehicle_delete'),

]