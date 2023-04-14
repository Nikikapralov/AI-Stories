
class CustomUserSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"