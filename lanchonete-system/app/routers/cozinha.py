from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models.pedido import Pedido
from app.schemas.services.pedido_service import atualizar_status_pedido

router = APIRouter(prefix="/cozinha", tags=["Cozinha"])
logger = logging.getLogger(__name__)

@router.get("/pedidos")
def pedidos_pendentes(db: Session = Depends(get_db)):
    try:
        pedidos = db.query(Pedido).filter(
            Pedido.status.in_(["PENDENTE", "EM_PREPARO"])
        ).all()
        return pedidos
    except Exception as e:
        logger.error(f"Erro ao listar pedidos da cozinha: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar pedidos")

@router.put("/pedido/{pedido_id}/status")
def atualizar_status(
    pedido_id: int,
    novo_status: str,
    db: Session = Depends(get_db)
):
    try:
        pedido = atualizar_status_pedido(db, pedido_id, novo_status)
        logger.info(f"Status do pedido {pedido_id} atualizado para {novo_status}")
        return {
            "msg": "Status atualizado com sucesso",
            "pedido_id": pedido.id,
            "novo_status": pedido.status
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar status: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar status")
