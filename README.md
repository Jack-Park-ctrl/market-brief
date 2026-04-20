# 📈 Daily Stock Alert System

매일 오전 8시 KST, Claude AI가 투자 원칙 기반으로 종목을 분석하고 이메일로 발송합니다.
서버 없이 GitHub Actions만으로 동작합니다.

---

## 세팅 방법 (5단계)

### 1단계 — 이 저장소를 내 GitHub에 올리기

```bash
git init
git add .
git commit -m "init"
# GitHub에서 새 Repository 생성 후:
git remote add origin https://github.com/[내아이디]/stock-alert.git
git push -u origin main
```

### 2단계 — Gmail 앱 비밀번호 발급

1. Google 계정 → 보안 → 2단계 인증 활성화
2. **앱 비밀번호** 생성 (앱: 메일, 기기: 기타)
3. 생성된 16자리 비밀번호 복사

### 3단계 — Anthropic API 키 발급

1. https://console.anthropic.com 접속
2. API Keys → Create Key
3. 키 복사

### 4단계 — GitHub Secrets 등록

저장소 → Settings → Secrets and variables → Actions → New repository secret

| Secret 이름 | 값 |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic에서 발급한 API 키 |
| `GMAIL_ADDRESS` | 발신 Gmail 주소 (예: myemail@gmail.com) |
| `GMAIL_APP_PASSWORD` | 2단계에서 발급한 앱 비밀번호 |
| `RECIPIENT_EMAIL` | 리포트 받을 이메일 (본인 주소 권장) |

### 5단계 — watchlist.json 수정

원하는 종목으로 수정 후 커밋:
```json
{
  "style": "가치",          // 가치 / 성장 / 배당 / 균형
  "market": "KR",           // KR / US / 혼합
  "period": "장기",         // 단기 / 중기 / 장기
  "stocks": [
    { "name": "삼성전자", "ticker": "005930", "market": "KR" }
  ],
  "auto_pick": {
    "enabled": true,
    "count": 2,
    "theme": "AI 반도체 섹터 위주"
  }
}
```

---

## 수동 실행 방법

GitHub → Actions → Daily Stock Analysis → Run workflow

---

## 디렉토리 구조

```
stock-alert-system/
├── .github/workflows/daily-analysis.yml   # 스케줄러
├── src/
│   ├── main.py          # 진입점
│   ├── analyzer.py      # Claude API 호출
│   └── email_sender.py  # Gmail 발송
├── watchlist.json        # 모니터링 종목
├── requirements.txt
└── README.md
```

---

> ⚠️ 본 시스템의 분석 결과는 교육·참고 목적이며 투자 권유가 아닙니다.
