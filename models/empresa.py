import uuid
from typing import Optional


class Empresa:
    def __init__(self, nome: str, cnpj: str, telefone: str):
        if not nome.strip():
            raise ValueError("Nome da empresa é obrigatório")
        if not cnpj.strip():
            raise ValueError("CNPJ é obrigatório")
        if not telefone.strip():
            raise ValueError("Telefone é obrigatório")
            
        self._id = str(uuid.uuid4())
        self._nome = nome.strip()
        self._cnpj = cnpj.strip()
        self._telefone = telefone.strip()
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, valor: str):
        if not valor.strip():
            raise ValueError("Nome da empresa é obrigatório")
        self._nome = valor.strip()
    
    @property
    def cnpj(self) -> str:
        return self._cnpj
    
    @cnpj.setter
    def cnpj(self, valor: str):
        if not valor.strip():
            raise ValueError("CNPJ é obrigatório")
        self._cnpj = valor.strip()
    
    @property
    def telefone(self) -> str:
        return self._telefone
    
    @telefone.setter
    def telefone(self, valor: str):
        if not valor.strip():
            raise ValueError("Telefone é obrigatório")
        self._telefone = valor.strip()
    
    def __str__(self) -> str:
        return f"{self._nome} (CNPJ: {self._cnpj})"
    
    def __repr__(self) -> str:
        return f"Empresa(id={self._id}, nome={self._nome}, cnpj={self._cnpj})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Empresa):
            return False
        return self._cnpj == other._cnpj 
