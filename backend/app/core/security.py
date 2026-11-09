from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

password_hash = PasswordHash.recommended()

def hash_senha(senha: str):
    return password_hash.hash(senha)

def verificar_senha(senha: str, senha_hash: str):
    return password_hash.verify(senha, senha_hash)

def criar_token(usuario_id: int):
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    dados_token = {
        "sub": str(usuario_id),
        "exp": expiracao
    }

    token = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)

    return token

def verificar_token(token: str):
    try:
        dados = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return dados
    except jwt.InvalidTokenError:
        return None

