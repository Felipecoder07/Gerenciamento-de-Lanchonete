from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse

router = APIRouter(prefix="/produtos", tags=["Produtos"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=ProdutoResponse)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    try:
        novo_produto = Produto(**produto.model_dump())
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)
        logger.info(f"Produto criado: {novo_produto.id}")
        return novo_produto
    except Exception as e:
        logger.error(f"Erro ao criar produto: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar produto")

@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    try:
        return db.query(Produto).filter(Produto.ativo == True).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Erro ao listar produtos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar produtos")

@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    try:
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return produto
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter produto: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter produto")

@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, produto_update: ProdutoUpdate, db: Session = Depends(get_db)):
    try:
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        dados_atualizacao = produto_update.model_dump(exclude_unset=True)
        for campo, valor in dados_atualizacao.items():
            setattr(produto, campo, valor)
        
        db.commit()
        db.refresh(produto)
        logger.info(f"Produto atualizado: {produto.id}")
        return produto
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar produto: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar produto")

@router.delete("/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    try:
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        produto.ativo = False
        db.commit()
        logger.info(f"Produto desativado: {produto.id}")
        return {"msg": "Produto desativado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar produto: {e}")
        raise HTTPException(status_code=500, detail="Erro ao deletar produto")
