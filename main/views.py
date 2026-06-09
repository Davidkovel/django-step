from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Car, SavedCar


def home(request):
    cars = Car.objects.prefetch_related('photos').select_related('seller')

    # Search/filter
    brand = request.GET.get('brand', '').strip()
    model = request.GET.get('model', '').strip()
    price_from = request.GET.get('price_from', '').strip()
    price_to = request.GET.get('price_to', '').strip()
    year_from = request.GET.get('year_from', '').strip()
    year_to = request.GET.get('year_to', '').strip()
    fuel = request.GET.get('fuel', '').strip()
    transmission = request.GET.get('transmission', '').strip()
    region = request.GET.get('region', '').strip()

    if brand:
        cars = cars.filter(brand__icontains=brand)
    if model:
        cars = cars.filter(model__icontains=model)
    if price_from:
        try:
            cars = cars.filter(price_usd__gte=int(price_from))
        except ValueError:
            pass
    if price_to:
        try:
            cars = cars.filter(price_usd__lte=int(price_to))
        except ValueError:
            pass
    if year_from:
        try:
            cars = cars.filter(year__gte=int(year_from))
        except ValueError:
            pass
    if year_to:
        try:
            cars = cars.filter(year__lte=int(year_to))
        except ValueError:
            pass
    if fuel:
        cars = cars.filter(fuel=fuel)
    if transmission:
        cars = cars.filter(transmission=transmission)
    if region:
        cars = cars.filter(region__icontains=region)

    total_count = cars.count()

    brands = Car.objects.values_list('brand', flat=True).distinct().order_by('brand')
    regions = Car.objects.values_list('region', flat=True).distinct().order_by('region')

    context = {
        'cars': cars,
        'total_count': total_count,
        'brands': brands,
        'regions': regions,
        'fuel_choices': Car.FUEL_CHOICES,
        'transmission_choices': Car.TRANSMISSION_CHOICES,
        'filters': {
            'brand': brand,
            'model': model,
            'price_from': price_from,
            'price_to': price_to,
            'year_from': year_from,
            'year_to': year_to,
            'fuel': fuel,
            'transmission': transmission,
            'region': region,
        }
    }
    return render(request, 'home.html', context)


def car_detail(request, pk):
    car = get_object_or_404(
        Car.objects.prefetch_related('photos').select_related('seller'),
        pk=pk
    )
    # Increment view count
    Car.objects.filter(pk=pk).update(views_count=car.views_count + 1)

    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedCar.objects.filter(user=request.user, car=car).exists()

    similar_cars = Car.objects.filter(
        brand=car.brand
    ).exclude(pk=pk).prefetch_related('photos')[:6]

    context = {
        'car': car,
        'is_saved': is_saved,
        'similar_cars': similar_cars,
        'photos': car.photos.all(),
    }
    return render(request, 'cars/detail.html', context)