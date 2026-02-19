from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Q


class Bike(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bikes'
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)

    location = models.CharField(max_length=255)

    # is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def is_available_for_dates(self, start_date, end_date):
        overlapping_bookings = self.bookings.filter(
            status__in=['pending', 'confirmed'],
            start_date__lte=end_date,
            end_date__gte=start_date,
        )
        return not overlapping_bookings.exists()
