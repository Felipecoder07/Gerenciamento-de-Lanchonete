from fastapi import FastAPI
from app.routers import produto, pedido, cozinha, usuario

app = FastAPI(
    title="Sistema de Pedidos - Lanchonete do Giga",
    description="Automação de pedidos para garçom, WhatsApp e cozinha",
    version="1.0.0"
)

app.include_router(produto.router)
app.include_router(pedido.router)
app.include_router(cozinha.router)
app.include_router(usuario.router)
