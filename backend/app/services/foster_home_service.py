from app.repositories.foster_home_repository import FosterHomeRepository
from app.models.foster_home import FosterHome
from app.utils.audit import log_action

class FosterHomeService:
    def __init__(self, repo: FosterHomeRepository):
        self.repo = repo

    def create(self, name: str, phone: str | None, email: str | None, address: str | None, comments: str | None) -> FosterHome:
        f = FosterHome(name=name.strip(), phone=phone, email=email, address=address, comments=comments)
        s = self.repo.create(f)
        log_action(self.repo.db, "foster_home", s.id, "CREATE")
        return s

    def list_all(self) -> list[FosterHome]:
        return list(self.repo.list_all())
