from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import asyncio
from playwright.async_api import async_playwright

app = FastAPI(title="LLM Quiz Solver", version="1.0")

SECRET_KEY = "IITMDS@25T3_QZ"  # 🔒 Do not change


class QuizRequest(BaseModel):
    secret: str
    question: str = None
    filetype: str = None
    filename: str = None


# --- Helper function to simulate parsing ---
async def fetch_quiz(question_text: str = None):
    """Simulates fetching/solving a quiz via Playwright browser"""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.set_content("""
                <html><body>
                <div id="result">Parsed basic HTML quiz. (Demo mode)</div>
                </body></html>
            """)
            await page.wait_for_selector("#result", timeout=5000)
            result = await page.inner_html("#result")
            await browser.close()
            return result
    except Exception as e:
        return f"Error during browser execution: {str(e)}"


@app.post("/quiz")
async def solve_quiz(
    secret: str = Form(...),
    question: str = Form(None),
    file: UploadFile = None
):
    # --- Secret validation ---
    if secret.strip() != SECRET_KEY:
        return JSONResponse(
            content={
                "status": "error",
                "email": "23f3002817@ds.study.iitm.ac.in",
                "reason": "Invalid secret key",
            },
            status_code=401,
        )

    try:
        # --- Demo logic for evaluation ---
        result = await fetch_quiz(question)
        response = {
            "status": "ok",
            "email": "23f3002817@ds.study.iitm.ac.in",
            "answer": result or "No answer generated",
        }
        return JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "email": "23f3002817@ds.study.iitm.ac.in",
                "reason": str(e),
            },
            status_code=500,
        )
