"""
email_sender.py
Gmail SMTP를 통해 HTML 형식의 투자 리포트 이메일을 발송한다.
"""

import os
import smtplib
from datetime import datetime, timezone, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown


KST = timezone(timedelta(hours=9))


def _md_to_html(md_text: str) -> str:
    """마크다운 → HTML 변환"""
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code"],
    )


def _build_email_body(analyses: list[dict], date_str: str) -> str:
    """분석 결과 리스트를 HTML 이메일 본문으로 조합"""
    sections_html = ""
    for item in analyses:
        label = item.get("label", "종목 분석")
        content_html = _md_to_html(item.get("content", ""))
        sections_html += f"""
        <div style="margin-bottom:32px;padding:24px;background:#f9f9f7;border-radius:12px;border:1px solid #e5e3db;">
          <h2 style="margin:0 0 16px;font-size:18px;color:#1a1a18;">{label}</h2>
          <div style="font-size:14px;line-height:1.7;color:#3d3d3a;">
            {content_html}
          </div>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#f0ede6;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <div style="max-width:680px;margin:0 auto;padding:32px 16px;">

    <!-- Header -->
    <div style="background:#1a1a18;border-radius:12px;padding:24px 28px;margin-bottom:24px;">
      <p style="margin:0 0 4px;font-size:12px;color:#888780;letter-spacing:.08em;">DAILY INVESTMENT REPORT</p>
      <h1 style="margin:0;font-size:22px;font-weight:500;color:#f1efe8;">{date_str} 투자 분석 리포트</h1>
    </div>

    <!-- Analyses -->
    {sections_html}

    <!-- Footer -->
    <div style="padding:20px 0;text-align:center;font-size:12px;color:#888780;border-top:1px solid #d3d1c7;">
      ⚠️ 본 리포트는 교육·참고 목적이며 투자 권유가 아닙니다.<br>
      최종 투자 결정은 반드시 본인의 판단과 책임 하에 이루어져야 합니다.
    </div>
  </div>
</body>
</html>
"""


def send_report(analyses: list[dict]) -> None:
    """이메일 발송"""
    now_kst = datetime.now(KST)
    date_str = now_kst.strftime("%Y년 %m월 %d일")

    sender   = os.environ["GMAIL_ADDRESS"]
    password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📈 {date_str} 투자 분석 리포트"
    msg["From"]    = sender
    msg["To"]      = recipient

    html_body = _build_email_body(analyses, date_str)
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"✅ 이메일 발송 완료 → {recipient}")
