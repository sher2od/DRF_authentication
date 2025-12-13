import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .serilizers import RegisterSerialzer, VerifyEmailSerializer, LoginSeralizer

from .utils import generate_code,send_verification_email

from rest_framework.authtoken.models import Token

User = get_user_model()

# Register + emailga kod yuborish
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerialzer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 4 xonali kod yaratish
        code = str(random.randint(1000, 9999))
        user.verification_code = code  # agar user modelga qo‘shilgan bo‘lsa
        user.save()

        # Email yuborish
        send_mail(
            'Tasdiqlash kodi',
            f'Sizning 4 xonali kodingiz: {code}',
            'your_email@gmail.com',
            [user.email],
            fail_silently=False
        )

        return Response({"msg": "Ro‘yxatdan o‘tildi. Emailga kod yuborildi."}, status=201)

# Verify email
class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User topilmadi"}, status=404)

        if user.verification_code != code:
            return Response({"error": "Kod noto‘g‘ri"}, status=400)

        user.is_active = True
        user.verification_code = None
        user.save()

        return Response({"msg": "Email tasdiqlandi"}, status=200)



# Login
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSeralizer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            return Response({"error": "Email yoki password noto‘g‘ri"}, status=400)

        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if not user:
            return Response({"error": "Email yoki password noto‘g‘ri"}, status=400)

        if not user.is_active:
            return Response({"error": "Email tasdiqlanmagan"}, status=400)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)




