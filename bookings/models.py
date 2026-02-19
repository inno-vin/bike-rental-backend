from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from bikes.models import Bike


class Booking(models.Model):
    bike = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    renter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    start_date = models.DateField()
    end_date = models.DateField()

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # 1️⃣ End date must be after start date
        if self.end_date < self.start_date:
            raise ValidationError(
                "End date cannot be before start date."
            )

        # 2️⃣ Prevent double booking for same bike
        overlapping_bookings = Booking.objects.filter(
            bike=self.bike,
            status__in=['pending', 'confirmed'],
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        )

        # Exclude current booking when updating
        if self.pk:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError(
                "This bike is already booked for the selected dates."
            )

    def save(self, *args, **kwargs):
        self.full_clean()   # 🔥 THIS enforces clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bike.title} booked by {self.renter.username}"
