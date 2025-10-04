

from app.models.audit_log import AuditLog


def log_action(db, entity_type: str, entity_id: int, action: str):
    log = AuditLog(entity_type=entity_type, entity_id=entity_id, action=action) 
    db.add(log)
    db.commit()