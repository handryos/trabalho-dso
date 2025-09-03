from datetime import date
from typing import List, Optional
import uuid
from .pessoa import Pessoa
from .destino import Destino
from .destino_viagem import DestinoViagem
from .transporte import Transporte
from exceptions import DataInvalidaException, ValorInvalidoException


class Viagem:
    def __init__(self, titulo: str, data_inicio: date, data_fim: date, 
                 valor_total: float, destinos: List[DestinoViagem]):
        if data_fim <= data_inicio:
            raise DataInvalidaException(f"Data de fim ({data_fim}) deve ser posterior à data de início ({data_inicio})")
        
        if valor_total < 0:
            raise ValorInvalidoException(valor_total, "Valor total da viagem não pode ser negativo")
        
        if not destinos:
            raise ValueError("Viagem deve ter pelo menos um destino")
        
        self._id = str(uuid.uuid4())
        self._titulo = titulo
        self._data_inicio = data_inicio
        self._data_fim = data_fim
        self._valor_total = valor_total
        self._destinos = sorted(destinos.copy(), key=lambda d: d.ordem)
        
        self._transportes: List[Transporte] = []
        self._participantes: List[Pessoa] = []
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def titulo(self) -> str:
        return self._titulo
    
    @property
    def data_inicio(self) -> date:
        return self._data_inicio
    
    @property
    def data_fim(self) -> date:
        return self._data_fim
    
    @property
    def valor_total(self) -> float:
        return self._valor_total
    
    @valor_total.setter
    def valor_total(self, valor: float):
        if valor < 0:
            raise ValorInvalidoException(valor, "Valor total da viagem não pode ser negativo")
        self._valor_total = valor
    
    @property
    def destinos(self) -> List[DestinoViagem]:
        return self._destinos.copy()
    
    @property
    def transportes(self) -> List[Transporte]:
        return self._transportes.copy()
    
    @property
    def participantes(self) -> List[Pessoa]:
        return self._participantes.copy()
    
    def adicionar_participante(self, pessoa: Pessoa):
        if pessoa not in self._participantes:
            self._participantes.append(pessoa)
    
    def remover_participante(self, pessoa: Pessoa):
        if pessoa in self._participantes:
            self._participantes.remove(pessoa)
    
    def adicionar_transporte(self, transporte: Transporte):
        self._transportes.append(transporte)
    
    def adicionar_destino(self, destino_viagem: DestinoViagem):
        if destino_viagem not in self._destinos:
            self._destinos.append(destino_viagem)
            self._destinos.sort(key=lambda d: d.ordem)
    
    def duracao_dias(self) -> int:
        return (self._data_fim - self._data_inicio).days
    
    def valor_por_pessoa(self) -> Optional[float]:
        if len(self._participantes) == 0:
            return None
        return self._valor_total / len(self._participantes)
    
    def esta_no_prazo_pagamento(self, data_atual: date) -> bool:
        return data_atual <= self._data_inicio
    
    def __str__(self) -> str:
        destinos_str = " → ".join([d.nome_completo() for d in self._destinos])
        return f"{self._titulo} - {destinos_str} ({self._data_inicio} a {self._data_fim})"
    
    def __repr__(self) -> str:
        return f"Viagem(id={self._id}, titulo={self._titulo}, participantes={len(self._participantes)})"
