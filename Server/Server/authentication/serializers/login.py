from django.contrib.auth import authenticate

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label="email", write_only=True)
    password = serializers.CharField(label="password", write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get("request"),
                                email=email, password=password)

            if not user:
                message = "Wrong email or password."
                raise serializers.ValidationError(message, code="authorization")

        else:
            message = 'Please enter email and password in order to login. One of the fields was empty.'
            raise serializers.ValidationError(message, code="authorization")

        attrs["user"] = user
        return attrs

