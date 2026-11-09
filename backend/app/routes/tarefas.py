from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import get_usuario_atual
from app.models.tarefa import Tarefa
from app.models.usuario import Usuario
from app.schemas.tarefa import TarefaCreate, TarefaResponse, TarefaUpdate

router = APIRouter()

@router.post("/tarefas", response_model=TarefaResponse)
def criar_tarefa(dados: TarefaCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_atual)):
    tarefa = Tarefa(
        titulo = dados.titulo,
        descricao = dados.descricao,
        prioridade = dados.prioridade,
        status = "Fazer",
        data_prazo = dados.data_prazo,
        usuario_id = usuario.id
    )

    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)  

    return tarefa

@router.get("/tarefas", response_model=list[TarefaResponse])
def listar_tarefas(db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_atual)):
    tarefas = db.query(Tarefa).filter(Tarefa.usuario_id == usuario.id).all()

    return tarefas

@router.get("/tarefas/{tarefa_id}", response_model=TarefaResponse)
def buscar_tarefa(tarefa_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_atual)):
    tarefa = db.query(Tarefa).filter(Tarefa.usuario_id == usuario.id, Tarefa.id == tarefa_id).first()

    if not tarefa:
        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada"
        )

    return tarefa

@router.put("/tarefas/{tarefa_id}", response_model=TarefaResponse)
def atualizar_tarefa(tarefa_id: int, dados: TarefaUpdate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_atual)):
    tarefa = db.query(Tarefa).filter(Tarefa.usuario_id == usuario.id, Tarefa.id == tarefa_id).first()
    
    if not tarefa:
        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada"
        )

    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(tarefa, campo, valor)

    db.add(tarefa)
    db.commit()
    db.refresh(tarefa) 

    return tarefa


@router.delete("/tarefas/{tarefa_id}")
def excluir_tarefa(tarefa_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_atual)):
    tarefa = db.query(Tarefa).filter(Tarefa.usuario_id == usuario.id, Tarefa.id == tarefa_id).first()
        
    if not tarefa:
        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada"
        )

    db.delete(tarefa)
    db.commit()

    return {"Mensagem" : "Tarefa excluida"}