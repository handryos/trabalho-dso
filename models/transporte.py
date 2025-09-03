import uuid
from typing import Optional
from datetime import date
from .tipo_transporte import TipoTransporte


class Transporte:
    def __init__(self, data: date, origem: str, destino: str, 
                 tipo_transporte: TipoTransporte, compra_realizada: bool = False,
                 responsavel_compra: Optional[str] = None):
        self._id = str(uuid.uuid4())
        self._data = data
        self._origem = origem
        self._destino = destino
        self._tipo_transporte = tipo_transporte 
        self._compra_realizada = compra_realizada
        self._responsavel_compra = responsavel_compra
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def data(self) -> date:
        return self._data
    
    @property
    def origem(self) -> str:
        return self._origem
    
    @property
    def destino(self) -> str:
        return self._destino
    
    @property
    def tipo_transporte(self) -> TipoTransporte:
        return self._tipo_transporte
    
    @property
    def compra_realizada(self) -> bool:
        return self._compra_realizada
    
    @compra_realizada.setter
    def compra_realizada(self, valor: bool):
        self._compra_realizada = valor
    
    @property
    def responsavel_compra(self) -> Optional[str]:
        return self._responsavel_compra
    
    @responsavel_compra.setter
    def responsavel_compra(self, valor: str):
        self._responsavel_compra = valor
    
    def __str__(self) -> str:
        status = "Comprado" if self._compra_realizada else "Pendente"
        return f"{self._origem} → {self._destino} ({self._data}) - {status}"
    
    def __repr__(self) -> str:
        return f"Transporte(id={self._id}, origem={self._origem}, destino={self._destino}, data={self._data})"
