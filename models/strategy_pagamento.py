from abc import ABC, abstractmethod
from typing import Dict, Any
from exceptions import PagamentoInvalidoException


class StrategyPagamento(ABC):
    @abstractmethod
    def validar(self, dados: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def processar(self, dados: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def get_detalhes(self, dados: Dict[str, Any]) -> str:
        pass
    
    @abstractmethod
    def get_nome_tipo(self) -> str:
        pass
