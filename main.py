from fastapi import FastAPI
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# .env 로드
load_dotenv()

app = FastAPI()

# Azure OpenAI 설정
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")

@app.get("/today-hero")
def get_today_hero():
    prompt = (
        "한국사에 등장하는 위인 중 한 명을 무작위로 선택해 주세요.\n"
        "가능하면 이전에 자주 등장하지 않았던 인물로 해주세요.\n"
        "그 인물의 이름과 시대, 대표 업적을 한 문단 이내로 소개하고,\n"
        "그 인물이 한 말 중 명언을 적어주세요.\n\n"
        "형식:\n"
        "[이름]([시대])\n"
        "[업적 설명]\n"
        "[명언]"
    )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=300,
    )

    return {"hero": response.choices[0].message.content.strip()}
