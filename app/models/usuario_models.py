from sqlalchemy import String, Integer, Boolean, text, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    senha: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true")
    )
    
    admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("false")
    )

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

    def as_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "ativo": self.ativo,
            "admin": self.admin
        }