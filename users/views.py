from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import User
from .forms import *
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from django.contrib.auth import login
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema

# Views que não são da API não precisam de anotações do Swagger

def home_view(request):
    return render(request, 'home.html')

def register_email_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('registration_success')
    else:
        form = RegistrationForm()
    return render(request, 'users/register_email.html', {'form': form})

def register_token_view(request):
    if request.method == 'POST':
        form = TokenRegistrationForm(request.POST)
        if form.is_valid():
            user, token = User.objects.create_user_with_token()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return render(request, 'users/token_display.html', {'token': token})
    else:
        form = TokenRegistrationForm()
    return render(request, 'users/register_token.html', {'form': form})

def registration_success_view(request):
    return render(request, 'users/registration_success.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "E-mail ou senha incorretos.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def token_and_password_login_view(request):
    form = TokenAndPasswordLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        token = form.cleaned_data.get('token')
        password = form.cleaned_data.get('password')
        try:
            user = User.objects.get(access_token=token)
            if user.check_password(password):
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Senha incorreta.")
        except User.DoesNotExist:
            form.add_error(None, "Token inválido.")
        except ValidationError:
            form.add_error('token', "Formato de token inválido.")
    return render(request, 'users/token_and_password_login.html', {'form': form})

############################# API #############################

@extend_schema(request=UserRegistrationSerializer, responses={201: UserRegistrationSerializer})
class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=TokenRegistrationSerializer, responses={201: TokenRegistrationSerializer})
class TokenRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    @extend_schema(request=LoginSerializer, responses={200: 'Login realizado com sucesso'})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            token = serializer.validated_data.get('token')
            user = None

            if email:
                user = authenticate(username=email, password=serializer.validated_data.get('password'))
            elif token:
                user = User.objects.get(access_token=token)

            if user:
                login(request, user)
                return Response({'message': 'Login realizado com sucesso'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Login falhou'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(responses={200: ReferralLinkSerializer})
class ReferralLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        referral_link = f"{request.scheme}://{request.get_host()}/register?referral={user.id}"
        return Response({"referral_link": referral_link})

class ReferralLinkView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: ReferralLinkSerializer})
    def get(self, request, format=None):
        user = request.user
        referral_link = f"{request.scheme}://{request.get_host()}/register?referral={user.id}"
        serializer = ReferralLinkSerializer(data={'referral_link': referral_link})
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
