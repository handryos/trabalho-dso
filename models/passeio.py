from datetime import time, date
from typing import Optional
import uuid
from .destino import Destino
from .pessoa import Pessoa
from exceptions import ValorInvalidoException, HorarioInvalidoException


class Passeio:
    def __init__(self, cidade: str, atracao_turistica: str, horario_inicio: time,
                 horario_fim: time, valor: float, pessoa: Pessoa, data_passeio: date,
                 destino: Optional[Destino] = None):
        if valor < 0:
            raise ValorInvalidoException(valor, "Valor do passeio não pode ser negativo")
        
        if horario_fim <= horario_inicio:
            raise HorarioInvalidoException("Horário de fim deve ser posterior ao horário de início")
        
        self._id = str(uuid.uuid4())
        self._cidade = cidade
        self._atracao_turistica = atracao_turistica
        self._horario_inicio = horario_inicio
        self._horario_fim = horario_fim
        self._valor = valor
        self._pessoa = pessoa 
        self._data_passeio = data_passeio
        self._destino = destino  
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def cidade(self) -> str:
        return self._cidade
    
    @property
    def atracao_turistica(self) -> str:
        return self._atracao_turistica
    
    @property
    def horario_inicio(self) -> time:
        return self._horario_inicio
    
    @property
    def horario_fim(self) -> time:
        return self._horario_fim
    
    @property
    def valor(self) -> float:
        return self._valor
    
    @valor.setter
    def valor(self, novo_valor: float):
        if novo_valor < 0:
            raise ValorInvalidoException(novo_valor, "Valor do passeio não pode ser negativo")
        self._valor = novo_valor
    
    @property
    def pessoa(self) -> Pessoa:
        return self._pessoa
    
    @property
    def data_passeio(self) -> date:
        return self._data_passeio
    
    @property
    def destino(self) -> Optional[Destino]:
        return self._destino
    
    @destino.setter
    def destino(self, novo_destino: Destino):
        self._destino = novo_destino
    
    def duracao_horas(self) -> float:
        inicio_minutos = self._horario_inicio.hour * 60 + self._horario_inicio.minute
        fim_minutos = self._horario_fim.hour * 60 + self._horario_fim.minute
        return (fim_minutos - inicio_minutos) / 60
    
    def valor_por_hora(self) -> float:
        duracao = self.duracao_horas()
        return self._valor / duracao if duracao > 0 else 0
    
    def __str__(self) -> str:
        return (f"{self._atracao_turistica} em {self._cidade} "
                f"({self._horario_inicio} às {self._horario_fim}) - "
                f"R$ {self._valor:.2f}")
    
    def __repr__(self) -> str:
        return (f"Passeio(id={self._id}, atracao={self._atracao_turistica}, "
                f"cidade={self._cidade}, valor={self._valor})")
