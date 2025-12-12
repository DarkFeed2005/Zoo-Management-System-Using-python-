import bcrypt
from .db import query

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def login(username: str, password: str):
    user = query("SELECT u.id, u.username, u.password_hash, r.name AS role FROM users u JOIN roles r ON u.role_id=r.id WHERE u.username=%s AND u.is_active=1", (username,), fetchone=True)
    if not user:
        return None
    if verify_password(password, user["password_hash"]):
        return {"id": user["id"], "username": user["username"], "role": user["role"]}
    return None