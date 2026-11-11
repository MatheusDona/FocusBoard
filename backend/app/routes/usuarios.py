from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario import UsuarioResponse, UsuarioUpdateNome, UsuarioUpdateSenha
from app.dependencies.auth import get_usuario_atual
from app.models.usuario import Usuario
from app.core.security import verificar_senha, hash_senha, verificar_token_confirmacao

router = APIRouter()

@router.get("/confirmar-email")
def confirmar_email(token: str, db: Session = Depends(get_db)):
    dados_token = verificar_token_confirmacao(token)

    if dados_token is None:
        raise HTTPException(
            status_code=400,
            detail="Link de confirmação inválido ou expirado"
        )

    usuario_id = dados_token.get("sub")

    if not usuario_id or not usuario_id.isdigit():
        raise HTTPException(
            status_code=400,
            detail="Token inválido"
        )

    usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    usuario.email_verificado = True

    db.commit()
    db.refresh(usuario)

    return {"detail": "E-mail confirmado com sucesso!"}

@router.get("/usuarios/me", response_model=UsuarioResponse)
def dados_usuario(usuario: Usuario = Depends(get_usuario_atual)):
    return usuario

@router.patch("/usuarios/me/nome", response_model=UsuarioResponse)
def atualizar_nome(dados: UsuarioUpdateNome, usuario: Usuario = Depends(get_usuario_atual), db: Session = Depends(get_db)):
    usuario.nome = dados.nome
    db.commit()
    db.refresh(usuario)

    return usuario

@router.patch("/usuarios/me/senha")
def atualizar_senha(dados: UsuarioUpdateSenha, usuario: Usuario = Depends(get_usuario_atual), db: Session = Depends(get_db)):
    senha = verificar_senha(dados.senha_atual, usuario.senha_hash)
    if senha is False:
        raise HTTPException(
        status_code=400,
        detail="Senha atual incorreta"
    )

    if dados.nova_senha != dados.confirmar_senha:        
        raise HTTPException(
            status_code=400,
            detail="As senhas precisam ser iguais"
    )

    usuario.senha_hash = hash_senha(dados.nova_senha)

    db.commit()

    return {"detail": "Senha alterada com sucesso"}

@router.delete("/usuarios/me")
def excluir_usuario(db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_atual)):
    db.delete(usuario)
    db.commit()

    return {"detail": "Conta excluída com sucesso"}

    