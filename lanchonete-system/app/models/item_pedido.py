from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database import Base

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), index=True)
    quantidade = Column(Integer, nullable=False)
    
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto")

    __table_args__ = (
        Index("idx_item_pedido_id", pedido_id),
        Index("idx_item_produto_id", produto_id),
    )
