from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin
from app.core.security import hash_senha, verificar_senha, criar_token

router = APIRouter()

@router.post("/register", response_model=UsuarioResponse, status_code=201)
def registrar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if usuario is not None:
        raise HTTPException(
            status_code=409,
            detail="E-mail já utilizado"
        )

    senha_hash = hash_senha(dados.senha)

    novo_usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=senha_hash
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario

@router.post("/login")
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos"
        )

    if not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos"
        )

    token = criar_token(usuario.id)

    token_gerado = {
        "access_token": token,
        "token_type": "bearer"
    }

    return token_gerado
    
