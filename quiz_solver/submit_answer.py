import requests

def submit_answer(url, email, secret, answer):
    payload = {
        "email": email,
        "secret": secret,
        "url": url,
        "answer": answer
    }
    response = requests.post(url, json=payload)
    return response.json()
