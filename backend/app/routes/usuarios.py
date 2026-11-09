from fastapi import APIRouter, Depends
from app.schemas.usuario import UsuarioResponse
from app.dependencies.auth import get_usuario_atual
from app.models.usuario import Usuario

router = APIRouter()

@router.get("/usuarios/me", response_model=UsuarioResponse)
def dados_usuario(usuario: Usuario = Depends(get_usuario_atual)):
    return usuario