from fastapi import HTTPException, UploadFile
from app.repositories.cat_repository import CatRepository
from app.schemas.cats import CatCreate, CatUpdate
from app.models.cat import Cat
from app.services.file_utils import upload_to_minio
from app.utils.audit import log_action


class CatService:
    def __init__(self, repo: CatRepository, minio_client):
        self.repo = repo
        self.minio = minio_client

    def create_from_payload(self, data: CatCreate, primary_image: UploadFile | None) -> Cat:
        if not data.name or not data.name.strip():
            raise HTTPException(status_code=422, detail="name is required")

        primary_obj = None
        if primary_image is not None:
            primary_obj = upload_to_minio(self.minio, primary_image)

        cat = Cat(**data.model_dump(exclude_unset=True))
        cat.name = cat.name.strip()  
        if primary_obj:
            cat.primary_photo_object = primary_obj

        cat = self.repo.create(cat)
        log_action(self.repo.db, "cat", cat.id, "CREATE")
        return cat


    def get(self, cat_id: int) -> Cat:
        cat = self.repo.get_with_related(cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="cat not found")
        return cat

    def list_all(self) -> list[Cat]:
        return list(self.repo.list_all_with_related())
    
    def update_from_payload(self, cat_id: int, payload: CatUpdate, new_primary_image) -> Cat | None:
        # cat id is target row, payload uses the fields defined in schema to build a patch dict
        object_key = None
        if new_primary_image is not None:
            object_key = upload_to_minio(self.minio, new_primary_image)

        data = payload.model_dump(exclude_unset=True)
        if object_key:
            data["primary_photo_object"] = object_key

        updated_cat = self.repo.update(cat_id, data)
        if updated_cat:
            log_action(self.repo.db, "cat", cat_id, "UPDATE") 
        return updated_cat
    
    def delete(self, cat: Cat) -> None:
        self.repo.delete(cat)
        log_action(self.repo.db, "cat", cat.id, "DELETE")