from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude =  ['password','groups','user_permissions','is_staff','is_superuser','last_login']


class RegisterSerialzer(serializers.ModelSerializer):
    confirm = serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = ['username','password','confirm','email','email','first_name','last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm']:
            raise serializers.ValidationError('password asn confirm mos emas')
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('confirm')
        password = validated_data['password']

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
    

class LoginSeralizer(serializers.Serializer):
    username = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=250)



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password','role','groups','user_permissions','is_staff','is_superuser']
        extra_kwargs = {
            'username':{
                'required':False
            }
        }


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)
    confirm = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm']:
            raise serializers.ValidationError('password asn confirm mos emas')
        return super().validate(attrs)
    




    