from sqlalchemy import Column, Integer, String, Float, Boolean, Index
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True, index=True)
    preco = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True, index=True)

    __table_args__ = (
        Index("idx_produto_ativo", ativo),
    )
