from sqlalchemy import Column, Integer, String, Index
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    papel = Column(String, nullable=False, index=True)

    __table_args__ = (
        Index("idx_usuario_papel", papel),
    )
