from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Vehicle, Booking, Payment

# ---------------------------
# Category Admin
# ---------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_per_page = 10


# ---------------------------
# Vehicle Admin
# ---------------------------
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_per_day', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_per_page = 10
    readonly_fields = ('created_at',)


# ---------------------------
# Inline Payment Admin for Booking
# ---------------------------
class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('created_at', 'paid_at')
    fields = ('amount', 'method', 'status', 'transaction_id', 'paid_at', 'created_at')


# ---------------------------
# Booking Admin
# ---------------------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vehicle', 'status', 'start_date', 'end_date', 'total_days', 'total_cost', 'created_at')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('user__username', 'vehicle__name')
    inlines = [PaymentInline]
    readonly_fields = ('total_days', 'total_cost', 'created_at')
    ordering = ('-created_at',)


# ---------------------------
# Payment Admin
# ---------------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'status', 'method', 'transaction_id', 'paid_at', 'created_at')
    list_filter = ('status', 'method')
    search_fields = ('booking__vehicle__name', 'booking__user__username', 'transaction_id')
    readonly_fields = ('created_at', 'paid_at')
    ordering = ('-created_at',)