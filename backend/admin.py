from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Region, Category, Craft, Master, Booking, Review, Favorite


# --- Кастомный пользователь ---
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Доп. поля", {"fields": ("phone", "role")}),
    )
    list_display = ("username", "email", "phone", "role", "is_staff")
    search_fields = ("username", "email", "phone", "role")


# --- Отзыв Inline ---
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ("user", "text", "is_approved")
    readonly_fields = ("user", "text")
    can_delete = True


# --- Профиль ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")
    search_fields = ("user__username", "bio")


# --- Регион ---
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# --- Категория ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# --- Ремесло ---
@admin.register(Craft)
class CraftAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "region", "price")
    list_filter = ("category", "region")
    search_fields = ("name", "description")
    inlines = [ReviewInline]   # ✅ отзывы внутри карточки ремесла


# --- Мастер ---
@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ("name", "bio")
    search_fields = ("name", "bio")


# --- Бронирование ---
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "craft", "date", "status")
    list_filter = ("status", "date")
    search_fields = ("user__username", "craft__name")
    ordering = ("-date",)


# --- Отзыв ---
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "craft", "user", "text", "is_approved")
    list_filter = ("is_approved", "craft")
    search_fields = ("text", "user__username", "craft__name")
    ordering = ("-id",)
    actions = ["approve_reviews", "disapprove_reviews"]

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "✅ Одобрить выбранные отзывы"

    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_reviews.short_description = "❌ Отклонить выбранные отзывы"


# --- Избранное ---
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "craft")
    search_fields = ("user__username", "craft__name")
