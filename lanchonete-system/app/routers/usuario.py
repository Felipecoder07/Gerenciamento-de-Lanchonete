from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
logger = logging.getLogger(__name__)

PAPEIS_VALIDOS = ["GARCOM", "COZINHA", "ADMIN"]

@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        if usuario.papel not in PAPEIS_VALIDOS:
            raise HTTPException(
                status_code=400,
                detail=f"Papel inválido. Use um de: {PAPEIS_VALIDOS}"
            )
        novo_usuario = Usuario(**usuario.model_dump())
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        logger.info(f"Usuário criado: {novo_usuario.id}")
        return novo_usuario
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")

@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    try:
        return db.query(Usuario).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar usuários")

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter usuário")

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, usuario_update: UsuarioUpdate, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        if usuario_update.papel and usuario_update.papel not in PAPEIS_VALIDOS:
            raise HTTPException(
                status_code=400,
                detail=f"Papel inválido. Use um de: {PAPEIS_VALIDOS}"
            )
        
        dados_atualizacao = usuario_update.model_dump(exclude_unset=True)
        for campo, valor in dados_atualizacao.items():
            setattr(usuario, campo, valor)
        
        db.commit()
        db.refresh(usuario)
        logger.info(f"Usuário atualizado: {usuario.id}")
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar usuário")

@router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        db.delete(usuario)
        db.commit()
        logger.info(f"Usuário deletado: {usuario_id}")
        return {"msg": "Usuário deletado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao deletar usuário")
