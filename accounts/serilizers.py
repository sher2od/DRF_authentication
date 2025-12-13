from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerialzer(serializers.ModelSerializer):
    confirm = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm']:
            raise serializers.ValidationError('password va confirm mos emas')
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Bu email allaqachon ro‘yxatdan o‘tgan')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm')
        password = validated_data.pop('password')
        validated_data['username'] = validated_data['email'].split('@')[0]
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

class LoginSeralizer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)




    