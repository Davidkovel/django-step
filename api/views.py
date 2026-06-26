from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer, ProfileUpdateSerializer

COOKIE_NAME = getattr(settings, 'JWT_REFRESH_COOKIE_NAME', 'refresh_token')
COOKIE_PATH = getattr(settings, 'JWT_REFRESH_COOKIE_PATH', '/api/')


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    """Кладём refresh-токен в httpOnly cookie — JS его не видит."""
    response.set_cookie(
        key=COOKIE_NAME,
        value=refresh_token,
        max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
        httponly=True,
        samesite='Lax',
        secure=not settings.DEBUG,  # HTTPS в prod, HTTP в dev
        path=COOKIE_PATH,
    )


def _delete_refresh_cookie(response: Response) -> None:
    response.delete_cookie(COOKIE_NAME, path=COOKIE_PATH)


class RegisterAPIView(APIView):
    """
    POST /api/auth/register/
    Body: { username, email, first_name, last_name, password, password2, phone? }
    Returns: { access } + httpOnly cookie(refresh)
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )
        _set_refresh_cookie(response, str(refresh))
        return response


class LoginAPIView(APIView):
    """
    POST /api/auth/login/
    Body: { username, password }
    Returns: { access, user } + httpOnly cookie(refresh)
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')

        if not username or not password:
            return Response(
                {'detail': 'Введіть логін та пароль.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # поддерживаем вход как по username, так и по email
        user = None
        try:
            u = User.objects.get(username=username)
            if u.check_password(password):
                user = u
        except User.DoesNotExist:
            try:
                u = User.objects.get(email=username)
                if u.check_password(password):
                    user = u
            except User.DoesNotExist:
                pass

        if user is None:
            return Response(
                {'detail': 'Невірний логін або пароль.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {'detail': 'Акаунт заблоковано.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)
        response = Response(
            {
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
            }
        )
        _set_refresh_cookie(response, str(refresh))
        return response


class RefreshAPIView(APIView):
    """
    POST /api/auth/refresh/
    Читает refresh из httpOnly cookie, возвращает новый access.
    Браузер отправляет cookie автоматически (credentials: 'include').
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(COOKIE_NAME)
        if not refresh_token:
            return Response(
                {'detail': 'Refresh-токен відсутній.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            response = Response({'access': new_access})
            # ROTATE_REFRESH_TOKENS=True → simplejwt уже выдал новый refresh
            _set_refresh_cookie(response, str(refresh))
            return response
        except TokenError as e:
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    """
    POST /api/auth/logout/
    Блэклистит refresh-токен и удаляет cookie.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(COOKIE_NAME)
        response = Response({'detail': 'Вийшли успішно.'})
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except (TokenError, InvalidToken):
                pass  # уже невалидный — просто удаляем cookie
        _delete_refresh_cookie(response)
        return response


class MeAPIView(APIView):
    """
    GET  /api/auth/me/   → данные текущего юзера
    PUT  /api/auth/me/   → обновить first_name, last_name, phone, city
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = ProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MySavedCarsAPIView(APIView):
    """GET /api/auth/saved/ → список сохранённых объявлений юзера"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from cars.models import SavedCar
        from cars.serializers import CarListSerializer
        saved = SavedCar.objects.filter(user=request.user).select_related(
            'car', 'car__seller'
        ).prefetch_related('car__photos').order_by('-saved_at')
        data = [
            {
                'saved_at': s.saved_at,
                'car': CarListSerializer(s.car).data,
            }
            for s in saved
        ]
        return Response(data)