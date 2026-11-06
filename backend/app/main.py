from fastapi import FastAPI
from app.database import Base, engine
from app.models.usuario import Usuario

app = FastAPI(
    title="Sistema Kanban",
    description="Sistema de gerenciamento de tarefas",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"mensagem": "API funcionando!"}