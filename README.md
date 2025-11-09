
# LLM Quiz Solver

### 🧩 Description
A FastAPI + Playwright-based automation that fetches and solves dynamic quiz pages
for the LLM Evaluator assignment.

### ⚙️ How to Run (in GitHub Codespaces)

```bash
# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload --port 8000

# In a new terminal, run test
python tests/test_demo.py
