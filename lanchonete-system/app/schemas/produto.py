from pydantic import BaseModel, Field
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str = Field(min_length=1)
    preco: float = Field(gt=0)

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1)
    preco: Optional[float] = Field(None, gt=0)
    ativo: Optional[bool] = None

class ProdutoResponse(ProdutoBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True
