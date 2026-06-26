from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .car_catalog import CAR_MODELS
from .models import Car, CarImage


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логін',
        widget=forms.TextInput(attrs={
            'class': 'auth-field__input',
            'placeholder': 'Ваш логін',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'auth-field__input',
            'placeholder': 'Ваш пароль',
        }),
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'auth-field__input',
            'placeholder': 'name@example.com',
            'required': True,
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Логін',
            'password1': 'Пароль',
            'password2': 'Повторіть пароль',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'auth-field__input',
                'placeholder': 'Придумайте логін',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'auth-field__input',
            'placeholder': 'Мінімум 8 символів',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'auth-field__input',
            'placeholder': 'Повторіть пароль',
        })

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Користувач з такою поштою вже існує.')
        return email


class CarForm(forms.ModelForm):
    extra_images = forms.CharField(
        label='Додаткові фото',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'sell-field__textarea',
            'placeholder': 'Кожне посилання на фото з нового рядка',
            'rows': 4,
        }),
    )

    class Meta:
        model = Car
        fields = [
            'brand',
            'model',
            'year',
            'price_usd',
            'mileage',
            'transmission',
            'engine',
            'body_type',
            'drive',
            'color',
            'city',
            'region',
            'plate',
            'vin',
            'generation',
            'modification',
            'description',
            'seller_name',
            'seller_phone',
            'image',
            'extra_images',
        ]
        widgets = {
            'brand': forms.TextInput(attrs={
                'class': 'sell-field__input',
                'placeholder': 'Почніть вводити марку',
                'list': 'car-brand-options',
                'autocomplete': 'off',
            }),
            'model': forms.TextInput(attrs={
                'class': 'sell-field__input',
                'placeholder': 'Спочатку виберіть марку',
                'list': 'car-model-options',
                'autocomplete': 'off',
            }),
            'year': forms.NumberInput(attrs={
                'class': 'sell-field__input',
                'placeholder': '2020',
                'min': 1980,
                'max': 2026,
            }),
            'price_usd': forms.NumberInput(attrs={
                'class': 'sell-field__input',
                'placeholder': '15000',
                'min': 100,
            }),
            'mileage': forms.NumberInput(attrs={
                'class': 'sell-field__input',
                'placeholder': '100',
                'min': 0,
            }),
            'transmission': forms.Select(attrs={'class': 'sell-field__select'}),
            'engine': forms.TextInput(attrs={
                'class': 'sell-field__input',
                'placeholder': '2.0 Бензин',
            }),
            'body_type': forms.Select(attrs={'class': 'sell-field__select'}),
            'drive': forms.Select(attrs={'class': 'sell-field__select'}),
            'color': forms.TextInput(attrs={
                'class': 'sell-field__input',
                'placeholder': 'Білий',
            }),
            'city': forms.TextInput(attrs={
                'class': 'sell-field__input',
                'placeholder': 'Київ',
            }),
            'region': forms.TextInput(attrs={
                'class': 'sell-field__input',
                'placeholder': 'Київська обл.',
            }),
            'plate': forms.TextInput(attrs={
                'class': 'sell-field__input',
                'placeholder': 'АА 1234 ВВ',
            }),
            'vin': forms.TextInput(attrs={
                'class': 'sell-field__input',
                'placeholder': 'JTNBF1FK5MJ012345',
                'maxlength': 17,
            }),
            'generation': forms.TextInput(attrs={
                'class': 'sell-field__input',
                'placeholder': 'XV70, 8 покоління',
            }),
            'modification': forms.TextInput(attrs={
                'class': 'sell-field__input',
                'placeholder': '2.5 AT (209 к.с.)',
            }),
            'description': forms.Textarea(attrs={
                'class': 'sell-field__textarea',
                'placeholder': 'Опишіть стан авто, комплектацію, історію обслуговування...',
                'rows': 5,
            }),
            'seller_name': forms.TextInput(attrs={
                'class': 'sell-field__input',
                'placeholder': "Ваше ім'я",
            }),
            'seller_phone': forms.TextInput(attrs={
                'class': 'sell-field__input',
                'placeholder': '(067) 123 45 67',
            }),
            'image': forms.URLInput(attrs={
                'class': 'sell-field__input',
                'placeholder': 'https://... (посилання на фото авто)',
            }),
        }
        labels = {
            'brand': 'Марка',
            'model': 'Модель',
            'year': 'Рік випуску',
            'price_usd': 'Ціна, $',
            'mileage': 'Пробіг, тис. км',
            'transmission': 'Коробка передач',
            'engine': 'Двигун',
            'body_type': 'Тип кузова',
            'drive': 'Привід',
            'color': 'Колір',
            'city': 'Місто',
            'region': 'Область',
            'plate': 'Номерний знак',
            'vin': 'VIN-код',
            'generation': 'Покоління',
            'modification': 'Модифікація',
            'description': 'Опис',
            'seller_name': "Ім'я продавця",
            'seller_phone': 'Телефон',
            'image': 'Посилання на фото',
            'extra_images': 'Додаткові фото',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        optional_fields = [
            'body_type', 'drive', 'color', 'region', 'vin',
            'generation', 'modification', 'description',
            'seller_name', 'seller_phone', 'image',
        ]
        for field_name in optional_fields:
            self.fields[field_name].required = False

        self.fields['brand'].widget.attrs['data-car-catalog'] = 'brand'
        self.fields['model'].widget.attrs['data-car-catalog'] = 'model'
        if self.instance and self.instance.pk:
            self.fields['extra_images'].initial = '\n'.join(self.instance.images.values_list('image', flat=True))

    def clean_brand(self):
        brand = self.cleaned_data['brand'].strip()
        matching_brand = next((known_brand for known_brand in CAR_MODELS if known_brand.lower() == brand.lower()), None)
        if not matching_brand:
            raise forms.ValidationError('Оберіть марку зі списку.')
        return matching_brand

    def clean_model(self):
        model = self.cleaned_data['model'].strip()
        brand = self.cleaned_data.get('brand')
        if not brand:
            return model

        matching_model = next((known_model for known_model in CAR_MODELS[brand] if known_model.lower() == model.lower()), None)
        if not matching_model:
            raise forms.ValidationError('Оберіть модель, яка відповідає вибраній марці.')
        return matching_model

    def clean_year(self):
        year = self.cleaned_data['year']
        if year < 1980 or year > 2026:
            raise forms.ValidationError('Вкажіть коректний рік випуску.')
        return year

    def clean_extra_images(self):
        value = self.cleaned_data.get('extra_images', '')
        urls = [url.strip() for url in value.replace(',', '\n').splitlines() if url.strip()]
        validator = forms.URLField()
        for url in urls:
            validator.clean(url)
        return urls

    def save(self, commit=True):
        car = super().save(commit=False)
        if car.price_usd:
            car.price_uah = car.price_usd * 44
        if commit:
            car.save()
            self.save_m2m()
            self.save_extra_images(car)
        return car

    def save_extra_images(self, car):
        car.images.all().delete()
        CarImage.objects.bulk_create([
            CarImage(car=car, image=image, order=index)
            for index, image in enumerate(self.cleaned_data.get('extra_images', []))
        ])
