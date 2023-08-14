from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import User, Employee


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'is_verified']
        read_only_fields = ['id', 'is_verified']


class EmployeeSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'phone_number', 'nationality', 'gender', 'bio', 'website']

    def update(self, instance, validated_data):
        print(validated_data)
        user = validated_data.pop('user')
        user_serializer = UserSerializer(instance.user, data=user)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return super(EmployeeSerializer, self).update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
