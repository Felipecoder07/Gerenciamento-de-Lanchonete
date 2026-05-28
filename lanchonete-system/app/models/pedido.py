from sqlalchemy import Column, Integer, String, DateTime, Float, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    origem = Column(String, nullable=False, index=True)
    status = Column(String, default="PENDENTE", index=True)
    total = Column(Float, default=0)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_pedido_status_criado", status, criado_em),
    )
