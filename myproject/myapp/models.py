from django.db import models
from django.core.validators import MinValueValidator

# Первая модель (Item)
class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    emailAdress = models.EmailField(verbose_name="Email")
    phoneNumber = models.CharField(max_length=20, verbose_name="Телефон")

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"

    def __str__(self):
        return self.name

# Вторая модель (Product - для интернет-магазина)
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0.01)]
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    available = models.BooleanField(default=True, verbose_name="Доступен")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"