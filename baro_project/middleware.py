from django.utils.deprecation import MiddlewareMixin

class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # localhost나 127.0.0.1인 경우에만 COOP 헤더 설정
        host = request.get_host().split(':')[0]  # 포트 번호 제거
        if host in ['localhost', '127.0.0.1']:
            response['Cross-Origin-Opener-Policy'] = 'same-origin'
        return response 