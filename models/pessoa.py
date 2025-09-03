from datetime import datetime, date
import uuid
from exceptions import IdadeInsuficienteException


class Pessoa:
    def __init__(self, nome: str, celular: str, identificacao: str, 
                 data_nascimento: date, tipo_identificacao: str = "cpf"):
 
        self._id = str(uuid.uuid4())
        self._nome = nome
        self._celular = celular
        self._identificacao = identificacao
        self._data_nascimento = data_nascimento
        self._tipo_identificacao = tipo_identificacao
        
        if not self._tem_idade_minima():
            idade = self.calcular_idade()
            raise IdadeInsuficienteException(idade)
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def celular(self) -> str:
        return self._celular
    
    @property
    def identificacao(self) -> str:
        return self._identificacao
    
    @property
    def data_nascimento(self) -> date:
        return self._data_nascimento
    
    @property
    def tipo_identificacao(self) -> str:
        return self._tipo_identificacao
    
    def calcular_idade(self) -> int:
        hoje = date.today()
        idade = hoje.year - self._data_nascimento.year
        
        if hoje < date(hoje.year, self._data_nascimento.month, self._data_nascimento.day):
            idade -= 1
            
        return idade
    
    def _tem_idade_minima(self) -> bool:
        return self.calcular_idade() >= 18
    
    def __str__(self) -> str:
        return f"{self._nome} ({self._tipo_identificacao}: {self._identificacao})"
    
    def __repr__(self) -> str:
        return f"Pessoa(id={self._id}, nome={self._nome}, idade={self.calcular_idade()})"
