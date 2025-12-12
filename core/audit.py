from .db import query

def log(user_id: int, action: str, entity: str, entity_id: int | None, details: str | None = None):
    query(
        "INSERT INTO audit_logs (user_id, action, entity, entity_id, details) VALUES (%s,%s,%s,%s,%s)",
        (user_id, action, entity, entity_id, details)
    )