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

## 배포 환경 (시험용)

### API 테스트 접근
- API 서버: `https://54.180.127.203/api/`
- API 문서 (Swagger): `https://54.180.127.203/swagger/`
- API 문서 (ReDoc): `https://54.180.127.203/redoc/`

### API 테스트 방법

#### 1. Swagger UI 사용
- 제공받은 API 서버 주소에 `/swagger/`를 붙여 접속
  예: `https://[서버주소]/swagger/`
- API 문서화 및 테스트를 위한 인터페이스 제공
- 각 API의 요청/응답 형식, 파라미터 등을 확인 가능

#### 2. 인증이 필요한 API 테스트 방법
1. 로그인 API 호출
   ```json
   {
       "username": "your_username",
       "password": "your_password"
   }
   ```
   - 응답으로 `access_token`과 `refresh_token` 발급

2. Swagger UI에서 인증 설정
   - 상단의 "Authorize" 버튼 클릭
   - `Bearer your_access_token_here` 형식으로 입력
   - Authorize 버튼 클릭

3. API 테스트
   - 인증이 필요한 API는 자동으로 Authorization 헤더에 토큰이 포함됨
   - 로그아웃 API의 경우 추가로 `X-Refresh-Token` 헤더 필요

### 주의사항
1. 토큰 관리
   - Access Token: 1일(24시간) 유효
   - Refresh Token: 7일 유효
   - 로그아웃 시 두 토큰 모두 무효화

2. API 요청 시 헤더
   - 인증이 필요한 API: `Authorization: Bearer <access_token>`
   - 로그아웃 API: 추가로 `X-Refresh-Token: <refresh_token>` 헤더 필요

3. 보안
   - 시험용 서버이므로 실제 프로덕션 환경과 보안 설정이 다를 수 있음
   - 민감한 정보는 포함하지 않도록 주의
   - 시험 종료 후 서버 접근 정보는 무효화됨

## 라이선스

BSD License 