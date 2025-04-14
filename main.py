from fastapi import FastAPI, HTTPException
from openai import AzureOpenAI
import os
import re
from dotenv import load_dotenv
load_dotenv()  # ✅ 이게 있어야 .env에서 불러옴


# Azure 환경변수 읽기
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")

# FastAPI 앱 생성
app = FastAPI()

# 시대별 위인 목록
era_figure_dict = {
    "조선 전기": ["세종대왕", "이순신"],
    "조선 후기": ["정약용", "흥선대원군"],
    "일제강점기": ["안중근", "김구"]
}

# 마크다운 볼드 -> HTML
def markdown_to_html(text):
    html = re.sub(r'\*\*(.+?)\*\*', r"<strong style='color:#d14;'>\1</strong>", text)
    html = html.replace("\n", "<br>")
    return html

# API 엔드포인트
@app.get("/today-hero")
def get_today_hero(era: str, figure: str):
    if era not in era_figure_dict or figure not in era_figure_dict[era]:
        raise HTTPException(status_code=400, detail="시대 또는 인물 정보가 유효하지 않습니다.")

    prompt = (
        f"{era} 시대의 {figure}를 오늘의 위인으로 소개해 주세요.\n"
        "그 인물이 1인칭 시점으로 **자연스럽고 구어체 말투**로 업적에 대해 스토리텔링 해주세요.\n"
        "말투는 근엄하지만 딱딱하지 않게, 예: '~했지', '~이끌었단다', '~고민했었어' 등.\n"
        "업적 위주로 간결하게 설명하되, 주요 업적에는 **볼드처리**하여 강조해주세요.\n"
        "형식:\n[이름]: [스토리텔링]"
    )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=1000,
    )

    raw = response.choices[0].message.content.strip()
    html = markdown_to_html(raw)
    return {
        "preview": html[:300] + "..." if len(html) > 300 else html,
        "full": html
    }
