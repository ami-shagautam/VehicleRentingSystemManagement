from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from .models import Category, Profile, Vehicle, Booking, Payment
from .forms import BookingForm, PaymentForm,ProfileForm  
from datetime import datetime, timedelta
import uuid
import json
import base64
from django.views import View
from rentingsystem.generate_signature import genSha256


# Home page - show all categories
def home(request):
    categories = Category.objects.all()
    vehicle = Vehicle.objects.all().order_by('id')[:3]  
    return render(request, 'rentingsystem/home.html', {'categories': categories, 'vehicle': vehicle})
   

def browse_vehicles(request):
    vehicles = Vehicle.objects.filter(is_available=True)
    return render(request, 'rentingsystem/browse_vehicle.html', {'vehicles': vehicles})

@login_required
def book_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    print("REQUEST METHOD:", request.method)

    if request.method == "POST":
        form=BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.vehicle = vehicle
            booking.start_time = request.POST.get('start_time')
            booking.end_time = request.POST.get('end_time')
            booking.save()

            messages.success(request, "Booking created!")
            return redirect('booking-details', booking_id=booking.id)

        else:
            print(form.errors)  

    else:
        form = BookingForm()

    return render(request, 'rentingsystem/booking_page.html', {
        'vehicle': vehicle,
        'form': form
    })
   
@login_required
def booking_details(request, booking_id):
    # booking = Booking.objects.filter(id=booking_id, user=request.user)
    # booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking = Booking.objects.filter(id=booking_id, user=request.user).first()
    # print(booking)
    return render(request, 'rentingsystem/booking_detail.html', {'booking': booking})

@login_required
def payment_method(request, booking_id):
    booking = Booking.objects.filter(id=booking_id, user=request.user).first()
    
    if request.method == "POST":
        method = request.POST.get('method')
        # Create payment record
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_cost,
            method=method,
            status='pending' 
        )
        if method == 'esewa':
            return redirect(f"{reverse('esewa-form')}?payment_id={payment.id}")
        # Mark booking & vehicle if COD
        elif method == 'COD':
            booking.status = 'confirmed'
            booking.vehicle.is_available = False
            booking.vehicle.save()
            booking.save()

            payment.status='completed'
            payment.paid_at = timezone.now()
            payment.save()
        return redirect('booking-details', booking_id=booking.id)
 
    return render(request, 'rentingsystem/payment_method.html', {'booking': booking})

class EsewaView(View):
    def get(self, request, *args, **kwargs):
        payment_id = request.GET.get('payment_id')
        payment = Payment.objects.get(id=payment_id)
        uuid_val=uuid.uuid4()

        secret_key = '8gBm/:&EnhH.1/q'

        data_to_sign = f"total_amount={payment.amount},transaction_uuid={uuid_val},product_code=EPAYTEST"
        result = genSha256(secret_key,data_to_sign)


        # save transaction id
        payment.transaction_id = uuid_val
        # payment.save()

        data = {
            'amount': payment.amount,
            'total_amount': payment.amount,
            'transaction_uuid': uuid_val,
            'product_code': 'EPAYTEST',
            'signature': result,
            "success_url": "http://127.0.0.1:8000/esewa-verify/{payment.id}/",
            "failure_url": "http://127.0.0.1:8000/payment/{payment.booking.id}/",
        }

        return render(request, 'rentingsystem/esewa-form.html', {
            'payment': payment,
            'data': data
        })
    
def esewa_verify(request, payment_id):
    data = request.GET.get('data')
    if not data:
        return HttpResponse("Invalid data", status=400)

    decoded = base64.b64decode(data).decode('utf-8')
    
    map_data= json.loads(decoded)

    payment = Payment.objects.get(id=payment_id)

    if map_data.get('status') == "COMPLETE":
        payment.mark_paid(method='esewa')
        # payment.save()
        booking = payment.booking
        booking.status = 'confirmed'
        booking.vehicle.is_available = False
        booking.vehicle.save()
        booking.save()
        messages.success(request, "Payment successfully completed!")

        return redirect('payment-success', booking_id=booking.id)

    messages.error(request, "Payment failed!")
    return redirect('payment-failed')


def payment_success(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'rentingsystem/payment_success.html', {'booking': booking})

def payment_failed(request):
    return render(request, 'rentingsystem/payment_failed.html')
@login_required
def profile_settings(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_settings')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'rentingsystem/profile_settings.html', {'form': form})

