from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from typing import List  # 1. List 임포트 추가

app = FastAPI()
templates = Jinja2Templates(directory='templates')

symptom_mapping = {
    "복통": "소화기내과",
    "흉통": "심장내과",
    "두통": "신경과",
    "기침": "호흡기내과",
    "어지러움": "신경과",
    "발열": "가정의학과",
}

FALLBACK_DEPARTMENT = 'AI 봇과 증상 관련 추가 대화 추천'

# 진료과 설명 (결과 화면 표시용)
department_info = {
    "소화기내과": {
        "icon": "🫃",
        "desc": "위, 식도, 장, 간, 담낭, 췌장 등 소화기관의 질환을 진단하고 치료합니다.",
        "treats": "위염·역류성 식도염, 위·대장 질환, 간 질환, 복통·소화불량",
    },
    "심장내과": {
        "icon": "🫀",
        "desc": "심장과 혈관에 생기는 질환을 진단하고 치료합니다. 가슴 통증이 반복되거나 숨이 차면 진료가 필요합니다.",
        "treats": "협심증·심근경색, 부정맥, 고혈압, 심부전",
    },
    "신경과": {
        "icon": "🧠",
        "desc": "뇌, 척수, 말초신경 등 신경계 질환을 진단하고 치료합니다.",
        "treats": "두통·편두통, 어지럼증, 뇌졸중, 치매, 말초신경병증",
    },
    "호흡기내과": {
        "icon": "🫁",
        "desc": "폐와 기관지 등 호흡기 질환을 진단하고 치료합니다. 기침이 오래 지속될 때 방문하세요.",
        "treats": "기관지염·폐렴, 천식, 만성 폐쇄성 폐질환, 지속되는 기침",
    },
    "가정의학과": {
        "icon": "🩺",
        "desc": "특정 장기에 국한되지 않고 전신 증상을 종합적으로 살펴, 필요 시 적합한 전문과로 연결해 드립니다.",
        "treats": "발열, 피로감, 감기, 만성질환 관리, 건강검진 상담",
    },
    FALLBACK_DEPARTMENT: {
        "icon": "💬",
        "desc": "선택하신 증상 중 일부는 아직 진료과가 정해져 있지 않아요. AI 봇과 증상을 더 자세히 이야기해 보시길 권해드려요.",
        "treats": "증상의 위치·기간·정도를 구체적으로 설명하면 더 정확한 안내를 받을 수 있어요",
    },
}

@app.get("/symptom")
def symptom(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='symptom.html'
    ) 

# 2. @app.post와 List[str] = Form(...) 적용, 변수명 일치시키기
@app.post("/result")
def result(request: Request, symptoms: List[str] = Form(...)):
    recommended_departments = set()

    for s in symptoms:
        if s in symptom_mapping:
            recommended_departments.add(symptom_mapping[s])
        else: 
            recommended_departments.add(FALLBACK_DEPARTMENT)

    # 실제 진료과 먼저, 안내 항목(AI 봇)은 마지막에 표시
    ordered = sorted(recommended_departments, key=lambda d: (d == FALLBACK_DEPARTMENT, d))
    departments = [{"name": d, **department_info[d]} for d in ordered]

    return templates.TemplateResponse(
        request=request,
        name='result.html',
        context={"departments": departments, "symptoms": symptoms}
    )