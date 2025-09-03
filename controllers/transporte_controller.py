from typing import Dict, Any, List, Optional
from controllers.base_controller import BaseController
from controllers.empresa_controller import EmpresaController
from models.transporte import TipoTransporte, Transporte
from exceptions import (
    EmpresaNaoEncontradaException,
    TransporteNaoEncontradoException,
    CampoObrigatorioException
)


class TransporteController(BaseController[Transporte]):
    def __init__(self, empresa_controller: EmpresaController):
        super().__init__()
        self._tipos: Dict[str, TipoTransporte] = {}
        self._transportes: Dict[str, Transporte] = {}
        self._empresa_controller = empresa_controller
    
    def criar_tipo(self, dados: Dict[str, Any]) -> str:
        try:
            empresa = self._empresa_controller.buscar_por_id_obrigatorio(dados['empresa_id'])
            
            tipo = TipoTransporte(
                tipo=dados['tipo'],
                empresa=empresa
            )
            
            self._tipos[tipo.id] = tipo
            return tipo.id
            
        except KeyError as e:
            raise CampoObrigatorioException(str(e))
    
    def criar(self, dados: Dict[str, Any]) -> str:
        try:
            tipo_transporte = self._tipos.get(dados['tipo_transporte_id'])
            if tipo_transporte is None:
                raise TransporteNaoEncontradoException(dados['tipo_transporte_id'])
            
            transporte = Transporte(
                data=dados['data'],
                origem=dados['origem'],
                destino=dados['destino'],
                tipo_transporte=tipo_transporte,
                compra_realizada=dados.get('compra_realizada', False),
                responsavel_compra=dados.get('responsavel_compra')
            )
            
            self._transportes[transporte.id] = transporte
            return transporte.id
            
        except KeyError as e:
            raise CampoObrigatorioException(str(e))
    
    def buscar_por_id(self, transporte_id: str) -> Optional[Transporte]:
        return self._transportes.get(transporte_id)
    
    def buscar_por_id_obrigatorio(self, transporte_id: str) -> Transporte:
        transporte = self.buscar_por_id(transporte_id)
        if transporte is None:
            raise TransporteNaoEncontradoException(transporte_id)
        return transporte
    
    def listar_todos(self) -> List[Transporte]:
        return list(self._transportes.values())
    
    def listar_tipos(self) -> List[TipoTransporte]:
        return list(self._tipos.values())
    
    def atualizar(self, transporte_id: str, dados: Dict[str, Any]) -> bool:
        transporte = self.buscar_por_id(transporte_id)
        if transporte is None:
            return False
        
        if 'compra_realizada' in dados:
            transporte.compra_realizada = dados['compra_realizada']
        
        if 'responsavel_compra' in dados:
            transporte.responsavel_compra = dados['responsavel_compra']
        
        return True
    
    def deletar(self, transporte_id: str) -> bool:
        if transporte_id in self._transportes:
            del self._transportes[transporte_id]
            return True
        return False
