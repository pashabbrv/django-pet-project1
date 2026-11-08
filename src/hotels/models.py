from django.db import models


class Room(models.Model):
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rooms"
        managed = False


class Booking(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    date_start = models.DateField()
    date_end = models.DateField()

    class Meta:
        db_table = "bookings"
        managed = False
