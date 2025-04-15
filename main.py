from fastapi import FastAPI
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")

@app.get("/random-hero")
def get_random_hero():
    prompt = (
        "한국사에 등장하는 위인 중에서 무작위로 한 명을 선정해서 소개해줘.\n"
        "가능하면 이전에 자주 등장하지 않았던 인물로 해주세요.\n"
        "다음 형식으로 작성해줘:\n\n"
        "[이름](출생연도~사망연도)\n"
        "핵심업적: [대표 업적 한 줄]"
    )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.2,
        max_tokens=200
    )

    content = response.choices[0].message.content.strip()
    return {"result": content}
