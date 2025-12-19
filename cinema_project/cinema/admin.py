from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Movie, Hall, Seans, Seat, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'duration')
    search_fields = ('title',)


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('number', 'rows', 'seats_per_row', 'seats_total')
    list_editable = ('rows', 'seats_per_row')


@admin.register(Seans)
class SeansAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'start_time', 'price')
    list_filter = ('hall', 'movie')
    search_fields = ('movie__title',)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('hall', 'row', 'seat_number')
    list_filter = ('hall',)
    ordering = ('hall', 'row', 'seat_number')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('seans', 'user', 'seat', 'booked_at')
    list_filter = ('seans', 'user')
    search_fields = ('user__username', 'seans__movie__title')
