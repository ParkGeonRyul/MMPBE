Maven Members Portal Backend (MMPBE)

MMPBE는 Maven Members Portal의 백엔드 시스템으로, OAuth2 인증 기반의 사용자 관리, 작업 요청/계획서 API, 파일 업로드, 관리자 기능, API Gateway 등 다양한 기능을 제공합니다. 이 저장소는 FastAPI를 기반으로 하며, Docker 및 Azure DevOps와 통합된 CI/CD 환경을 갖추고 있습니다.

🚀 주요 기능

🛂 인증 (OAuth2.0 기반)

OAuth2.0 기반 로그인 및 인증 처리

로그인 시 회원 정보가 DB에 없으면 자동 등록

MSAL 라이브러리 사용으로 인증 최적화

Token 유효성 검사 및 쿠키 기반 접근 제어

🧑‍💻 사용자 관리

관리자 전용 고객 목록 조회

사용자 상세 정보 조회 (파일 포함)

role = user인 계정만 필터링

Access 권한에 따른 Proxy 경로 제어

📄 작업 요청 API

작업 요청 Create / Read / Update / Delete 지원

작업 요청 목록 및 상세조회 API

role 별 조회 조건 설정 (관리자 / 사용자)

status, title, category 등의 필드 구조 개선

🗂️ 작업 계획서 API

작업계획서 등록, 수정, 승인, 반려

파일 업로드/다운로드 지원 (multipart/form-data)

Acceptor/Requestor 컬럼 관리 및 role에 따른 접근 제한

관리자용 통계, 리스트 조회 성능 개선

📁 파일 서버 기능

파일 업로드/다운로드 기능 구현

FileServer 연동 및 Path 최적화

파일 사이즈/타입 검증, Null 체크 등 예외 처리 강화

🔐 API Gateway

multipart/form-data와 JSON 요청 구분 처리

env 환경변수 기반 동적 설정 지원

요청 시 검증 및 Redirect 기능 개선

⚙️ 시스템 관리

Category API 개발 및 role별 필터링 지원

Access 권한 기반 데이터 전송 제어

MongoDB Join 성능 최적화

DTO 구조 개선 및 일관된 Naming 적용

📦 프로젝트 구조 (예시)

MMPBE/
├── app/
│   ├── api/              # 라우팅 정의
│   ├── core/             # 설정 파일, 인증 처리
│   ├── models/           # DB 모델 (Pydantic, MongoDB)
│   ├── services/         # 비즈니스 로직 처리
│   └── utils/            # 유틸리티 모듈
├── tests/                # 테스트 코드
├── Dockerfile            # Docker 설정
├── docker-compose.yml    # 로컬 개발용 컴포즈
├── azure-pipelines.yml   # Azure CI/CD 설정
└── README.md             # 현재 문서

⚒️ 기술 스택

Backend: Python FastAPI

Database: MongoDB

Auth: OAuth2.0 + MSAL

CI/CD: Azure Pipelines

DevOps: Docker, Docker Compose

📅 주요 히스토리 요약

2024년 7월 ~ 9월

OAuth2.0 인증 도입 및 사용자 인증 구조 전환

작업 요청 및 계획서 API CRUD 기능 전체 구현

파일 업로드 및 파일 서버 기능 완성

관리자/사용자 역할 기반 접근 권한 제어 도입

API Gateway 및 Proxy 구성

MongoDB Join 및 DTO 리팩토링

Docker 환경 구성 및 Azure DevOps 배포 자동화 설정

🧑‍🤝‍🧑 주요 기여자

이름

역할

Lucas Lee

프로젝트 리드, 기능 설계, OAuth 인증, 파일 서버, 테스트 코드, 구조 설계

Wade Park

기능 설계, 작업 요청/계획서 개발, DevOps 구성

Nova Lee

작업 계획서 구현

📝 향후 개선 예정

Swagger 자동 문서화 연동

관리자용 통계 기능 추가

테넌시 기반 DB 분리 구조 적용

리팩토링 완료 후 버전 태깅 (v1.0.0)

