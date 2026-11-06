from fastapi import FastAPI
from app.database import Base, engine
from app.models.usuario import Usuario
from app.routes.auth import router as auth_router

app = FastAPI(
    title="Sistema Kanban",
    description="Sistema de gerenciamento de tarefas",
    version="1.0.0"
)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)
