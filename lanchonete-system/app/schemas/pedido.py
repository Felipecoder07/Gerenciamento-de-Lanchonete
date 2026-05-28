from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.item_pedido import ItemPedidoCreate, ItemPedidoResponse
from datetime import datetime

class PedidoCreate(BaseModel):
    origem: str
    itens: List[ItemPedidoCreate] = Field(min_items=1)

class PedidoResponse(BaseModel):
    id: int
    origem: str
    status: str
    total: float
    criado_em: datetime
    itens: List[ItemPedidoResponse]

    class Config:
        from_attributes = True
