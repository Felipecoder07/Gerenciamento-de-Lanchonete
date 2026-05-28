from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.produto import Produto
from app.schemas.pedido import PedidoCreate, PedidoResponse

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
logger = logging.getLogger(__name__)

ORIGENS_VALIDAS = ["GARCOM", "WHATSAPP"]

@router.post("/", response_model=PedidoResponse)
def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    try:
        if pedido.origem not in ORIGENS_VALIDAS:
            raise HTTPException(
                status_code=400,
                detail=f"Origem inválida. Use um de: {ORIGENS_VALIDAS}"
            )
        
        if not pedido.itens:
            raise HTTPException(status_code=400, detail="Pedido deve ter pelo menos um item")
        
        for item in pedido.itens:
            if item.quantidade <= 0:
                raise HTTPException(status_code=400, detail="Quantidade deve ser maior que 0")
            
            produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
            if not produto:
                raise HTTPException(status_code=404, detail=f"Produto {item.produto_id} não encontrado")
            if not produto.ativo:
                raise HTTPException(status_code=400, detail=f"Produto {item.produto_id} está desativado")
        
        novo_pedido = Pedido(origem=pedido.origem)
        db.add(novo_pedido)
        db.commit()
        db.refresh(novo_pedido)

        for item in pedido.itens:
            item_db = ItemPedido(
                pedido_id=novo_pedido.id,
                produto_id=item.produto_id,
                quantidade=item.quantidade
            )
            db.add(item_db)

        db.commit()
        db.refresh(novo_pedido)
        logger.info(f"Pedido criado: {novo_pedido.id}")
        return novo_pedido
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar pedido: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar pedido")

@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    try:
        return db.query(Pedido).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Erro ao listar pedidos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar pedidos")

@router.get("/{pedido_id}", response_model=PedidoResponse)
def obter_pedido(pedido_id: int, db: Session = Depends(get_db)):
    try:
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return pedido
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter pedido: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter pedido")
