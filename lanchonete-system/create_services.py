import os
import sys

path = r"c:\Users\Mateus\OneDrive\Documentos\Projeto Giga\lanchonete-system\app\services"
os.makedirs(path, exist_ok=True)

# Create __init__.py
init_file = os.path.join(path, "__init__.py")
with open(init_file, "w") as f:
    f.write("")

# Create pedido_service.py
service_file = os.path.join(path, "pedido_service.py")
with open(service_file, "w") as f:
    f.write("""from sqlalchemy.orm import Session
from app.models.pedido import Pedido

def atualizar_status_pedido(db: Session, pedido_id: int, status: str):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    if not pedido:
        raise ValueError(f"Pedido {pedido_id} não encontrado")
    
    status_validos = ["PENDENTE", "EM_PREPARO", "PRONTO", "ENTREGUE", "CANCELADO"]
    if status not in status_validos:
        raise ValueError(f"Status '{status}' inválido. Use um de: {status_validos}")
    
    pedido.status = status
    db.commit()
    db.refresh(pedido)
    
    return pedido
""")

print(f"✓ Pasta criada: {path}")
print(f"✓ Arquivos criados")
