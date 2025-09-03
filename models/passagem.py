import uuid
from typing import Optional
from datetime import date, time
from .tipo_transporte import TipoTransporte
from .empresa import Empresa
from exceptions import ValorInvalidoException


class Passagem:
    def __init__(self, data_viagem: date, origem: str, destino: str, 
                 tipo_transporte: TipoTransporte, viagem_id: str,
                 horario_partida: Optional[time] = None,
                 horario_chegada: Optional[time] = None,
                 valor: Optional[float] = None,
                 compra_realizada: bool = False,
                 responsavel_compra_id: Optional[str] = None,
                 numero_assento: Optional[str] = None,
                 codigo_reserva: Optional[str] = None):
        
        if valor is not None and valor < 0:
            raise ValorInvalidoException(valor, "Valor da passagem não pode ser negativo")
        
        self._id = str(uuid.uuid4())
        self._data_viagem = data_viagem
        self._origem = origem.strip()
        self._destino = destino.strip()
        self._tipo_transporte = tipo_transporte
        self._viagem_id = viagem_id
        self._horario_partida = horario_partida
        self._horario_chegada = horario_chegada
        self._valor = valor
        self._compra_realizada = compra_realizada
        self._responsavel_compra_id = responsavel_compra_id
        self._numero_assento = numero_assento
        self._codigo_reserva = codigo_reserva
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def data_viagem(self) -> date:
        return self._data_viagem
    
    @data_viagem.setter
    def data_viagem(self, valor: date):
        self._data_viagem = valor
    
    @property
    def origem(self) -> str:
        return self._origem
    
    @origem.setter
    def origem(self, valor: str):
        self._origem = valor.strip()
    
    @property
    def destino(self) -> str:
        return self._destino
    
    @destino.setter
    def destino(self, valor: str):
        self._destino = valor.strip()
    
    @property
    def tipo_transporte(self) -> TipoTransporte:
        return self._tipo_transporte
    
    @property
    def empresa(self) -> Empresa:
        return self._tipo_transporte.empresa
    
    @property
    def viagem_id(self) -> str:
        return self._viagem_id
    
    @property
    def horario_partida(self) -> Optional[time]:
        return self._horario_partida
    
    @horario_partida.setter
    def horario_partida(self, valor: Optional[time]):
        self._horario_partida = valor
    
    @property
    def horario_chegada(self) -> Optional[time]:
        return self._horario_chegada
    
    @horario_chegada.setter
    def horario_chegada(self, valor: Optional[time]):
        self._horario_chegada = valor
    
    @property
    def valor(self) -> Optional[float]:
        return self._valor
    
    @valor.setter
    def valor(self, valor: Optional[float]):
        if valor is not None and valor < 0:
            raise ValorInvalidoException(valor, "Valor da passagem não pode ser negativo")
        self._valor = valor
    
    @property
    def compra_realizada(self) -> bool:
        return self._compra_realizada
    
    @compra_realizada.setter
    def compra_realizada(self, valor: bool):
        self._compra_realizada = valor
    
    @property
    def responsavel_compra_id(self) -> Optional[str]:
        return self._responsavel_compra_id
    
    @responsavel_compra_id.setter
    def responsavel_compra_id(self, valor: Optional[str]):
        self._responsavel_compra_id = valor
    
    @property
    def numero_assento(self) -> Optional[str]:
        return self._numero_assento
    
    @numero_assento.setter
    def numero_assento(self, valor: Optional[str]):
        self._numero_assento = valor
    
    @property
    def codigo_reserva(self) -> Optional[str]:
        return self._codigo_reserva
    
    @codigo_reserva.setter
    def codigo_reserva(self, valor: Optional[str]):
        self._codigo_reserva = valor
    
    def marcar_como_comprada(self, responsavel_id: str, codigo_reserva: Optional[str] = None,
                           numero_assento: Optional[str] = None):

        self._compra_realizada = True
        self._responsavel_compra_id = responsavel_id
        if codigo_reserva:
            self._codigo_reserva = codigo_reserva
        if numero_assento:
            self._numero_assento = numero_assento
    
    def cancelar_compra(self):

        self._compra_realizada = False
        self._responsavel_compra_id = None
        self._codigo_reserva = None
        self._numero_assento = None
    
    def get_duracao_estimada(self) -> Optional[str]:

        if self._horario_partida and self._horario_chegada:
            if self._horario_chegada >= self._horario_partida:
                delta = time(
                    self._horario_chegada.hour - self._horario_partida.hour,
                    self._horario_chegada.minute - self._horario_partida.minute
                )
            else:
                horas = (24 - self._horario_partida.hour) + self._horario_chegada.hour
                minutos = self._horario_chegada.minute - self._horario_partida.minute
                if minutos < 0:
                    horas -= 1
                    minutos += 60
                delta = time(horas, minutos)
            
            return f"{delta.hour}h{delta.minute:02d}min"
        return None
    
    def __str__(self) -> str:
        status = "✅ Comprada" if self._compra_realizada else "⏳ Pendente"
        empresa = self.empresa.nome
        
        info = f"{self._origem} → {self._destino} ({self._data_viagem})"
        info += f" - {self._tipo_transporte.tipo} ({empresa}) - {status}"
        
        if self._horario_partida:
            info += f" - Partida: {self._horario_partida}"
        
        return info
    
    def __repr__(self) -> str:
        return f"Passagem(id={self._id}, origem={self._origem}, destino={self._destino}, comprada={self._compra_realizada})"
