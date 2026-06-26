# Generated manually

from django.db import migrations, models
import django.utils.timezone


def seed_initial_cars(apps, schema_editor):
    Car = apps.get_model('autoria', 'Car')
    if Car.objects.exists():
        return

    Car.objects.bulk_create([
        Car(
            brand='Toyota',
            model='Camry',
            year=2021,
            price_usd=28500,
            price_uah=1259700,
            mileage=45,
            transmission='A',
            engine='2.5 Бензин',
            body_type='sedan',
            drive='fwd',
            color='Білий',
            city='Київ',
            region='Київська обл.',
            plate='АА 1234 ВВ',
            vin='JTNBF1FK5MJ012345',
            generation='XV70, 8 покоління',
            modification='2.5 AT (209 к.с.)',
            description='В відмінному стані, один власник, повний сервіс у дилера.',
            seller_name='Олександр',
            seller_phone='(067) XXX XX XX',
            posted='3 дні тому',
            image='/static/images/cars/bmw.jpg',
        ),
        Car(
            brand='BMW',
            model='320d',
            year=2019,
            price_usd=23000,
            price_uah=1016600,
            mileage=120,
            transmission='A',
            engine='2.0 Дизель',
            body_type='sedan',
            drive='rwd',
            color='Чорний',
            city='Вінниця',
            region='Вінницька обл.',
            plate='ВІ 5678 АН',
            vin='WBA5R1C50KAK78901',
            generation='G20, 7 покоління',
            modification='2.0 AT (190 к.с.)',
            description='M-пакет, шкіряний салон, LED фари, навігація. Без ДТП.',
            seller_name='Дмитро',
            seller_phone='(097) XXX XX XX',
            posted='Місяць тому',
            image='/static/images/cars/bmw.jpg',
        ),
        Car(
            brand='Volkswagen',
            model='Golf 8',
            year=2022,
            price_usd=21000,
            price_uah=928200,
            mileage=30,
            transmission='M',
            engine='1.5 Бензин',
            body_type='hatchback',
            drive='fwd',
            color='Сірий',
            city='Львів',
            region='Львівська обл.',
            plate='ВС 9012 КР',
            vin='WVWZZZCDZMW456789',
            generation='Mk8, 8 покоління',
            modification='1.5 MT (150 к.с.)',
            description='Як нова, гаражне зберігання, зимова гума в комплекті.',
            seller_name='Марія',
            seller_phone='(063) XXX XX XX',
            posted='18 днів тому',
            image='/static/images/cars/bmw.jpg',
        ),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('autoria', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='body_type',
            field=models.CharField(blank=True, choices=[('sedan', 'Седан'), ('hatchback', 'Хетчбек'), ('suv', 'Позашляховик / Кросовер'), ('wagon', 'Універсал'), ('coupe', 'Купе'), ('minivan', 'Мінівен'), ('pickup', 'Пікап')], default='', max_length=20, verbose_name='Тип кузова'),
        ),
        migrations.AddField(
            model_name='car',
            name='color',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Колір'),
        ),
        migrations.AddField(
            model_name='car',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Опис'),
        ),
        migrations.AddField(
            model_name='car',
            name='drive',
            field=models.CharField(blank=True, choices=[('fwd', 'Передній'), ('rwd', 'Задній'), ('awd', 'Повний')], default='', max_length=10, verbose_name='Привід'),
        ),
        migrations.AddField(
            model_name='car',
            name='generation',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Покоління'),
        ),
        migrations.AddField(
            model_name='car',
            name='modification',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Модифікація'),
        ),
        migrations.AddField(
            model_name='car',
            name='region',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Область'),
        ),
        migrations.AddField(
            model_name='car',
            name='seller_name',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name="Ім'я продавця"),
        ),
        migrations.AddField(
            model_name='car',
            name='seller_phone',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='car',
            name='vin',
            field=models.CharField(blank=True, default='', max_length=17, verbose_name='VIN'),
        ),
        migrations.AlterField(
            model_name='car',
            name='city',
            field=models.CharField(default='Київ', max_length=100, verbose_name='Місто'),
        ),
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='car',
            name='posted',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='car',
            name='transmission',
            field=models.CharField(choices=[('A', 'Автомат'), ('M', 'Механіка')], max_length=1, verbose_name='КПП'),
        ),
        migrations.RunPython(seed_initial_cars, migrations.RunPython.noop),
    ]
