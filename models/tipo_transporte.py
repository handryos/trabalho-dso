import uuid
from .empresa import Empresa


class TipoTransporte:
    def __init__(self, tipo: str, empresa: Empresa):
        if not tipo.strip():
            raise ValueError("Tipo de transporte é obrigatório")
        if not isinstance(empresa, Empresa):
            raise ValueError("Empresa deve ser uma instância válida da classe Empresa")
            
        self._id = str(uuid.uuid4())
        self._tipo = tipo.strip()
        self._empresa = empresa 
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def tipo(self) -> str:
        return self._tipo
    
    @tipo.setter
    def tipo(self, valor: str):
        if not valor.strip():
            raise ValueError("Tipo de transporte é obrigatório")
        self._tipo = valor.strip()
    
    @property
    def empresa(self) -> Empresa:
        return self._empresa
    
    @empresa.setter
    def empresa(self, valor: Empresa):
        if not isinstance(valor, Empresa):
            raise ValueError("Empresa deve ser uma instância válida da classe Empresa")
        self._empresa = valor
    
    def __str__(self) -> str:
        return f"{self._tipo} - {self._empresa.nome}"
    
    def __repr__(self) -> str:
        return f"TipoTransporte(id={self._id}, tipo={self._tipo}, empresa={self._empresa.nome})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, TipoTransporte):
            return False
        return (self._tipo.lower() == other._tipo.lower() and 
                self._empresa == other._empresa)
