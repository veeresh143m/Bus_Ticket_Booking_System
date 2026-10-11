from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from .models import Bus, Seat, Booking, SeatLock


# =========================
# REGISTER
# =========================
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'testapp/register.html', {'error': 'User already exists'})
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return redirect('login')
    return render(request, 'testapp/register.html')


# =========================
# LOGIN
# =========================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'testapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'testapp/login.html')


# =========================
# HOME
# =========================
def home_view(request):
    buses = Bus.objects.all()
    source = request.GET.get('source', '').strip()
    destination = request.GET.get('destination', '').strip()

    if source:
        buses = buses.filter(source__icontains=source)
    if destination:
        buses = buses.filter(destination__icontains=destination)

    return render(request, 'testapp/home.html', {
        'buses': buses,
        'source': source,
        'destination': destination,
    })


# =========================
# SEAT PAGE
# =========================
def seat_view(request, id):
    bus = get_object_or_404(Bus, id=id)
    seats = Seat.objects.filter(bus=bus)
    request.session['bus_id'] = bus.id
    return render(request, 'testapp/seat.html', {
        'bus': bus,
        'seats': seats
    })


# =========================
# PASSENGER PAGE
# =========================
def passenger_view(request):
    if request.method == "POST":
        seat_ids = request.POST.getlist('seat')
        if not seat_ids:
            bus_id = request.session.get('bus_id')
            bus = get_object_or_404(Bus, id=bus_id) if bus_id else None
            seats = Seat.objects.filter(bus=bus) if bus else Seat.objects.none()
            return render(request, 'testapp/seat.html', {
                'bus': bus,
                'seats': seats,
                'error': 'Please select at least one seat'
            })
        request.session['seat_ids'] = seat_ids
        return redirect('passenger_page')
    return redirect('home')


@transaction.atomic
def payment_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        passenger_name = request.POST.get('passenger_name', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        bus_id = request.session.get('bus_id')
        seat_ids = request.session.get('seat_ids')

        if not bus_id or not seat_ids:
            return redirect('home')
        if not passenger_name or not mobile:
            return render(request, 'testapp/passenger.html', {
                'error': 'Please enter your passenger name and mobile number'
            })

        bus = get_object_or_404(Bus, id=bus_id)
        seats = list(Seat.objects.filter(id__in=seat_ids, bus=bus))
        if len(seats) != len(seat_ids):
            return redirect('home')

        for seat in seats:
            if seat.is_booked:
                return render(request, 'testapp/payment.html', {
                    'error': 'One or more selected seats are already booked'
                })

        booking = Booking.objects.create(
            user=request.user,
            bus=bus,
            passenger_name=passenger_name,
            mobile=mobile,
            status='CONFIRMED'
        )
        booking.seats.set(seats)
        Seat.objects.filter(id__in=[seat.id for seat in seats]).update(is_booked=True)
        SeatLock.objects.filter(user=request.user).delete()

        request.session['booking_id'] = booking.id
        request.session['passenger_name'] = passenger_name
        request.session['mobile'] = mobile
        request.session['first_name'] = passenger_name

        total_amount = bus.price * len(seats)
        return render(request, 'testapp/payment.html', {
            'bus': bus,
            'seats': seats,
            'seat_count': len(seats),
            'amount': total_amount,
            'booking': booking
        })
    return redirect('home')


# =========================
# SUCCESS PAGE
# =========================
def success_view(request):
    booking_id = request.session.get('booking_id')
    if not booking_id:
        return redirect('home')
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'testapp/success.html', {
        'booking': booking,
        'selected_seats': booking.seats.all(),
    })


def logout_view(request):
    logout(request)
    return redirect('login')


def passenger_page(request):
    bus_id = request.session.get('bus_id')
    seat_ids = request.session.get('seat_ids')
    if not bus_id or not seat_ids:
        return redirect('home')
    bus = get_object_or_404(Bus, id=bus_id)
    return render(request, 'testapp/passenger.html', {
        'bus': bus,
        'seat_ids': seat_ids,
    })