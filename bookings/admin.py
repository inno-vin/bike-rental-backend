from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'bike',
        'renter',
        'start_date',
        'end_date',
        'status',
        'created_at',
    )

    list_filter = ('status', 'start_date')
    search_fields = (
        'bike__title',
        'renter__username',
    )
