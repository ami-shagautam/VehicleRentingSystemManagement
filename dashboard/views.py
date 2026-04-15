from django.shortcuts import redirect, render
from .models import Vehicle, Booking, Payment
from .forms  import VehicleForm,BookingForm,PaymentForm
from django.shortcuts import get_object_or_404
# Create your views here.
def dashboard(request):
    return render(request,'dashboard/base-dashboard.html')


def dashboard_overview(request):
    context = {
        'total_vehicles': Vehicle.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_payments': Payment.objects.count(),
    }
    return render(request, 'dashboard/overview.html', context)

def booking_dashboard(request):
    bookings = Booking.objects.all()

    return render(request, 'dashboard/booking-dashboard.html', {
        'bookings': bookings,
        'total_bookings': bookings.count(),
        'pending': bookings.filter(status='pending').count(),
        'confirmed': bookings.filter(status='confirmed').count(),
    })



def booking_form(request):
    form = BookingForm()

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_list')

    return render(request, 'dashboard/booking-form.html', {'form': form})



def booking_delete(request, pk):
    Booking.objects.get(id=pk).delete()
    return redirect('booking_dashboard')

def vehicle_dashboard(request):
    vehicles = Vehicle.objects.all()

    return render(request, 'dashboard/vehicle-dashboard.html', {
        'vehicles': vehicles,
        'total_vehicles': vehicles.count(),
        'available': vehicles.filter(is_available=True).count(),
        'booked': vehicles.filter(is_available=False).count(),
    })



def vehicle_form(request):
    form = VehicleForm()

    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('vehicle_dashboard')

    return render(request, 'dashboard/vehicle_form.html', {'form': form})



def vehicle_update(request, pk):
    vehicle = Vehicle.objects.get(id=pk)
    form = VehicleForm(request.POST or None, request.FILES or None, instance=vehicle)

    if form.is_valid():
        form.save()
        return redirect('vehicle_dashboard')

    return render(request, 'dashboard/vehicle_form.html', {'form': form})



def vehicle_delete(request, pk):
    Vehicle.objects.get(id=pk).delete()
    return redirect('vehicle_dashboard')

def payment_dashboard(request):
    payments = Payment.objects.select_related('booking')

    return render(request, 'dashboard/payment-dashboard.html', {
        'payments': payments,
        'total_payments': payments.count(),
        'completed': payments.filter(status='completed').count(),
        'pending': payments.filter(status='pending').count(),
    })



def payment_form(request):
    form = PaymentForm()

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_dashboard')

    return render(request, 'dashboard/payment-form.html', {'form': form})



def payment_delete(request, pk):
    Payment.objects.get(id=pk).delete()
    return redirect('payment_dashboard')
