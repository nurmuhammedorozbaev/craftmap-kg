from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


# --- Кастомный пользователь ---
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    role = models.CharField(max_length=50, default="visitor", verbose_name="Роль")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


# --- Профиль ---
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    bio = models.TextField(blank=True, verbose_name="Биография")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватар")
    website = models.URLField(blank=True, null=True, verbose_name="Сайт")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.user.username} ({self.user.role})"


# --- Категории ---
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


# --- Регионы ---
class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name="Регион")

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return self.name


# --- Мастера ---
class Master(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя мастера")
    bio = models.TextField(blank=True, verbose_name="Биография")

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):
        return self.name


# --- Ремёсла ---
class Craft(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Цена")
    image = models.ImageField(upload_to="crafts/", blank=True, null=True, verbose_name="Изображение")

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Регион")

    masters = models.ManyToManyField(Master, related_name="crafts", blank=True, verbose_name="Мастера")

    latitude = models.FloatField(null=True, blank=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Долгота")

    class Meta:
        verbose_name = "Ремесло"
        verbose_name_plural = "Ремёсла"

    def __str__(self):
        return self.name


# --- Бронирование ---
class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидание"),
        ("approved", "Одобрено"),
        ("completed", "Завершено"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    craft = models.ForeignKey(Craft, on_delete=models.CASCADE, verbose_name="Ремесло")
    date = models.DateTimeField(default=now, verbose_name="Дата бронирования")
    notes = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"{self.user.username} → {self.craft.name} ({self.get_status_display()})"


# --- Отзывы ---
class Review(models.Model):
    craft = models.ForeignKey(Craft, on_delete=models.CASCADE, related_name="reviews", verbose_name="Ремесло")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        choices=[(i, f"{i} ⭐") for i in range(1, 6)],
        default=5
    )
    is_approved = models.BooleanField(default=True, verbose_name="Одобрен")
    created_at = models.DateTimeField(default=now, verbose_name="Дата отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв {self.user.username} о {self.craft.name} ({self.rating}⭐)"


# --- Избранное ---
class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    craft = models.ForeignKey(Craft, on_delete=models.CASCADE, verbose_name="Ремесло")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return f"{self.user.username} ♥ {self.craft.name}"
