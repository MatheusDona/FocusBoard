from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import get_usuario_atual
from app.models.tarefa import Tarefa
from app.schemas.tarefas import TarefaCreate, TarefaResponse