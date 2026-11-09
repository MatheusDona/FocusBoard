from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import verificar_token
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    dados = verificar_token(token)

    if dados is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )

    usuario_id = dados.get("sub")

    if not usuario_id or not usuario_id.isdigit():
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )
    usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    return usuario      