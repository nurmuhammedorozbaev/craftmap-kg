from django.urls import path
from . import views

app_name = "backend"

urlpatterns = [
    # --- Главная ---
    path("", views.home_view, name="home"),

    # --- Ремёсла ---
    path("crafts/", views.crafts_view, name="crafts"),
    path("craft/<int:pk>/", views.craft_detail_view, name="craft_detail"),

    # --- Аутентификация ---
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # --- Совместимость с Django (redirect на login) ---
    path("accounts/login/", views.login_view, name="login"),

    # --- Профиль ---
    path("profile/", views.profile_view, name="profile"),

    # --- Бронирование ---
    path("craft/<int:craft_id>/booking/", views.booking_view, name="booking_view"),
    path("bookings/admin/", views.booking_list_admin, name="booking_list_admin"),
    path("bookings/<int:booking_id>/update/", views.update_booking_status, name="update_booking_status"),

    # --- Избранное ---
    path("favorites/", views.favorites_view, name="favorites"),
    path("craft/<int:craft_id>/favorite/add/", views.add_favorite, name="add_favorite"),
    path("craft/<int:craft_id>/favorite/remove/", views.remove_favorite, name="remove_favorite"),

    # --- Карта ---
    path("map/", views.map_view, name="map"),
]
