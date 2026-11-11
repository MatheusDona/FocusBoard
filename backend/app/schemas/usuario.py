from pydantic import BaseModel, EmailStr, ConfigDict

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class UsuarioUpdateNome(BaseModel):
    nome: str

class UsuarioUpdateSenha(BaseModel):
    senha_atual: str
    nova_senha: str
    confirmar_senha: str

class ReenviarConfirmacao(BaseModel):
    email: EmailStr