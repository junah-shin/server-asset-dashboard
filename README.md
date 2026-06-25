# Server Asset Management Dashboard

Streamlit + Supabase 기반 서버 자산 관리 대시보드.

## Features

- 전체 서버 수 KPI (정상/장애/점검)
- 설치위치(IDC/HQ)별 서버 분포 차트
- 운영등급(PRD/STG/DEV) 분포 차트
- 운영상태별 서버 분포 차트
- 서버 인벤토리 테이블 (필터링 지원)
- 서버 등록 기능
- Supabase Auth 기반 로그인/회원가입

---

## 1. Supabase 설정

### 1-1. 프로젝트 생성
1. [https://supabase.com](https://supabase.com) 접속 후 로그인
2. "New Project" 클릭
3. 프로젝트 이름/비밀번호 설정 후 생성

### 1-2. 테이블 생성
1. Supabase Dashboard -> **SQL Editor** 이동
2. `schema.sql` 파일 내용 전체 복사 & 붙여넣기
3. **Run** 클릭
4. `server_inventory` 테이블 + 샘플 데이터 20건이 생성됨

### 1-3. API 키 확인
1. Supabase Dashboard -> **Settings** -> **API**
2. `Project URL`과 `anon public` key 복사

---

## 2. 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일에 Supabase URL과 Key 입력

# 실행
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속.

---

## 3. Streamlit Cloud 배포

### 3-1. GitHub 연동
1. 이 프로젝트를 본인 GitHub 리포지토리에 push
2. `.env` 파일은 push하지 않음 (`.gitignore`에 포함)

### 3-2. Streamlit Cloud 배포
1. [https://share.streamlit.io](https://share.streamlit.io) 접속 후 GitHub 로그인
2. "New app" 클릭
3. 리포지토리, 브랜치, `app.py` 선택
4. **Advanced settings** -> Secrets에 아래 내용 입력:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key-here"
```

5. "Deploy" 클릭
6. 배포 완료 후 `https://your-app.streamlit.app` 으로 접속 가능

### 3-3. Secrets 적용 (Streamlit Cloud)
Streamlit Cloud에서는 `.env` 대신 Secrets를 사용합니다.
`utils/auth.py`에서 `os.getenv()`가 Streamlit Cloud의 Secrets도 자동으로 읽습니다 (`python-dotenv`와 호환).

만약 Secrets가 인식되지 않으면 `utils/auth.py`의 `get_supabase_client()`에서:
```python
url = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")
```
로 변경하면 됩니다.

---

## 4. 데이터 구조

| Column   | Type         | Constraint                |
|----------|--------------|---------------------------|
| location | VARCHAR(10)  | 'IDC' or 'HQ'            |
| env      | VARCHAR(10)  | 'PRD', 'STG', or 'DEV'   |
| hostname | VARCHAR(255) | NOT NULL                  |
| ip       | VARCHAR(45)  | NOT NULL                  |
| owner    | VARCHAR(100) | NOT NULL                  |
| status   | VARCHAR(10)  | '정상', '장애', or '점검' |

---

## Project Structure

```
server-asset-dashboard/
├── app.py                 # Main Streamlit app
├── schema.sql             # Supabase table schema + sample data
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── .streamlit/
│   └── config.toml        # Streamlit theme config
├── assets/
│   └── style.css          # Custom dark theme CSS
└── utils/
    ├── auth.py            # Supabase authentication
    ├── database.py        # Server inventory queries
    └── charts.py          # Plotly chart generators
```
