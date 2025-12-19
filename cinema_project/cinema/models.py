from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Длительность в минутах")

    def __str__(self):
        return f"Фильм '{self.title}'"


class Hall(models.Model):
    number = models.PositiveIntegerField(unique=True)
    rows = models.PositiveIntegerField(default=10)
    seats_per_row = models.PositiveIntegerField(default=12)

    def seats_total(self):
        return self.rows * self.seats_per_row

    def __str__(self):
        return f"Зал №{self.number}"


class Seans(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seanses')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seanses')
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return (
            f"Сеанс '{self.movie.title}' "
            f"в зале №{self.hall.number} "
            f"в {self.start_time}"
        )


class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField()
    seat_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('hall', 'row', 'seat_number')

    def __str__(self):
        return (
            f"Место {self.seat_number} | Ряд {self.row} | "
            f"Зал №{self.hall.number}"
        )


class Booking(models.Model):
    seans = models.ForeignKey(Seans, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seans', 'seat')

    def __str__(self):
        return (
            f"Бронь: {self.seat} | "
            f"Сеанс '{self.seans.movie.title}' | "
            f"{self.user.username}"
        )
