from django.shortcuts import render,redirect
from .models import *
# # Create your views here.
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User.objects.create(
            username=username,
            email=email,
            password=password
        )
        return redirect('home')
    return render(request, 'testapp/register.html')

# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username, password=password)
        if user:
            request.session['user'] = username
            return redirect('home')
        else:
            return render(request, 'testapp/login.html', {
                'error': 'Invalid Username or Password'
            })
    return render(request, 'testapp/login.html')

def home_view(request):
    request.session.flush()   # 🔥 clears old session
    buses = Bus.objects.all()
    return render(request, 'testapp/home.html', {'buses': buses})

def seat_view(request, id):
    bus = Bus.objects.get(id=id)

    request.session['bus'] = bus.id   # ✅ FIXED

    return render(request, 'testapp/seat.html', {'bus': bus})
def passenger_view(request):
    if request.method == "POST":
        seats = request.POST.getlist('seat')
        if not seats:
            return redirect('/home/')   # no seats selected
        request.session['seat'] = seats   # ✅ correct
        return render(request, 'testapp/passenger.html')
    return redirect('/home/')   # ✅ FIXED

def payment_view(request):
    if request.method == "POST":
        request.session['first_name'] = request.POST.get('first_name')
        request.session['last_name'] = request.POST.get('last_name')
        request.session['mobile'] = request.POST.get('mobile')
        request.session['email'] = request.POST.get('email')
        request.session['address'] = request.POST.get('address')
        request.session['age'] = request.POST.get('age')
        request.session['gender'] = request.POST.get('gender')

    bus_id = request.session.get('bus')
    seats = request.session.get('seat')
    if not bus_id or not seats:
        return redirect('/success/')
    bus = Bus.objects.get(id=bus_id)
    seat_count = len(seats)
    total_amount = bus.price * seat_count
    return render(request, 'testapp/payment.html', {
        'bus': bus,
        'seats': seats,
        'seat_count': seat_count,
        'amount': total_amount
    })
def success_view(request):
    return render(request, 'testapp/success.html')