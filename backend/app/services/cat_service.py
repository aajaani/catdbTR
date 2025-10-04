from fastapi import HTTPException, UploadFile
from app.repositories.cat_repository import CatRepository
from app.schemas.cats import CatCreate
from app.models.cat import Cat
from app.services.file_utils import upload_to_minio

class CatService:
    def __init__(self, repo: CatRepository, minio_client):
        self.repo = repo
        self.minio = minio_client

    def create_from_payload(self, data: CatCreate, primary_image: UploadFile | None) -> Cat:
        if not data.name or not data.name.strip():
            raise HTTPException(status_code=422, detail="name is required")

        primary_obj = None
        if primary_image is not None:
            # Upload to MinIO, get object key
            primary_obj = upload_to_minio(self.minio, primary_image)

        cat = Cat(
            name=data.name.strip(),
            sex=data.sex,
            chip_number=data.chip_number,
            status=data.status,
            manager_id=data.manager_id,
            foster_home_id=data.foster_home_id,
            colony_id=data.colony_id,
            kk_alates=data.kk_alates,
            birth_date=data.birth_date,
            foster_end=data.foster_end,
            location_text=data.location_text,
            notes=data.notes,
            ussitableti_nimi=data.ussitableti_nimi,
            ussitablett=data.ussitablett,
            ussit_kordus=data.ussit_kordus,
            turjatilga_nimi=data.turjatilga_nimi,
            turjatilk=data.turjatilk,
            turj_kordus=data.turj_kordus,
            i_vaktsiin=data.i_vaktsiin,
            kordusvax=data.kordusvax,
            ster_kastr=data.ster_kastr,
            primary_photo_object=primary_obj,
        )
        return self.repo.create(cat)

    def get(self, cat_id: int) -> Cat:
        cat = self.repo.get_with_related(cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="cat not found")
        return cat

    def list_all(self) -> list[Cat]:
        return list(self.repo.list_all_with_related())
