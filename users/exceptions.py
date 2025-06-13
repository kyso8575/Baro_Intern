from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response

class TokenExpired(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        'error': {
            'code': 'TOKEN_EXPIRED',
            'message': '토큰이 만료되었습니다.'
        }
    }
    default_code = 'token_expired'

class TokenNotFound(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        'error': {
            'code': 'TOKEN_NOT_FOUND',
            'message': '토큰이 없습니다.'
        }
    }
    default_code = 'token_not_found'

class InvalidToken(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        'error': {
            'code': 'INVALID_TOKEN',
            'message': '토큰이 유효하지 않습니다.'
        }
    }
    default_code = 'invalid_token'

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        if hasattr(exc, 'default_detail'):
            return Response(exc.default_detail, status=exc.status_code)
        
        return Response({
            'error': {
                'code': 'INVALID_TOKEN',
                'message': str(exc)
            }
        }, status=status.HTTP_401_UNAUTHORIZED)

    return response 