from Server.authentication.models import CustomUser
from Server.utils.DynamicFieldsSerializer import DynamicFieldsModelSerializer


class CustomUserSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"