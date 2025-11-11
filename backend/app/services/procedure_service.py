from datetime import date

from minio import Minio
from fastapi import UploadFile, HTTPException

from app.models.cat_procedure import CatProcedure, ProcedureTypeEnum

from app.repositories.cat_procedure_repository import CatProcedureRepository
from app.repositories.cat_repository import CatRepository

from app.services.file_utils import upload_to_minio
from app.utils.audit import log_action

class ProcedureService:
    def __init__(self, proc_repo: CatProcedureRepository, cat_repo: CatRepository, minio_client: Minio | None):
        self.proc_repo = proc_repo
        self.cat_repo = cat_repo
        self.minio = minio_client

    # add new procedure for cat
    def add(self, cat_id: int, type_: str, is_repeat: bool, at_date: date, notes: str | None, payment: int | None, file: UploadFile | None):
        if self.cat_repo.get_with_related(cat_id) is None:
            raise HTTPException(status_code=404, detail="cat not found")

        if self.minio is None:
            raise HTTPException(status_code=500, detail="minio bucket was not passed")

        file_key = None
        if file is not None:
            file_key = upload_to_minio(self.minio, file)

        p = CatProcedure(
            cat_id=cat_id,
            type=ProcedureTypeEnum(type_),
            is_repeat=is_repeat,
            at_date=at_date,
            notes=notes,
            payment=payment,
            file_object=file_key,
        )
        p = self.proc_repo.create(p)
        log_action(self.proc_repo.db, "cat_procedure", p.id, "CREATE")
        return p

    def list_for_cat(self, cat_id: int):
        return list(self.proc_repo.list_by_cat(cat_id))
