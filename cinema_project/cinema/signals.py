from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Hall, Seat


@receiver(post_save, sender=Hall)
def create_seats_for_hall(sender, instance, created, **kwargs):
    if created:
        hall = instance
        for row in range(1, hall.rows + 1):
            for seat in range(1, hall.seats_per_row + 1):
                Seat.objects.create(
                    hall=hall,
                    row=row,
                    seat_number=seat
                )
