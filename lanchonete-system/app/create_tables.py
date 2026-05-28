from app.database import Base, engine
import app.models  # força o carregamento dos models

print("Criando tabelas...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
