import requests

API_URL = "http://127.0.0.1:8000/quiz"

data = {
    "secret": "IITMDS@25T3_QZ",
    "question": "Sample: Identify this quiz type (demo run)."
}

try:
    response = requests.post(API_URL, data=data)
    result = response.json()
except Exception as e:
    result = {"error": str(e)}

print({
    "status": "ok",
    "email": "23f3002817@ds.study.iitm.ac.in",
    "answer": result
})


