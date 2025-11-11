from app.repositories.manager_repository import ManagerRepository
from app.models.manager import Manager
from app.utils.audit import log_action
from app.schemas.manager import ManagerCreate
from app.models.manager import Manager, StatusEnum, RoleEnum
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


class ManagerService:
    def __init__(self, repo: ManagerRepository):
        self.repo = repo

    def create(self, data: ManagerCreate) -> Manager:
        # email must be unique
        """ email_norm = data.email.strip.lower()

        if self.repo.get_by_email(email_norm):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="manager email must be unique") """
        manager = Manager(display_name= data.display_name.strip(), phone=data.phone,email=data.email, status= StatusEnum(data.status), role = RoleEnum(data.role))
        created = self.repo.create(manager)

        log_action(self.repo.db, "manager", created.id, "CREATE")
        return created
        
       
    """  try:   
            created = self.repo.create(manager)
    except IntegrityError:
        self.repo.db.rollback()
        # topelt-kaitse, kui paralleelselt lisatakse sama nimega
        raise HTTPException(status_code=409, detail="manager email must be unique") """
    
       

    def list_all(self) -> list[Manager]:
        rows = list(self.repo.list_all())
        return list(self.repo.list_all())
