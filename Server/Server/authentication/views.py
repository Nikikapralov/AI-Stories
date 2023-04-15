from django.shortcuts import render

# Create your views here.

# Create your views here.
from datetime import datetime

from django.contrib.auth import authenticate
from rest_auth.app_settings import LoginSerializer
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK
from rest_framework.views import APIView

from Server.ai_stories.models import UserAccount
from Server.authentication.models import CustomUser


class Register(ObtainAuthToken):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = CustomUser.objects.create_user(email=email, password=password)
        UserAccount.objects.create(user_owner=user)
        user = authenticate(request=request,
                            email=email, password=password)
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "is_superuser": user.is_superuser,
            },  status=HTTP_201_CREATED
        )


class Login(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
                                     context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.last_login = datetime.today()
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "is_superuser": user.is_superuser,
            }, status=HTTP_202_ACCEPTED)
        return Response(data={
            "message": "Account has been suspended.",
        }, status=HTTP_403_FORBIDDEN)


class Logout(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        token = Token.objects.get(user=self.request.user)
        token.delete()
        return Response(data=
            {
                "message": "Logged out successfully."
            },
            status=HTTP_200_OK
        )
