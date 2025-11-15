from pydantic import BaseModel, Field
from app.schemas.cats import CatRead

class ColonyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    notes: str | None = None
    cat_ids: list[int] | None = None


class ColonyRead(BaseModel):
    id: int
    name: str
    notes: str | None
    cats: list[CatRead]

    class ConfigDict:
        from_attributes = True


class ColonyUpdate(BaseModel):
    name: str | None = None
    notes: str | None = None
    cat_ids: list[int] | None = None