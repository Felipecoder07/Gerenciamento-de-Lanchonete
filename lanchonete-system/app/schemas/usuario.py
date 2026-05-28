from pydantic import BaseModel, Field
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str = Field(min_length=1)
    papel: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1)
    papel: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
