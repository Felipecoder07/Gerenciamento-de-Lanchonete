from pydantic import BaseModel, Field
from typing import List, Optional

class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)

class ProdutoMini(BaseModel):
    id: int
    nome: str
    preco: float

class ItemPedidoResponse(BaseModel):
    id: int
    pedido_id: int
    produto_id: int
    quantidade: int
    produto: ProdutoMini

    class Config:
        from_attributes = True
