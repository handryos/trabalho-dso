from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, TypeVar, Generic
import uuid

T = TypeVar('T')

class BaseController(ABC, Generic[T]):
    def __init__(self):
        self._dados: Dict[str, T] = {}
    
    @abstractmethod
    def criar(self, dados: Dict[str, Any]) -> str:
        pass
    
    @abstractmethod
    def buscar_por_id(self, entity_id: str) -> Optional[T]:
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[T]:
        pass
    
    def atualizar(self, entity_id: str, dados: Dict[str, Any]) -> bool:
        return False
    
    def deletar(self, entity_id: str) -> bool:
        return False
    
    def _gerar_id(self) -> str:
        return str(uuid.uuid4())
