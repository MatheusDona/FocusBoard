from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin, ReenviarConfirmacao
from app.core.security import hash_senha, verificar_senha, criar_token
from app.core.security import criar_token_confirmacao
from app.services.email_service import enviar_email

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

    token = criar_token_confirmacao(novo_usuario.id)

    link_confirmacao = f"http://127.0.0.1:8000/confirmar-email?token={token}"

    enviar_email(
        destinatario=novo_usuario.email,
        assunto="Confirme seu e-mail - FocusBoard",
        conteudo=f"""
Olá, {novo_usuario.nome}!

Para confirmar seu e-mail, acesse o link abaixo:

{link_confirmacao}

Este link expira em 15 minutos.

Equipe FocusBoard
"""
)

    return novo_usuario

@router.post("/reenviar-confirmacao")
def reenviar_confirmacao(dados: ReenviarConfirmacao, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )
    
    if usuario.email_verificado:
        raise HTTPException(
            status_code=400,
            detail="Este e-mail já foi confirmado"
        )

    token = criar_token_confirmacao(usuario.id)

    link_confirmacao = f"http://127.0.0.1:8000/confirmar-email?token={token}"

    enviar_email(
        destinatario=usuario.email,
        assunto="Confirme seu e-mail - FocusBoard",
        conteudo=f"""
Olá, {usuario.nome}!

Para confirmar seu e-mail, acesse o link abaixo:

{link_confirmacao}

Este link expira em 15 minutos.

Equipe FocusBoard
"""
    )

    return {"detail": "E-mail de confirmação enviado com sucesso!"}

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

    if not usuario.email_verificado:
        raise HTTPException(
            status_code=403,
            detail="Confirme seu e-mail antes de fazer login"
        )

    token = criar_token(usuario.id)

    token_gerado = {
        "access_token": token,
        "token_type": "bearer"
    }

    return token_gerado
    
