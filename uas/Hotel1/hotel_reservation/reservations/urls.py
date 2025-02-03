from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Halaman utama
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/reserve/', views.create_reservation, name='create_reservation'),
    path('reservations/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('admin/reservation_report/', views.reservation_report, name='reservation_report'),
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('upload-room-image/<int:room_id>/', views.upload_room_image, name='upload_room_image'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)