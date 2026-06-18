"""
Команда для заполнения базы тестовыми объявлениями.

Запуск:
    python manage.py seed_cars

Дополнительно можно очистить старые данные перед сидированием:
    python manage.py seed_cars --flush
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Car

SAMPLE_CARS = [
    dict(brand='BMW', model='X6', year=2016, price_usd=36000, mileage_km=130,
         fuel='diesel', engine_volume='2.99', transmission='auto', drive='awd',
         body_type='suv', color='Чорний', city='Київ', region='Київська',
         vin_code='WBAKV610X00S72676', license_plate='BX 7179 IA',
         owners_count=1, is_verified=True, is_first_registration=True,
         imported_from='Німеччини',
         description='Автомобіль пригнаний з Німеччини для себе — не «під продаж». M-пакет, повна комплектація.'),

    dict(brand='Mercedes-Benz', model='E-Class', year=2019, price_usd=70250, mileage_km=52,
         fuel='petrol', engine_volume='3.98', transmission='auto', drive='rwd',
         body_type='sedan', color='Зелений', city='Одеса', region='Одеська',
         vin_code='WDDZF8KB4KA625748', license_plate='KI 0007 CB',
         owners_count=1, is_verified=True, is_first_registration=False,
         description='Авто в ідеалі. Перекупщиків не турбувати. 700 к.с. під капотом.'),

    dict(brand='Audi', model='A6', year=2022, price_usd=52000, mileage_km=18,
         fuel='petrol', engine_volume='2.0', transmission='auto', drive='awd',
         body_type='sedan', color='Білий', city='Львів', region='Львівська',
         vin_code='WAUZZZ4G7KN012345', license_plate='BC 1234 AA',
         owners_count=1, is_verified=True, is_first_registration=True,
         description='Один власник, повна сервісна історія в офіційного дилера.'),

    dict(brand='Skoda', model='Kodiaq', year=2018, price_usd=26000, mileage_km=60,
         fuel='petrol', engine_volume='2.0', transmission='auto', drive='awd',
         body_type='suv', color='Сірий', city='Харків', region='Харківська',
         vin_code='TMBJM9NS5J0123456', license_plate='BO 1200 BM',
         owners_count=2, is_verified=True, is_first_registration=False,
         description='Перевірений VIN, без ДТП, обслуговувався у дилера.'),

    dict(brand='Audi', model='Q5', year=2021, price_usd=29800, mileage_km=162,
         fuel='diesel', engine_volume='2.0', transmission='auto', drive='awd',
         body_type='suv', color='Синій', city='Дніпро', region='Дніпропетровська',
         license_plate='', owners_count=1, is_verified=False, is_first_registration=False,
         description='Дизельний двигун, економний, повний привід quattro.'),

    dict(brand='Land Rover', model='Range Rover Sport', year=2022, price_usd=118000, mileage_km=59,
         fuel='petrol', engine_volume='3.0', transmission='auto', drive='awd',
         body_type='suv', color='Чорний', city='Київ', region='Київська',
         vin_code='SALWA2SU8NA123456', license_plate='KE 8888 BX',
         owners_count=1, is_verified=True, is_first_registration=True,
         description='Максимальна комплектація, пневмопідвіска, панорамний дах.'),

    dict(brand='Nissan', model='Murano', year=2013, price_usd=12800, mileage_km=223,
         fuel='petrol', engine_volume='3.5', transmission='variator', drive='awd',
         body_type='suv', color='Бронзовий', city='Одеса', region='Одеська',
         vin_code='JN1AZ4EH4DM123456', license_plate='BH 2446 KB',
         owners_count=2, is_verified=True, is_first_registration=False,
         description='Надійний варіатор, комфортний салон, нові шини.'),

    dict(brand='Suzuki', model='Vitara', year=2020, price_usd=11138, mileage_km=59,
         fuel='petrol', engine_volume='1.6', transmission='auto', drive='fwd',
         body_type='suv', color='Червоний', city='Вінниця', region='Вінницька',
         license_plate='', owners_count=1, is_verified=True, is_first_registration=False,
         description='Компактний кросовер, економний, ідеальний стан.'),

    dict(brand='Jaguar', model='F-Pace', year=2017, price_usd=17700, mileage_km=234,
         fuel='diesel', engine_volume='2.0', transmission='auto', drive='awd',
         body_type='suv', color='Сірий', city='Київ', region='Київська',
         vin_code='SADCA2BN8HA123456', license_plate='BA 6267 EH',
         owners_count=2, is_verified=True, is_first_registration=False,
         description='Британський преміум-кросовер, шкіряний салон.'),

    dict(brand='Peugeot', model='206', year=2007, price_usd=2399, mileage_km=240,
         fuel='petrol', engine_volume='1.4', transmission='manual', drive='fwd',
         body_type='hatchback', color='Синій', city='Полтава', region='Полтавська',
         license_plate='AA 2890 MH', owners_count=3, is_verified=False, is_first_registration=False,
         description='Бюджетний варіант для початківців, економний витрата.'),
]


class Command(BaseCommand):
    help = 'Заповнює базу тестовими оголошеннями автомобілів (без фото — placeholder)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Видалити всі існуючі оголошення перед сидируванням',
        )

    def handle(self, *args, **options):
        if options['flush']:
            deleted, _ = Car.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Видалено {deleted} старих записів.'))

        # Понадобится продавец — берём первого superuser/staff, либо создаём демо-продавца
        seller = User.objects.filter(is_superuser=True).first()
        if not seller:
            seller, created = User.objects.get_or_create(
                username='demo_seller',
                defaults={'email': 'demo_seller@example.com', 'first_name': 'Демо', 'last_name': 'Продавець'}
            )
            if created:
                seller.set_password('demo12345')
                seller.save()
                self.stdout.write(self.style.SUCCESS(
                    "Створено демо-продавця: username='demo_seller', password='demo12345'"
                ))

        created_count = 0
        for data in SAMPLE_CARS:
            car, created = Car.objects.get_or_create(
                brand=data['brand'], model=data['model'], year=data['year'],
                vin_code=data.get('vin_code', ''),
                defaults={**data, 'seller': seller},
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Готово! Додано {created_count} нових оголошень. Всього в базі: {Car.objects.count()}.'
        ))
        self.stdout.write(self.style.WARNING(
            'Зверни увагу: фото (CarPhoto) не створювались автоматично — '
            'без фото картки покажуть іконку-заглушку 🚗. '
            'Додай фото через /admin/ або через CarPhoto.objects.create(car=..., image=...).'
        ))
