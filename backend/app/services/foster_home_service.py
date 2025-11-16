from app.repositories.foster_home_repository import FosterHomeRepository
from app.models.foster_home import FosterHome
from app.utils.audit import log_action
from app.schemas.foster_home import FosterHomeUpdate
from fastapi import HTTPException

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
    
    def update(self, home_id: int, data: FosterHomeUpdate) -> FosterHome:
        foster_home_data = data.model_dump(exclude_unset=True)
        
        updated_home = self.repo.update(home_id, foster_home_data)

        if updated_home is None:
            raise HTTPException(status_code=404, detail="foster home not found")

        if updated_home:
            log_action(self.repo.db, "foster_home", home_id, "UPDATE") 
        return updated_home
