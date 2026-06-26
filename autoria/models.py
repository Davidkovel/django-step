from django.db import models
from django.conf import settings
from django.utils import timezone


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('A', 'Автомат'),
        ('M', 'Механіка'),
    ]

    BODY_TYPE_CHOICES = [
        ('sedan', 'Седан'),
        ('hatchback', 'Хетчбек'),
        ('suv', 'Позашляховик / Кросовер'),
        ('wagon', 'Універсал'),
        ('coupe', 'Купе'),
        ('minivan', 'Мінівен'),
        ('pickup', 'Пікап'),
    ]

    DRIVE_CHOICES = [
        ('fwd', 'Передній'),
        ('rwd', 'Задній'),
        ('awd', 'Повний'),
    ]

    brand = models.CharField(max_length=50, verbose_name='Марка')
    model = models.CharField(max_length=50, verbose_name='Модель')
    year = models.IntegerField(verbose_name='Рік')

    price_usd = models.PositiveIntegerField(verbose_name='Ціна, $')
    price_uah = models.PositiveIntegerField(verbose_name='Ціна, грн')

    mileage = models.PositiveIntegerField(verbose_name='Пробіг, тис. км')
    transmission = models.CharField(max_length=1, choices=TRANSMISSION_CHOICES, verbose_name='КПП')

    engine = models.CharField(max_length=50, verbose_name='Двигун')
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, blank=True, default='', verbose_name='Тип кузова')
    drive = models.CharField(max_length=10, choices=DRIVE_CHOICES, blank=True, default='', verbose_name='Привід')
    color = models.CharField(max_length=50, blank=True, default='', verbose_name='Колір')

    city = models.CharField(max_length=100, default='Київ', verbose_name='Місто')
    region = models.CharField(max_length=100, blank=True, default='', verbose_name='Область')

    plate = models.CharField(max_length=20, verbose_name='Номерний знак')
    vin = models.CharField(max_length=17, blank=True, default='', verbose_name='VIN')

    generation = models.CharField(max_length=100, blank=True, default='', verbose_name='Покоління')
    modification = models.CharField(max_length=100, blank=True, default='', verbose_name='Модифікація')
    description = models.TextField(blank=True, default='', verbose_name='Опис')

    seller_name = models.CharField(max_length=100, blank=True, default='', verbose_name="Ім'я продавця")
    seller_phone = models.CharField(max_length=20, blank=True, default='', verbose_name='Телефон')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cars', null=True, blank=True)
    posted = models.CharField(max_length=50, blank=True, default='')
    image = models.URLField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"

    def save(self, *args, **kwargs):
        if not self.price_uah and self.price_usd:
            self.price_uah = self.price_usd * 44
        if not self.posted:
            self.posted = 'Щойно'
        if not self.image:
            self.image = '/static/images/cars/bmw.jpg'
        super().save(*args, **kwargs)

    @property
    def price(self):
        return self.price_usd

    @property
    def gallery_images(self):
        images = [self.image] if self.image else []
        images.extend(self.images.values_list('image', flat=True))
        return images or ['/static/images/cars/bmw.jpg']

    @property
    def body_type_display(self):
        return dict(self.BODY_TYPE_CHOICES).get(self.body_type, self.body_type or '—')

    @property
    def drive_display(self):
        return dict(self.DRIVE_CHOICES).get(self.drive, self.drive or '—')

    @property
    def transmission_label(self):
        return self.get_transmission_display()

    @property
    def old_price(self):
        return None

    @property
    def credit_monthly(self):
        return int(self.price_uah / 36) if self.price_uah else 0

    @property
    def zip_code(self):
        return ''

    @property
    def tags(self):
        return ['Вперше на AUTO.RIA']

    @property
    def owners(self):
        return 1

    @property
    def state(self):
        return '—'

    @property
    def doors(self):
        return 4

    @property
    def seats(self):
        return 5

    @property
    def eco_standard(self):
        return '—'

    @property
    def fuel_city(self):
        return '—'

    @property
    def fuel_highway(self):
        return '—'

    @property
    def fuel_mixed(self):
        return '—'

    @property
    def seller_verified(self):
        return False

    @property
    def seller_years(self):
        return 'Новий продавець'

    @property
    def seller_online(self):
        return f'Опубліковано {timezone.localtime(self.created_at).strftime("%d.%m.%Y")}'

    @property
    def safety(self):
        return '—'

    @property
    def comfort(self):
        return '—'

    @property
    def multimedia(self):
        return '—'

    @property
    def headlights(self):
        return '—'

    @property
    def conditioning(self):
        return '—'

    @property
    def power_steering(self):
        return '—'

    @property
    def steering_adjustment(self):
        return '—'

    @property
    def spare_wheel(self):
        return '—'

    @property
    def optics(self):
        return '—'

    @property
    def parking_help(self):
        return '—'

    @property
    def airbags(self):
        return '—'

    @property
    def electric_windows(self):
        return '—'

    @property
    def seat_adjustment(self):
        return '—'

    @property
    def interior_color(self):
        return '—'

    @property
    def interior_material(self):
        return '—'


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'car'], name='unique_user_favorite_car'),
        ]

    def __str__(self):
        return f'{self.user} - {self.car}'


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.car} image {self.order + 1}'
