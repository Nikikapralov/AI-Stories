from django.contrib.auth import get_user_model
from django.db import models

from Server.authentication.models import CustomUser

custom_user_model = get_user_model()


class UserAccount(models.Model):
    """
    User model with data for the corresponding user.
    """
    user_owner = models.OneToOneField(custom_user_model, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    image_url = models.URLField(max_length=255, null=True)

    def __str__(self) -> str:
        """
        Str magic method.
        @return: Returns an interpolated string of the whole User name.
        """
        return f"{self.nickname}"


class Story(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    image_url = models.URLField(max_length=255, null=True)
    user_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Comment(models.Model):
    story_fk = models.ForeignKey(Story, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    user_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)