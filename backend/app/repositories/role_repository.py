from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.role import Role

class RoleRepository(BaseRepository):
    def create(self, r: Role) -> Role:
        self.db.add(r)
        self.db.commit()
        self.db.refresh(r)
        return r

    def get_by_name(self, role_name: str) -> Role | None:
        stmt = select(Role).where(Role.name == role_name)
        return self.db.execute(stmt).scalars().first()

    def get_by_id(self, role_id: int) -> Role | None:
        return self.db.get(Role, role_id)