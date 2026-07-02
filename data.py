"""Quick manual tests for the Weledi API.

Run the server first:  ./enviro/bin/python manage.py runserver
Then:                   ./enviro/bin/python data.py

The /api/posts/ endpoint now REQUIRES authentication (Token or Basic).
Auth endpoints (signup/login/token) stay public so you can get in.
"""
import base64

import requests

BASE = "http://127.0.0.1:8000"

USERNAME = "bright"
PASSWORD = "1234"


# ---------------------------------------------------------------------------
# Auth  (public endpoints)
# ---------------------------------------------------------------------------
def signup():
    payload = {"username": USERNAME, "phone": "+255700111222", "password": PASSWORD}
    r = requests.post(f"{BASE}/api/auth/signup/", json=payload)
    print("POST /api/auth/signup/ ->", r.status_code)
    print(r.json())


def get_token():
    """Log in and return the auth token string."""
    r = requests.post(f"{BASE}/api/auth/token/",
                      json={"username": USERNAME, "password": PASSWORD})
    print("POST /api/auth/token/ ->", r.status_code)
    print(r.json())
    return r.json().get("token")


# ---------------------------------------------------------------------------
# Posts  (protected endpoints)
# ---------------------------------------------------------------------------
def list_posts_no_auth():
    r = requests.get(f"{BASE}/api/posts/")
    print("GET /api/posts/ (no auth) ->", r.status_code, "(expect 401)")


def list_posts_token(token):
    r = requests.get(f"{BASE}/api/posts/",
                     headers={"Authorization": f"Token {token}"})
    print("GET /api/posts/ (token) ->", r.status_code)
    print(r.json())


def list_posts_basic():
    # HTTP Basic auth = base64("username:password") behind the "Basic" scheme.
    # (Token/JWT use the "Bearer" scheme instead; "Basic" is for user:pass.)
    raw = f"{USERNAME}:{PASSWORD}".encode()
    print(raw)
    encoded = base64.b64encode(raw).decode()
    print(encoded)
    r = requests.get(f"{BASE}/api/posts/",
                     headers={"Authorization": f"Basic {encoded}"})
    print(r.json())
    print("GET /api/posts/ (basic) ->", r.status_code)


def create_post_token(token):
    payload = {
        "title": "Flexi Foods kufunguliwa Kimara",
        "body": "Mguu kwa mguu mpaka Flexi Consult, tunawaletea kijana "
                "alietengeneza mfumo wa kuplan chakula kwa wagonjwa wa kisukari.",
    }
    r = requests.post(f"{BASE}/api/posts/", json=payload,
                      headers={"Authorization": f"Token {token}"})
    print("POST /api/posts/ (token) ->", r.status_code)


if __name__ == "__main__":
    # signup()                 # run once to create the user
    # token = "cc3d9ef6d64167e641c87b313d17622d1806d7efi"
    # list_posts_no_auth()       # blocked -> 401
    # list_posts_token(token)    # allowed via token
    list_posts_basic()         # allowed via basic auth
    # create_post_token(token)   # create through the protected endpoint
