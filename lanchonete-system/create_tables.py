from app.database import Base, engine
import app.models

print("Tabelas encontradas:", Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)
print("Tabelas criadas!")
