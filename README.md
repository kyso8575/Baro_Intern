# Baro Project

Django REST framework를 사용한 사용자 인증 API 프로젝트입니다.

## 주요 기능

- 회원가입
- 로그인/로그아웃
- JWT 토큰 기반 인증
- 토큰 갱신
- Swagger API 문서화

## 기술 스택

- Python 3.13
- Django 5.0.2
- Django REST framework
- JWT (JSON Web Token)
- SQLite (개발 환경)

## 설치 및 실행

1. 저장소 클론
```bash
git clone https://github.com/yourusername/baro-project.git
cd baro-project
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
.\venv\Scripts\activate  # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가:
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. 데이터베이스 마이그레이션
```bash
python manage.py migrate
```

6. 개발 서버 실행
```bash
python manage.py runserver
```

## API 엔드포인트

- 회원가입: `POST /api/users/signup/`
- 로그인: `POST /api/users/login/`
- 로그아웃: `POST /api/users/logout/`
- 토큰 갱신: `POST /api/users/token/refresh/`

## API 문서

- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## 테스트

```bash
pytest
```

## 라이선스

BSD License 