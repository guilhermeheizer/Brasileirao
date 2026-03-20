from pydantic import BaseModel
from typing import Optional
from typing import List

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True

class ResponseUsuarioSchema(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool
    admin: bool
    
    class Config:
        from_attributes = True