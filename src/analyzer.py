"""
analyzer.py
Claude API를 호출하여 analyzing-investments 스킬 기반 종목 분석을 수행한다.
"""

import os
import json
import anthropic

SKILL_SYSTEM_PROMPT = """
당신은 analyzing-investments 스킬을 보유한 투자 분석 AI입니다.
성공한 투자자(버핏·린치·그레이엄·달리오·피셔)의 원칙을 적용해 종목을 분석하고,
매수 / 관망 / 매도회피 의견을 제시합니다.

분석 원칙별 수치 기준:
- 버핏: ROE ≥ 15%, 부채비율 < 50%, PER < 업종 평균 × 1.2
- 린치: PEG < 1.0, 재고 증가율 < 매출 증가율
- 그레이엄: 주가 ≤ 내재가치 × 0.67, 유동비율 ≥ 2.0
- 피셔: R&D 매출 대비 ≥ 3%(기술주), 영업이익률 3년 연속 상승
- 달리오: 현재 경제 사이클과 수혜 관계 명확

반드시 웹 검색으로 실시간 데이터를 수집한 후 분석하세요.
출력은 아래 마크다운 형식을 따르세요:

---
## [종목명] ([티커]) 분석

### 핵심 재무 지표 (수집 기준일: YYYY-MM-DD)
| 지표 | 현재값 | 업종 평균 | 판단 |
...

### 원칙별 통과 현황
| 원칙 | 기준 | 결과 | 근거 |
...

### 💡 투자 의견
**[매수적극 / 매수 / 관망 / 매도회피]**
> [수치 2개 이상 포함한 근거]

### 핵심 리스크
- 거시: ...
- 산업: ...
- 기업: ...

### 자기 평가 신뢰도: [상/중/하]
---

⚠️ 본 분석은 참고용이며 투자 권유가 아닙니다.
"""

def analyze_stock(stock: dict, style: str, period: str) -> str:
    """단일 종목 분석 수행 후 마크다운 문자열 반환"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = (
        f"다음 종목을 분석해주세요.\n"
        f"종목: {stock['name']} ({stock['ticker']}), 시장: {stock['market']}\n"
        f"투자 스타일: {style}, 기간: {period}\n\n"
        f"웹 검색으로 최신 재무 데이터를 수집하고 원칙 기반 분석을 수행하세요."
    )

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=SKILL_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
    )

    result_parts = [
        block.text
        for block in response.content
        if hasattr(block, "text")
    ]
    return "\n".join(result_parts)


def run_auto_pick(theme: str, count: int, style: str) -> str:
    """AI가 직접 종목을 선별하여 분석"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = (
        f"다음 조건으로 유망 종목 {count}개를 직접 선별하고 각각 분석해주세요.\n"
        f"선별 테마: {theme}\n"
        f"투자 스타일: {style}\n\n"
        f"웹 검색으로 최신 데이터를 수집하고, 선별 이유와 원칙 기반 분석을 함께 제공하세요."
    )

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        system=SKILL_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
    )

    result_parts = [
        block.text
        for block in response.content
        if hasattr(block, "text")
    ]
    return "\n".join(result_parts)
