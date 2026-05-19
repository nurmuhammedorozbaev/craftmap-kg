from rest_framework import serializers
from .models import Profile, Region, Craft, Master, Booking, Review, Favorite


# --- Профиль ---
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = "__all__"


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
    user = serializers.StringRelatedField()
    craft = CraftSerializer(read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Master
        fields = "__all__"


# --- Заказ ---
class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    craft = CraftSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"


# --- Отзыв ---
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    craft = CraftSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


# --- Избранное ---
class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    craft = CraftSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = "__all__"
