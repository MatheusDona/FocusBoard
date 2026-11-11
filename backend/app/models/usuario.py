from app.database import Base
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Usuario(Base):
    __tablename__ = "usuarios"

    tarefas = relationship("Tarefa", back_populates="usuario", cascade="all, delete", passive_deletes=True)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    senha_hash: Mapped[str] = mapped_column(String, nullable=False)
    email_verificado: Mapped[bool] = mapped_column(Boolean, default=False ,nullable=False)