from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.apps import apps
from django.contrib import messages
from .models import Reservation, Room
from .forms import ReservationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

def home(request):
    rooms = Room.objects.all()  # Ambil semua kamar yang tersedia
    reservations = Reservation.objects.filter(user=request.user)
    reservation_form = ReservationForm()

    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            # Menyimpan pemesanan kamar
            reservation_form.instance.user = request.user
            reservation_form.save()
            return redirect('home')  # Setelah pemesanan, kembali ke halaman utama

    context = {
        'rooms': rooms,
        'reservation_form': reservation_form,
        'reservations': reservations
    }
    return render(request, 'home.html', context)

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'reservations/room_list.html', {'rooms': rooms})

def upload_room_image(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return HttpResponse(f"Upload room image page for room: {room.room_number}")

@login_required
def create_reservation(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.room = room
            try:
                reservation.clean()  # Panggil validasi manual
                reservation.save()
                messages.success(request, 'Pemesanan berhasil!')
                return redirect('room_list')
            except ValidationError as e:
                messages.error(request, e.message)
    else:
        form = ReservationForm()
    return render(request, 'reservations/reservation_form.html', {'form': form, 'room': room})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.delete()
    return redirect('home')

def reservation_report(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/reservation_report.html', {'reservations': reservations})

def room_list(request):
    rooms = Room.objects.all()
    if 'search' in request.GET:
        search_query = request.GET['search']
        rooms = rooms.filter(name__icontains=search_query)
    if 'min_price' in request.GET and 'max_price' in request.GET:
        min_price = request.GET['min_price']
        max_price = request.GET['max_price']
        rooms = rooms.filter(price_per_night__gte=min_price, price_per_night__lte=max_price)
    return render(request, 'reservations/room_list.html', {'rooms': rooms})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Ganti dengan URL login setelah pendaftaran
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})


