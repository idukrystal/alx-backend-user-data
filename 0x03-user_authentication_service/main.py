#!/usr/bin/env python3
"""
Main file: test all functions integration
"""

from requests import delete, get, post, put
from json import dumps
base_url = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    response = post(base_url+"/users", {"email": email, "password": password})
    if response.status_code == 200:
        assert response.json() == {"email": f"{email}",
                                   "message": "user created"
                                   }
    else:
        assert response.status_code == 400
        assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    response = post(
        base_url+"/sessions",
        {"email": email, "password": password}
    )
    if response.status_code == 200:
        assert response.json() == {'email': f'{email}', 'message': 'logged in'}
    else:
        assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    response = post(
        base_url+"/sessions",
        {"email": email, "password": password}
    )
    if response.status_code == 200:
        assert response.json() == {'email': f'{email}', 'message': 'logged in'}
        return response.cookies["session_id"]
    else:
        assert response.status_code == 401


def profile_unlogged() -> None:
    response = get(base_url+"/profile")
    assert response.status_code == 403


def profile_logged(session_id: str, email: str) -> None:
    response = get(base_url+"/profile", cookies={"session_id": session_id})
    if session_id:
        assert response.status_code == 200
        assert response.json() == {"email": f"{email}"}
    else:
        assert response.status_code == 403


def log_out(session_id: str) -> None:
    cookies = {'session_id': session_id}
    response = delete(base_url+"/sessions", cookies=cookies)
    if session_id:
        assert response.status_code == 200
        assert response.json() == {"message": "Bienvenue"}
    else:
        assert response.status_code == 403


def reset_password_token(email: str) -> str:
    response = post(base_url+"/reset_password", {"email": email})
    assert response.status_code == 200
    token = response.json()["reset_token"]
    assert response.json() == {"email": f"{email}", "reset_token": f"{token}"}
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    response = put(
        base_url+"/reset_password",
        {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    )
    assert response.status_code == 200
    assert response.json() == {"email": f"{email}",
                               "message": "Password updated"
                               }


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id, EMAIL)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
