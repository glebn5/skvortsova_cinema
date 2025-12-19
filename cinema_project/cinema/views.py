from django.shortcuts import render, get_object_or_404
from .models import Movie, Seans, Hall, Seat
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from .models import Booking
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def home(request):
    """Главная — выводим ближайшие сеансы."""
    seanses = Seans.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    return render(request, 'home.html', {'seanses': seanses})


def movie_detail(request, movie_id):
    """Страница фильма."""
    movie = get_object_or_404(Movie, id=movie_id)
    seanses = movie.seanses.order_by('start_time')
    return render(request, 'movie_detail.html', {
        'movie': movie,
        'seanses': seanses,
    })

@login_required
def book_seat(request, seans_id, seat_id):
    seans = get_object_or_404(Seans, id=seans_id)
    seat = get_object_or_404(Seat, id=seat_id)

    # Проверяем, занято ли место
    exists = Booking.objects.filter(seans=seans, seat=seat).exists()
    if exists:
        messages.error(request, "Это место уже занято!")
        return redirect('seans_detail', seans_id=seans_id)

    # Создаём бронь
    Booking.objects.create(
        seans=seans,
        seat=seat,
        user=request.user
    )

    messages.success(request, "Место успешно забронировано!")
    return redirect('seans_detail', seans_id=seans_id)


def seans_detail(request, seans_id):
    """Страница сеанса — показываем схему мест."""
    seans = get_object_or_404(Seans, id=seans_id)
    hall = seans.hall

    # Получаем ВСЕ места зала
    seats = Seat.objects.filter(hall=hall).order_by('row', 'seat_number')

    # Делаем матрицу вида:
    # [
    #   [место1, место2, ...],
    #   [место1, место2, ...],
    # ]
    hall_scheme = []
    for row_num in range(1, hall.rows + 1):
        row_seats = seats.filter(row=row_num)
        hall_scheme.append(row_seats)

    # Занятые места
    booked_seats = seans.bookings.values_list('seat_id', flat=True)

    return render(request, 'seans_detail.html', {
        'seans': seans,
        'hall': hall,
        'hall_scheme': hall_scheme,
        'booked_seats': booked_seats,
    })
