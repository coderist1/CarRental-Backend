from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Car
from .serializers import RegisterSerializer, UserSerializer, CarSerializer


def get_tokens_for_user(user):
    """Helper: generate JWT access and refresh tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# ─── Register ────────────────────────────────────────────────────────────────
class RegisterView(APIView):
    """
    POST /api/auth/register/
    Register a new user account.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'status': 'success',
                'message': 'Account created successfully.',
                'user': UserSerializer(user).data,
                'tokens': tokens,
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


# ─── Login ───────────────────────────────────────────────────────────────────
class LoginView(APIView):
    """
    POST /api/auth/login/
    Authenticate a user and return JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()

        if not username or not password:
            return Response({
                'status': 'error',
                'message': 'Username and password are required.',
            }, status=status.HTTP_400_BAD_REQUEST)

        # Fetch user manually to avoid leaking which field is wrong
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Invalid credentials.',
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({
                'status': 'error',
                'message': 'Invalid credentials.',
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({
                'status': 'error',
                'message': 'Account is disabled.',
            }, status=status.HTTP_403_FORBIDDEN)

        tokens = get_tokens_for_user(user)
        return Response({
            'status': 'success',
            'message': 'Login successful.',
            'user': UserSerializer(user).data,
            'tokens': tokens,
        }, status=status.HTTP_200_OK)


# ─── Profile ─────────────────────────────────────────────────────────────────
class ProfileView(APIView):
    """
    GET /api/auth/profile/
    Return the authenticated user's profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'status': 'success',
            'user': serializer.data,
        }, status=status.HTTP_200_OK)


# ─── Cars ────────────────────────────────────────────────────────────────────
class CarListView(generics.ListCreateAPIView):
    """
    GET  /api/cars/  — List all cars
    POST /api/cars/  — Add a new car (authenticated only)
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'count': queryset.count(),
            'cars': serializer.data,
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Car added successfully.',
                'car': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/cars/<id>/  — Retrieve a single car
    PUT    /api/cars/<id>/  — Update a car (full update)
    PATCH  /api/cars/<id>/  — Partial update a car
    DELETE /api/cars/<id>/  — Delete a car
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'car': serializer.data,
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Car updated successfully.',
                'car': serializer.data,
            })
        return Response({
            'status': 'error',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        plate = str(instance)
        instance.delete()
        return Response({
            'status': 'success',
            'message': f'{plate} has been deleted.',
        }, status=status.HTTP_200_OK)