import auth

auth = auth.Auth()
auth.register_user("james", "jhon")
session = auth.create_session("james")
user = auth.get_user_from_session_id(session)
print(f">>> {user.reset_token}")
auth.get_reset_password_token("james")
print(f">>> {user.reset_token}")
auth.get_reset_password_token("jhon")
