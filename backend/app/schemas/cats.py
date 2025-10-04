from datetime import date
from typing import Literal
from pydantic import BaseModel, Field
from .common import ORMBase
from .refs import ManagerRef, FosterHomeRef

Sex = Literal["isane", "emane", "unknown"]
Status = Literal["ACTIVE","FOSTER","ADOPTED","ARCHIVED","KADUNUD","BRONEERITUD"]

class CatCreate(BaseModel):
    # only 'name' required; everything else optional
    name: str = Field(min_length=1, max_length=200)
    sex: Sex | None = "unknown"
    chip_number: str | None = None
    status: Status = "ACTIVE"

    manager_id: int | None = None
    foster_home_id: int | None = None
    colony_id: int | None = None

    kk_alates: date | None = None
    birth_date: date | None = None
    foster_end: date | None = None

    location_text: str | None = None
    notes: str | None = None

    # medical (estonian)
    ussitableti_nimi: str | None = None
    ussitablett: date | None = None
    ussit_kordus: date | None = None

    turjatilga_nimi: str | None = None
    turjatilk: date | None = None
    turj_kordus: date | None = None

    i_vaktsiin: date | None = None
    kordusvax: date | None = None

    ster_kastr: bool | None = None

class CatRead(ORMBase):
    id: int
    name: str
    sex: Sex | None
    chip_number: str | None
    status: Status

    manager: ManagerRef | None = None
    foster_home: FosterHomeRef | None = None

    colony_id: int | None = None

    kk_alates: date | None = None
    birth_date: date | None = None
    foster_end: date | None = None

    location_text: str | None = None
    notes: str | None = None

    ussitableti_nimi: str | None = None
    ussitablett: date | None = None
    ussit_kordus: date | None = None

    turjatilga_nimi: str | None = None
    turjatilk: date | None = None
    turj_kordus: date | None = None

    i_vaktsiin: date | None = None
    kordusvax: date | None = None

    ster_kastr: bool | None = None

    primary_photo_object: str | None = None
