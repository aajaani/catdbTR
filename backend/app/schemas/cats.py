# app/schemas/cats.py
from datetime import date
from typing import Literal
from pydantic import BaseModel, Field
from .common import ORMBase
from .refs import ManagerRef, FosterHomeRef

Sex = Literal["male", "female", "unknown"]
Status = Literal["ACTIVE","FOSTER","ADOPTED","ARCHIVED","MISSING","RESERVED"]

class CatCreate(BaseModel):
    # only 'name' required; everything else optional
    name: str = Field(min_length=1, max_length=200)
    sex: Sex | None = "unknown"
    chip_number: str | None = None
    status: Status = "ACTIVE"

    manager_id: int | None = None
    foster_home_id: int | None = None
    colony_id: int | None = None

    intake_date: date | None = None
    birth_date: date | None = None
    foster_end_date: date | None = None

    location_text: str | None = None
    notes: str | None = None

    # medical 
    dewormer_name: str | None = None
    dewormed_at: date | None = None
    deworm_repeat_at: date | None = None

    spot_on_name: str | None = None
    spot_on_at: date | None = None
    spot_on_repeat_at: date | None = None

    first_vaccine_at: date | None = None
    booster_vaccine_at: date | None = None

    is_neutered: bool | None = None

class CatRead(ORMBase):
    id: int
    name: str
    sex: Sex | None
    chip_number: str | None
    status: Status

    manager: ManagerRef | None = None
    foster_home: FosterHomeRef | None = None

    colony_id: int | None = None

    intake_date: date | None = None
    birth_date: date | None = None
    foster_end_date: date | None = None

    location_text: str | None = None
    notes: str | None = None

    dewormer_name: str | None = None
    dewormed_at: date | None = None
    deworm_repeat_at: date | None = None

    spot_on_name: str | None = None
    spot_on_at: date | None = None
    spot_on_repeat_at: date | None = None

    first_vaccine_at: date | None = None
    booster_vaccine_at: date | None = None

    is_neutered: bool | None = None

    primary_photo_object: str | None = None


class CatUpdate(BaseModel):
    # everything optional
    name: str | None = None
    sex: Sex | None = None
    chip_number: str | None = None
    status: Status | None = None

    manager_id: int | None = None
    foster_home_id: int | None = None
    colony_id: int | None = None

    intake_date: date | None = None
    birth_date: date | None = None
    foster_end_date: date | None = None

    location_text: str | None = None
    notes: str | None = None

    dewormer_name: str | None = None
    dewormed_at: date | None = None
    deworm_repeat_at: date | None = None

    spot_on_name: str | None = None
    spot_on_at: date | None = None
    spot_on_repeat_at: date | None = None

    first_vaccine_at: date | None = None
    booster_vaccine_at: date | None = None

    is_neutered: bool | None = None
