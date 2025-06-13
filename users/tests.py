from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user_data():
    return {
        'username': 'testuser',
        'password': 'testpass123',
        'nickname': 'TestUser'
    }

@pytest.fixture
def existing_user(test_user_data):
    user = User.objects.create_user(
        username=test_user_data['username'],
        password=test_user_data['password'],
        nickname=test_user_data['nickname']
    )
    return user

class TestSignUp:
    @pytest.mark.django_db
    def test_signup_success(self, api_client, test_user_data):
        """회원가입 성공 테스트"""
        url = reverse('signup')
        response = api_client.post(url, test_user_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == test_user_data['username']
        assert response.data['nickname'] == test_user_data['nickname']
        assert 'password' not in response.data
        
        # DB에 사용자가 생성되었는지 확인
        assert User.objects.filter(username=test_user_data['username']).exists()

    @pytest.mark.django_db
    def test_signup_duplicate_username(self, api_client, test_user_data, existing_user):
        """중복된 사용자명으로 회원가입 시도 테스트"""
        url = reverse('signup')
        response = api_client.post(url, test_user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error']['code'] == 'USER_ALREADY_EXISTS'
        assert response.data['error']['message'] == '이미 가입된 사용자입니다.'

    @pytest.mark.django_db
    def test_signup_invalid_data(self, api_client):
        """잘못된 데이터로 회원가입 시도 테스트"""
        url = reverse('signup')
        invalid_data = {
            'username': 't',     # 너무 짧은 사용자명 (길이 1)
            'password': '123',   # 너무 짧은 비밀번호
            'nickname': ''       # 빈 닉네임
        }
        response = api_client.post(url, invalid_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data
        assert 'password' in response.data
        assert 'nickname' in response.data

class TestLogin:
    @pytest.mark.django_db
    def test_login_success(self, api_client, existing_user, test_user_data):
        """로그인 성공 테스트"""
        url = reverse('login')
        login_data = {
            'username': test_user_data['username'],
            'password': test_user_data['password']
        }
        response = api_client.post(url, login_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert isinstance(response.data['token'], str)

    @pytest.mark.django_db
    def test_login_wrong_password(self, api_client, existing_user, test_user_data):
        """잘못된 비밀번호로 로그인 시도 테스트"""
        url = reverse('login')
        login_data = {
            'username': test_user_data['username'],
            'password': 'wrongpassword'
        }
        response = api_client.post(url, login_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error']['code'] == 'INVALID_CREDENTIALS'
        assert response.data['error']['message'] == '아이디 또는 비밀번호가 올바르지 않습니다.'

    @pytest.mark.django_db
    def test_login_nonexistent_user(self, api_client):
        """존재하지 않는 사용자로 로그인 시도 테스트"""
        url = reverse('login')
        login_data = {
            'username': 'nonexistent',
            'password': 'password123'
        }
        response = api_client.post(url, login_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error']['code'] == 'INVALID_CREDENTIALS'
        assert response.data['error']['message'] == '아이디 또는 비밀번호가 올바르지 않습니다.'

    @pytest.mark.django_db
    def test_login_invalid_data(self, api_client):
        """잘못된 형식의 데이터로 로그인 시도 테스트"""
        url = reverse('login')
        invalid_data = {
            'username': '',  # 빈 사용자명
            'password': ''   # 빈 비밀번호
        }
        response = api_client.post(url, invalid_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data
        assert 'password' in response.data
