from rest_framework.serializers import ModelSerializer
from backend.models import User


class CreateUserSerialyzer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'type', 'first_name', 'last_name', 'father_name', 'company', 'position', 'auth_token']
        read_only_fields = ['auth_token', 'id']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'type', 'first_name', 'last_name', 'father_name', 'company', 'position', 'token']
        read_only_fields = ['id', 'token']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
