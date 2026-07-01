"""Quick manual tests for the Weledi API.

Run the server first:  ./enviro/bin/python manage.py runserver
Then:                   ./enviro/bin/python data.py
"""
import requests

BASE = "http://127.0.0.1:8000"


# ---------------------------------------------------------------------------
# Posts
# ---------------------------------------------------------------------------
def list_posts():
    r = requests.get(f"{BASE}/api/posts/")
    print("GET /api/posts/ ->", r.status_code)
    print(r.json())


def create_post():
    payload = {
        "title": "Flexi Foods kufunguliwa Kimara",
        "body": "Mguu kwa mguu mpaka Flexi Consult, tunawaletea kijana "
                "alietengeneza mfumo wa kuplan chakula kwa wagonjwa wa kisukari.",
    }
    r = requests.post(f"{BASE}/api/posts/", json=payload)
    print("POST /api/posts/ ->", r.status_code)
    print(r.json())


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
def signup():
    payload = {
        "username": "amina",
        "phone": "+255700111222",
        "password": "SafariNews2026",
    }
    r = requests.post(f"{BASE}/api/auth/signup/", json=payload)
    print("POST /api/auth/signup/ ->", r.status_code)
    print(r.json())


def login():
    payload = {
        "username": "amina",
        "password": "SafariNews2026",
    }
    r = requests.post(f"{BASE}/api/auth/login/", json=payload)
    print("POST /api/auth/login/ ->", r.status_code)
    print(r.json())


if __name__ == "__main__":
    list_posts()
    create_post()
    signup()
    login()
