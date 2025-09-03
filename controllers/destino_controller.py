from typing import Dict, Any, List, Optional
from controllers.base_controller import BaseController
from models.destino import Destino
from exceptions import DestinaNaoEncontradoException, CampoObrigatorioException


class DestinoController(BaseController[Destino]):
    def __init__(self):
        super().__init__()
        self._destinos: Dict[str, Destino] = {}
    
    def criar(self, dados: Dict[str, Any]) -> str:
        try:
            destino = Destino(
                cidade=dados['cidade'],
                pais=dados['pais'],
                descricao=dados.get('descricao')
            )
            
            self._destinos[destino.id] = destino
            return destino.id
            
        except KeyError as e:
            raise CampoObrigatorioException(str(e))
    
    def buscar_por_id(self, destino_id: str) -> Optional[Destino]:
        return self._destinos.get(destino_id)
    
    def buscar_por_id_obrigatorio(self, destino_id: str) -> Destino:
        destino = self.buscar_por_id(destino_id)
        if destino is None:
            raise DestinaNaoEncontradoException(destino_id)
        return destino
    
    def listar_todos(self) -> List[Destino]:
        return list(self._destinos.values())
    
    def atualizar(self, destino_id: str, dados: Dict[str, Any]) -> bool:
        destino = self.buscar_por_id(destino_id)
        if destino is None:
            return False
        
        if 'descricao' in dados:
            destino.descricao = dados['descricao']
        
        return True
    
    def deletar(self, destino_id: str) -> bool:
        if destino_id in self._destinos:
            del self._destinos[destino_id]
            return True
        return False
    
    def buscar_por_cidade(self, cidade: str) -> List[Destino]:
        return [d for d in self._destinos.values() 
                if d.cidade.lower() == cidade.lower()]
    
    def buscar_por_pais(self, pais: str) -> List[Destino]:
        return [d for d in self._destinos.values() 
                if d.pais.lower() == pais.lower()]
