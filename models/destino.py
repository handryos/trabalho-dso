import uuid
from typing import Optional


class Destino:
    def __init__(self, cidade: str, pais: str, descricao: Optional[str] = None):
        self._id = str(uuid.uuid4())
        self._cidade = cidade
        self._pais = pais
        self._descricao = descricao
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def cidade(self) -> str:
        return self._cidade
    
    @property
    def pais(self) -> str:
        return self._pais
    
    @property
    def descricao(self) -> Optional[str]:
        return self._descricao
    
    @descricao.setter
    def descricao(self, valor: str):
        self._descricao = valor
    
    def nome_completo(self) -> str:
        return f"{self._cidade}, {self._pais}"
    
    def __str__(self) -> str:
        return self.nome_completo()
    
    def __repr__(self) -> str:
        return f"Destino(id={self._id}, cidade={self._cidade}, pais={self._pais})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Destino):
            return False
        return self._cidade == other._cidade and self._pais == other._pais
