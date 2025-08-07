# 🚀 Maven Members Portal Backend (MMPBE)

**MMPBE**는 *Maven Members Portal*의 백엔드 시스템으로, 사용자 인증, 작업 요청/계획서 API, 파일 서버, 관리자 기능 등 다양한 기능을 제공합니다.  
FastAPI 기반으로 개발되었으며, Docker 및 Azure DevOps 기반의 CI/CD 환경이 구축되어 있습니다.

---

## 🧩 Features

### 🛂 인증 (OAuth2.0 기반)
- OAuth2.0 + MSAL 기반 로그인 및 인증 처리
- 최초 로그인 시 사용자 정보 자동 등록
- 쿠키 기반 접근 제어 및 Token 유효성 검사

### 👥 사용자 관리
- 관리자 전용 고객 목록 및 상세 조회 (파일 포함)
- `role = user` 필터링 지원
- Proxy 접근 경로 권한 제어

### 📌 작업 요청 API
- CRUD 지원: 작업 요청 생성, 조회, 수정, 삭제
- 관리자/사용자 별 조회 조건 설정
- `status`, `title`, `category` 필드 구조 개선

### 🗂 작업 계획서 API
- 계획서 등록, 수정, 승인, 반려 기능
- 파일 업로드/다운로드 (multipart/form-data)
- 역할 기반 컬럼 접근 제한 (Acceptor / Requestor)
- 관리자 통계 및 리스트 조회 성능 개선

### 📁 파일 서버
- 파일 업/다운로드 처리
- FileServer 연동 및 경로 최적화
- 사이즈/타입 검증 및 예외 처리 강화

### 🔐 API Gateway
- JSON vs multipart/form-data 요청 구분 처리
- `env` 환경변수 기반 동적 설정
- 요청 검증 및 Redirect 기능

### ⚙️ 시스템 관리
- Category API 및 역할 기반 필터링
- Access 권한별 데이터 전송 제어
- MongoDB Join 최적화 및 DTO 리팩토링

---

## 🏗 프로젝트 구조

```
MMPBE/
├── app/
│   ├── api/              # 라우팅 정의
│   ├── core/             # 설정 파일, 인증 모듈
│   ├── models/           # Pydantic + MongoDB 모델
│   ├── services/         # 비즈니스 로직
│   └── utils/            # 공통 유틸리티
├── tests/                # 테스트 코드
├── Dockerfile            # Docker 설정
├── docker-compose.yml    # 로컬 개발용
├── azure-pipelines.yml   # Azure DevOps CI/CD
└── README.md             # 프로젝트 설명서
```

---

## ⚒ 기술 스택

| 항목       | 기술 |
|------------|------|
| Backend    | Python (FastAPI) |
| Database   | MongoDB |
| 인증       | OAuth2.0 + MSAL |
| CI/CD      | Azure Pipelines |
| DevOps     | Docker, Docker Compose |

---

## 📅 프로젝트 히스토리 (2024년 7월 ~ 9월)

- OAuth2 인증 도입 및 사용자 인증 구조 전환
- 작업 요청 / 계획서 API 전체 구현
- 파일 서버 및 업로드 기능 완성
- 역할 기반 접근 권한 설정
- API Gateway 및 Proxy 경로 설계
- MongoDB Join 최적화 및 DTO 구조 통일
- Docker + Azure DevOps 연동 CI/CD 파이프라인 구축

---

## 👨‍💻 주요 기여자

| 이름              | 역할 |
|-------------------|------|
| **Lucas Lee (이환주)** | 프로젝트 리드, 초기 프론트엔드 서버 구축, 초기 백엔드 서버 구축, 초기 DB서버 구축, Azure 기반 DevOps 구축, Azure DevOps Pipeline 기반 DockerFile, Docker Compose 구축, 인증 및 구조 설계|
| **Wade Park (박건률)** | 초기 백엔드 서버 구축, DTO 설정 등 DB 작업, 백엔드 AzureDevOps Pipelines 설계, 작업 요청/계획서 개발, API Gateway 등 프록시 관련 개발, 파일 서버 구축, 테스트 코드 작성|
| **Nova Lee (이은빈)** | 작업 계획서 기능 구현 |

---

## 🔭 향후 계획

- Swagger 문서 자동화 연동
- 관리자용 통계 기능 추가
- 테넌시 기반 DB 분리 구조 도입
- 버전 태깅 (v1.0.0) 및 정식 릴리즈


