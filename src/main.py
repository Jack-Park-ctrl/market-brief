"""
main.py
GitHub Actions에서 실행되는 진입점.
watchlist.json을 읽고 → 분석 수행 → 이메일 발송
"""

import json
import time
import sys
from pathlib import Path

from analyzer import analyze_stock, run_auto_pick
from email_sender import send_report


def load_watchlist() -> dict:
    path = Path(__file__).parent.parent / "watchlist.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    print("📊 투자 분석 시작...")
    wl = load_watchlist()

    style  = wl.get("style", "균형")
    period = wl.get("period", "중기")
    stocks = wl.get("stocks", [])
    auto   = wl.get("auto_pick", {})

    analyses: list[dict] = []

    # 1) 관심 종목 개별 분석
    for stock in stocks:
        print(f"  → {stock['name']} ({stock['ticker']}) 분석 중...")
        try:
            content = analyze_stock(stock, style, period)
            time.sleep(30)
            analyses.append({
                "label":   f"{stock['name']} ({stock['ticker']})",
                "content": content,
            })
        except Exception as e:
            print(f"  ⚠️ {stock['name']} 분석 실패: {e}", file=sys.stderr)

    # 2) AI 자동 종목 선별 (활성화된 경우)
    if auto.get("enabled"):
        print(f"  → AI 자동 선별 ({auto['count']}종목) 분석 중...")
        try:
            content = run_auto_pick(
                theme=auto.get("theme", ""),
                count=auto.get("count", 2),
                style=style,
            )
            analyses.append({
                "label":   "🤖 AI 자동 선별 종목",
                "content": content,
            })
        except Exception as e:
            print(f"  ⚠️ 자동 선별 실패: {e}", file=sys.stderr)

    if not analyses:
        print("❌ 분석 결과 없음. 이메일 발송 건너뜀.")
        sys.exit(1)

    # 3) 이메일 발송
    print("📧 이메일 발송 중...")
    send_report(analyses)
    print("✅ 완료")


if __name__ == "__main__":
    main()
