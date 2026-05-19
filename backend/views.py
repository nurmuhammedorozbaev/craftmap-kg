from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from datetime import timedelta
from django.db.models import Avg

from .models import CustomUser, Profile, Region, Craft, Master, Booking, Review, Favorite, Category
from .forms import CustomUserCreationForm


# --- Главная ---
def home_view(request):
    crafts_count = Craft.objects.count()
    masters_count = Master.objects.count()
    regions_count = Region.objects.count()
    return render(request, "backend/home.html", {
        "crafts_count": crafts_count,
        "masters_count": masters_count,
        "regions_count": regions_count,
    })


# --- Список ремёсел ---
def crafts_view(request):
    crafts = Craft.objects.all()
    regions = Region.objects.all()
    categories = Category.objects.all()

    # Поиск
    search_query = request.GET.get("search")
    if search_query:
        crafts = crafts.filter(name__icontains=search_query)

    # Фильтр по категории
    category = request.GET.get("category")
    if category and category != "Все категории":
        crafts = crafts.filter(category__name=category)

    # Фильтр по региону
    region_name = request.GET.get("region")
    if region_name and region_name != "Все регионы":
        crafts = crafts.filter(region__name=region_name)

    return render(request, "backend/crafts.html", {
        "crafts": crafts,
        "regions": regions,
        "categories": categories,
    })


# --- Детали ремесла + отзывы ---
def craft_detail_view(request, pk):
    craft = get_object_or_404(Craft, pk=pk)
    reviews = Review.objects.filter(craft=craft, is_approved=True)
    masters = craft.masters.all()

    # Добавление отзыва
    if request.method == "POST" and request.user.is_authenticated:
        text = request.POST.get("text")
        rating = request.POST.get("rating")
        if text and rating:
            Review.objects.create(
                craft=craft,
                user=request.user,
                text=text,
                rating=int(rating),
                is_approved=False  # админ потом одобрит
            )
            return redirect("backend:craft_detail", pk=pk)

    # Средний рейтинг
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]

    return render(request, "backend/craft_detail.html", {
        "craft": craft,
        "reviews": reviews,
        "masters": masters,
        "avg_rating": avg_rating,
    })


# --- Регистрация ---
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Профиль создаётся сигналом
            login(request, user)
            return redirect("backend:home")
    else:
        form = CustomUserCreationForm()
    return render(request, "backend/register.html", {"form": form})


# --- Вход ---
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("backend:home")
        else:
            return render(request, "backend/login.html", {"error": "Неверные данные"})
    return render(request, "backend/login.html")


# --- Выход ---
def logout_view(request):
    logout(request)
    return redirect("backend:home")


# --- Профиль ---
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user, defaults={"bio": ""})
    bookings = Booking.objects.filter(user=request.user)
    favorites = Favorite.objects.filter(user=request.user)

    # Статистика
    approved_count = bookings.filter(status="approved").count()
    pending_count = bookings.filter(status="pending").count()
    completed_count = bookings.filter(status="completed").count()

    today = now().date()
    tomorrow = today + timedelta(days=1)
    today_count = bookings.filter(date__gte=today, date__lt=tomorrow).count()

    return render(request, "backend/profile.html", {
        "profile": profile,
        "bookings": bookings,
        "favorites": favorites,
        "approved_count": approved_count,
        "pending_count": pending_count,
        "completed_count": completed_count,
        "today_count": today_count,
    })


# --- Бронирование ---
@login_required
def booking_view(request, craft_id):
    craft = get_object_or_404(Craft, id=craft_id)
    if request.method == "POST":
        Booking.objects.create(
            user=request.user,
            craft=craft,
            date=now(),
            notes=request.POST.get("notes", ""),
            status="pending"
        )
        return redirect("backend:profile")
    return render(request, "backend/booking_form.html", {"craft": craft})


# --- Избранное ---
@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, "backend/favorites.html", {"favorites": favorites})


@login_required
def add_favorite(request, craft_id):
    if request.method == "POST":
        craft = get_object_or_404(Craft, id=craft_id)
        Favorite.objects.get_or_create(user=request.user, craft=craft)
    return redirect("backend:favorites")


@login_required
def remove_favorite(request, craft_id):
    if request.method == "POST":
        craft = get_object_or_404(Craft, id=craft_id)
        Favorite.objects.filter(user=request.user, craft=craft).delete()
    return redirect("backend:favorites")


# --- Карта ---
def map_view(request):
    regions = Region.objects.all()
    categories = Category.objects.all()
    crafts = Craft.objects.all()
    return render(request, "backend/map.html", {
        "regions": regions,
        "categories": categories,
        "crafts": crafts,
    })


# --- Админ: список бронирований ---
@login_required
def booking_list_admin(request):
    if not request.user.is_staff:
        return redirect("backend:home")

    bookings = Booking.objects.all().select_related("user", "craft")
    return render(request, "backend/booking_list_admin.html", {"bookings": bookings})


# --- Админ: обновление статуса бронирования ---
@login_required
@require_POST
def update_booking_status(request, booking_id):
    if not request.user.is_staff:
        return redirect("backend:home")

    booking = get_object_or_404(Booking, id=booking_id)
    new_status = request.POST.get("status")

    if new_status in dict(Booking.STATUS_CHOICES).keys():
        booking.status = new_status
        booking.save()

    return redirect("backend:booking_list_admin")
