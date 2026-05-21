from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Region, Craft, Master, Booking, Review, Favorite

# --- Пользователь ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

# --- Профиль ---
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "username", "email", "role", "bio", "avatar"]

# --- Регион ---
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"

# --- Ремесло ---
class CraftSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Craft
        fields = "__all__"

# --- Мастер ---
class MasterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    craft = CraftSerializer(read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Master
        fields = "__all__"

# --- Заказ ---
class BookingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    craft = CraftSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"

# --- Отзыв ---
class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    craft = CraftSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"

# --- Избранное ---
class FavoriteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    craft = CraftSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = "__all__"
