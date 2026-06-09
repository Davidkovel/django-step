from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Car(models.Model):
    FUEL_CHOICES = [
        ('petrol', 'Бензин'),
        ('diesel', 'Дизель'),
        ('gas', 'Газ/Бензин'),
        ('electric', 'Електро'),
        ('hybrid', 'Гібрид'),
    ]
    TRANSMISSION_CHOICES = [
        ('auto', 'Автомат'),
        ('manual', 'Механіка'),
        ('robot', 'Робот'),
        ('variator', 'Варіатор'),
    ]
    DRIVE_CHOICES = [
        ('fwd', 'Передній'),
        ('rwd', 'Задній'),
        ('awd', 'Повний'),
    ]
    BODY_CHOICES = [
        ('sedan', 'Седан'),
        ('suv', 'Позашляховик / Кросовер'),
        ('hatchback', 'Хетчбек'),
        ('wagon', 'Універсал'),
        ('coupe', 'Купе'),
        ('minivan', 'Мінівен'),
        ('pickup', 'Пікап'),
        ('convertible', 'Кабріолет'),
    ]

    brand = models.CharField('Марка', max_length=100)
    model = models.CharField('Модель', max_length=100)
    year = models.PositiveIntegerField('Рік')
    price_usd = models.PositiveIntegerField('Ціна ($)')
    mileage_km = models.PositiveIntegerField('Пробіг (тис. км)')
    fuel = models.CharField('Паливо', max_length=20, choices=FUEL_CHOICES, default='petrol')
    engine_volume = models.DecimalField('Об\'єм двигуна (л)', max_digits=4, decimal_places=2)
    transmission = models.CharField('КПП', max_length=20, choices=TRANSMISSION_CHOICES, default='auto')
    drive = models.CharField('Привід', max_length=10, choices=DRIVE_CHOICES, default='fwd')
    body_type = models.CharField('Тип кузова', max_length=20, choices=BODY_CHOICES, default='sedan')
    color = models.CharField('Колір', max_length=50, default='Чорний')
    city = models.CharField('Місто', max_length=100, default='Київ')
    region = models.CharField('Область', max_length=100, default='Київська')

    description = models.TextField('Опис від продавця', blank=True)
    vin_code = models.CharField('VIN-код', max_length=17, blank=True)
    license_plate = models.CharField('Держ. номер', max_length=15, blank=True)
    owners_count = models.PositiveIntegerField('Кількість власників', default=1)

    is_verified = models.BooleanField('Перевірено', default=False)
    is_first_registration = models.BooleanField('Перша реєстрація', default=False)
    imported_from = models.CharField('Пригнано з', max_length=100, blank=True)

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings', verbose_name='Продавець')
    created_at = models.DateTimeField('Дата публікації', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)
    views_count = models.PositiveIntegerField('Перегляди', default=0)

    class Meta:
        verbose_name = 'Автомобіль'
        verbose_name_plural = 'Автомобілі'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.brand} {self.model} {self.year}'

    def get_absolute_url(self):
        return reverse('cars:detail', kwargs={'pk': self.pk})

    @property
    def main_photo(self):
        photo = self.photos.filter(is_main=True).first()
        if not photo:
            photo = self.photos.first()
        return photo

    @property
    def price_uah(self):
        return self.price_usd * 41


class CarPhoto(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField('Фото', upload_to='cars/photos/')
    is_main = models.BooleanField('Головне фото', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ['order']

    def __str__(self):
        return f'Фото {self.car} #{self.order}'


class SavedCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_cars')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')
        verbose_name = 'Збережене авто'
        verbose_name_plural = 'Збережені авто'