from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import SignUpSerializer, LoginSerializer
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class SignUpView(APIView):
    @swagger_auto_schema(
        operation_description="새로운 사용자를 등록합니다.",
        request_body=SignUpSerializer,
        responses={
            201: openapi.Response(
                description="회원가입 성공",
                schema=SignUpSerializer,
                examples={
                    "application/json": {
                        "username": "testuser",
                        "nickname": "TestUser"
                    }
                }
            ),
            400: openapi.Response(
                description="잘못된 요청",
                examples={
                    "application/json": {
                        "error": {
                            "code": "USER_ALREADY_EXISTS",
                            "message": "이미 가입된 사용자입니다."
                        }
                    }
                }
            )
        },
        tags=['사용자 관리']
    )
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({
                    'username': user.username,
                    'nickname': user.nickname
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({
                    'error': {
                        'code': 'USER_ALREADY_EXISTS',
                        'message': '이미 가입된 사용자입니다.'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
        # error 키가 있으면 그대로, 아니면 일반 에러로 반환
        errors = serializer.errors
        if 'error' in errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="사용자 로그인을 수행합니다.",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="로그인 성공",
                examples={
                    "application/json": {
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    }
                }
            ),
            400: openapi.Response(
                description="잘못된 요청",
                examples={
                    "application/json": {
                        "error": {
                            "code": "INVALID_CREDENTIALS",
                            "message": "아이디 또는 비밀번호가 올바르지 않습니다."
                        }
                    }
                }
            )
        },
        tags=['사용자 관리']
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': {
                        'code': 'INVALID_CREDENTIALS',
                        'message': '아이디 또는 비밀번호가 올바르지 않습니다.'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="사용자 로그아웃을 수행합니다. 현재 사용자의 access token과 refresh token을 무효화합니다.",
        manual_parameters=[
            openapi.Parameter(
                'X-Refresh-Token',
                openapi.IN_HEADER,
                description="무효화할 refresh token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="로그아웃 성공",
                examples={
                    "application/json": {
                        "message": "로그아웃되었습니다."
                    }
                }
            ),
            401: openapi.Response(
                description="인증되지 않은 요청",
                examples={
                    "application/json": {
                        "detail": "인증 자격이 제공되지 않았습니다."
                    }
                }
            ),
            400: openapi.Response(
                description="잘못된 요청",
                examples={
                    "application/json": {
                        "error": {
                            "code": "LOGOUT_FAILED",
                            "message": "로그아웃 처리 중 오류가 발생했습니다."
                        }
                    }
                }
            )
        },
        tags=['사용자 관리']
    )
    def post(self, request):
        try:
            # 헤더에서 refresh token 가져오기
            refresh_token = request.headers.get('X-Refresh-Token')
            if not refresh_token:
                return Response({
                    'error': {
                        'code': 'REFRESH_TOKEN_REQUIRED',
                        'message': 'Refresh token이 필요합니다.'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            # refresh token 블랙리스트에 추가
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                'message': '로그아웃되었습니다.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': {
                    'code': 'LOGOUT_FAILED',
                    'message': '로그아웃 처리 중 오류가 발생했습니다.'
                }
            }, status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description="Refresh Token을 사용하여 새로운 Access Token을 발급받습니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh_token'],
            properties={
                'refresh_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Refresh Token"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="토큰 갱신 성공",
                examples={
                    "application/json": {
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    }
                }
            ),
            401: openapi.Response(
                description="유효하지 않은 Refresh Token",
                examples={
                    "application/json": {
                        "detail": "Token is invalid or expired",
                        "code": "token_not_valid"
                    }
                }
            )
        },
        tags=['사용자 관리']
    )
    def post(self, request, *args, **kwargs):
        # refresh_token 키를 refresh로 변경
        if 'refresh_token' in request.data:
            request.data['refresh'] = request.data.pop('refresh_token')
        response = super().post(request, *args, **kwargs)
        # 응답의 access 키를 access_token으로 변경
        if 'access' in response.data:
            response.data['access_token'] = response.data.pop('access')
        return response
