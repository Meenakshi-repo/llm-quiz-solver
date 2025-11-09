import asyncio
import json
import io
import base64
import pandas as pd
import requests
from playwright.async_api import async_playwright

# -----------------------
# Helper: download file (CSV/XLSX/PDF)
# -----------------------
def download_file(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        content_type = r.headers.get("content-type", "")
        if "csv" in content_type or url.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(r.content))
        elif "excel" in content_type or url.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(r.content))
        else:
            # fallback to raw text
            return r.text
        return df
    except Exception as e:
        return {"error": f"Download failed: {str(e)}"}

# -----------------------
# Core async quiz solver
# -----------------------
async def solve_quiz(url: str, email: str, secret: str):
    """
    Visit the quiz page, extract the question, perform required computation,
    and return JSON answer.
    """
    print(f"🟢 Visiting quiz page: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)

            # wait up to 60s for #result (JS-rendered content)
            try:
                await page.wait_for_selector("#result", timeout=60000)
                content = await page.inner_html("#result")
            except Exception:
                content = await page.content()
                print("⚠️ #result not found, using full page HTML")

            print("✅ Page loaded successfully")

            # Try to extract embedded JSON question if present
            if "<pre>" in content:
                import re
                match = re.search(r"<pre[^>]*>(.*?)</pre>", content, re.DOTALL)
                if match:
                    text = match.group(1)
                    text = text.replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">")
                    try:
                        question_data = json.loads(text)
                    except Exception:
                        question_data = {"raw_text": text}
                else:
                    question_data = {"raw_html": content[:500]}
            else:
                question_data = {"raw_html": content[:500]}

            # -----------------------------------------------------
            # ✅ Sample demo logic — detect “value” column sum
            # -----------------------------------------------------
            if "Download" in content or ".csv" in content or ".xlsx" in content:
                import re
                file_url_match = re.search(r'href="([^"]+\.(?:csv|xlsx))"', content)
                if file_url_match:
                    file_url = file_url_match.group(1)
                    print(f"📂 Detected file URL: {file_url}")
                    data = download_file(file_url)
                    if isinstance(data, pd.DataFrame):
                        if "value" in data.columns:
                            total = data["value"].sum()
                            answer = total
                        else:
                            answer = f"No 'value' column found in {data.columns.tolist()}"
                    else:
                        answer = data
                else:
                    answer = "No downloadable file link found."
            else:
                answer = "Parsed basic HTML quiz. (Demo mode)"

        except Exception as e:
            print("❌ Error solving quiz:", str(e))
            answer = {"error": str(e)}

        finally:
            await browser.close()

    # Return answer JSON (as per assignment)
    return {"status": "ok", "email": email, "answer": answer}
