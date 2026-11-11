from fastapi import FastAPI
from app.database import Base, engine
from app.models.usuario import Usuario
from app.models.tarefa import Tarefa
from app.routes.auth import router as auth_router
from app.routes.usuarios import router as usuario_router
from app.routes.tarefas import router as tarefas_router
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

bearer_scheme = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if "security" in operation:
                operation["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    title="Sistema Kanban",
    description="Sistema de gerenciamento de tarefas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(tarefas_router)

app.openapi = custom_openapi

Base.metadata.create_all(bind=engine)
