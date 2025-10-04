from app.repositories.manager_repository import ManagerRepository
from app.models.manager import Manager
from app.utils.audit import log_action

class ManagerService:
    def __init__(self, repo: ManagerRepository):
        self.repo = repo

    def create(self, display_name: str, phone: str | None, email: str | None) -> Manager:
        m = Manager(display_name=display_name.strip(), phone=phone, email=email)
        s = self.repo.create(m)
        log_action(self.repo.db, "manager", s.id, "CREATE")
        return s

    def list_all(self) -> list[Manager]:
        return list(self.repo.list_all())
