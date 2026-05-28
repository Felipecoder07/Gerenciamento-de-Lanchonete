import os
file = r"c:\Users\Mateus\OneDrive\Documentos\Projeto Giga\lanchonete-system\create_services.py"
if os.path.exists(file):
    os.remove(file)
    print("Arquivo temporário removido")
