from rest_framework import serializers
from .models import User

class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=4)
    password = serializers.CharField(write_only=True, min_length=8)
    nickname = serializers.CharField(min_length=2)

    class Meta:
        model = User
        fields = ['username', 'password', 'nickname']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({
                'error': {
                    'code': 'USER_ALREADY_EXISTS',
                    'message': '이미 가입된 사용자입니다.'
                }
            })
        if User.objects.filter(nickname=data['nickname']).exists():
            raise serializers.ValidationError({
                'error': {
                    'code': 'USER_ALREADY_EXISTS',
                    'message': '이미 가입된 사용자입니다.'
                }
            })
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname']
        )
        return user 

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True) 