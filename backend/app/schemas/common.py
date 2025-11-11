from pydantic import BaseModel

class ORMBase(BaseModel):
    class ConfigDict:
        from_attributes = True  # allow Pydantic to read ORM attributes
