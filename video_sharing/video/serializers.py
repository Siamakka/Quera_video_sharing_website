from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class PasswordConfirmationMixin:
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Password fields did not match.'})
        
        return data  

class SignUpSerializer(PasswordConfirmationMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password2',
            'email',
            'first_name',
            'last_name',
            )
        extra_kwargs = {
            'first_name': {
                'required': True,
            },
            'last_name': {
                'required': True,
            },
        }
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password]
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        )
        
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
        )

    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    

class ChangePasswordSerializer(PasswordConfirmationMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'old_password',
            'password',
            'password2',
        )
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password]
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        )
    
    old_password = serializers.CharField(
        write_only=True,
        required=True,
    )
    
    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'old_password': 'Old password is incorrect.'})
        return value
    
    def validate(self, data):
        data = super().validate(data)
        
        if data['old_password'] == data['password']:
            raise serializers.ValidationError({'password': 'Password should not be the same with old password.'})
        return data
    

    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    