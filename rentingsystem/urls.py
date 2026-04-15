from django.urls import path,include
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),  # Home page - categories
    path('vehicles/', views.browse_vehicles, name='browse_vehicles'),  
    path('book/<int:vehicle_id>/', views.book_vehicle, name='book_vehicle'),
    path('booking/<int:booking_id>/', views.booking_details, name='booking-details'),
    path('payment/<int:booking_id>/', views.payment_method, name='process-payment'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('esewa_form/', views.EsewaView.as_view(), name='esewa-form'),
    path('esewa-verify/<int:payment_id>/', views.esewa_verify, name='esewa-verify'),

  
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)