from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.pedido import Pedido
from app.models.produto import Produto

STATUS_VALIDOS = ["PENDENTE", "EM_PREPARO", "PRONTO", "ENTREGUE"]

def validar_transicao_status(status_atual: str, novo_status: str) -> bool:
    fluxo = {
        "PENDENTE": ["EM_PREPARO"],
        "EM_PREPARO": ["PRONTO"],
        "PRONTO": ["ENTREGUE"],
        "ENTREGUE": []
    }
    return novo_status in fluxo.get(status_atual, [])

def atualizar_status_pedido(
    db: Session,
    pedido_id: int,
    novo_status: str
):
    if novo_status not in STATUS_VALIDOS:
        raise HTTPException(status_code=400, detail="Status inválido")

    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if not validar_transicao_status(pedido.status, novo_status):
        raise HTTPException(
            status_code=400,
            detail=f"Transição inválida: {pedido.status} → {novo_status}"
        )

    pedido.status = novo_status
    db.commit()
    db.refresh(pedido)
    return pedido
