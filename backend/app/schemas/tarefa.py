from pydantic import BaseModel, ConfigDict
from datetime import date
from enum import Enum

class PrioridadeEnum(str, Enum):
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"

class StatusEnum(str, Enum):
    FAZER = "Fazer"
    ANDAMENTO = "Em andamento"
    FEITO = "Feito"
    PENDENTE = "Pendente"

class TarefaCreate(BaseModel):
    titulo: str
    descricao: str | None = None
    prioridade: PrioridadeEnum
    data_prazo: date | None = None

class TarefaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descricao: str | None = None
    prioridade: PrioridadeEnum
    status: StatusEnum
    data_prazo: date | None = None
    usuario_id: int

class TarefaUpdate(BaseModel):

    titulo: str | None = None
    descricao: str | None = None
    prioridade: PrioridadeEnum | None = None
    status: StatusEnum | None = None
    data_prazo: date | None = None
    