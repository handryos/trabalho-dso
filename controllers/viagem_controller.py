from typing import Dict, Any, List, Optional
from datetime import date
from controllers.base_controller import BaseController
from controllers.pessoa_controller import PessoaController
from controllers.destino_controller import DestinoController
from models.viagem import Viagem
from models.destino_viagem import DestinoViagem
from models.pagamento import Pagamento
from exceptions import (
    ViagemNaoEncontradaException, 
    DataInvalidaException,
    PessoaNaoEncontradaException,
    DestinaNaoEncontradoException,
    CampoObrigatorioException
)


class ViagemController(BaseController[Viagem]):
    def __init__(self, pessoa_controller: PessoaController, destino_controller: DestinoController):
        super().__init__()
        self._viagens: Dict[str, Viagem] = {}
        self._pagamentos: Dict[str, List[Pagamento]] = {} 
        self._pessoa_controller = pessoa_controller
        self._destino_controller = destino_controller
    
    def criar(self, dados: Dict[str, Any]) -> str:
        try:
            destinos_viagem = []
            destino_ids = dados['destino_ids']
            
            ordens = dados.get('ordens', list(range(1, len(destino_ids) + 1)))
            
            if len(ordens) != len(destino_ids):
                raise ValueError("Número de ordens deve corresponder ao número de destinos")
            
            for i, destino_id in enumerate(destino_ids):
                destino = self._destino_controller.buscar_por_id_obrigatorio(destino_id)
                destino_viagem = DestinoViagem(destino, ordens[i])
                destinos_viagem.append(destino_viagem)
            
            viagem = Viagem(
                titulo=dados['titulo'],
                data_inicio=dados['data_inicio'],
                data_fim=dados['data_fim'],
                valor_total=dados['valor_total'],
                destinos=destinos_viagem
            )
            
            self._viagens[viagem.id] = viagem
            self._pagamentos[viagem.id] = []
            
            return viagem.id
            
        except KeyError as e:
            raise CampoObrigatorioException(str(e))
        except (DataInvalidaException, ValueError):
            raise 
    
    def buscar_por_id(self, viagem_id: str) -> Optional[Viagem]:
        return self._viagens.get(viagem_id)
    
    def buscar_por_id_obrigatorio(self, viagem_id: str) -> Viagem:
        viagem = self.buscar_por_id(viagem_id)
        if viagem is None:
            raise ViagemNaoEncontradaException(viagem_id)
        return viagem
    
    def listar_todos(self) -> List[Viagem]:
        return list(self._viagens.values())
    
    def atualizar(self, viagem_id: str, dados: Dict[str, Any]) -> bool:
        viagem = self.buscar_por_id(viagem_id)
        if viagem is None:
            return False
        
        if 'valor_total' in dados:
            viagem.valor_total = dados['valor_total']
        
        return True
    
    def deletar(self, viagem_id: str) -> bool:
        if viagem_id in self._viagens:
            del self._viagens[viagem_id]
            if viagem_id in self._pagamentos:
                del self._pagamentos[viagem_id]
            return True
        return False
    
    def adicionar_participante(self, viagem_id: str, pessoa_id: str) -> bool:
        try:
            viagem = self.buscar_por_id_obrigatorio(viagem_id)
            pessoa = self._pessoa_controller.buscar_por_id_obrigatorio(pessoa_id)
            
            viagem.adicionar_participante(pessoa)
            return True
            
        except (ViagemNaoEncontradaException, PessoaNaoEncontradaException):
            return False
    
    def remover_participante(self, viagem_id: str, pessoa_id: str) -> bool:
        try:
            viagem = self.buscar_por_id_obrigatorio(viagem_id)
            pessoa = self._pessoa_controller.buscar_por_id_obrigatorio(pessoa_id)
            
            viagem.remover_participante(pessoa)
            return True
            
        except (ViagemNaoEncontradaException, PessoaNaoEncontradaException):
            return False
    
    def adicionar_pagamento(self, viagem_id: str, pagamento: Pagamento):
        if viagem_id not in self._pagamentos:
            self._pagamentos[viagem_id] = []
        self._pagamentos[viagem_id].append(pagamento)
    
    def calcular_total_pago(self, viagem_id: str) -> float:
        if viagem_id not in self._pagamentos:
            return 0.0
        
        return sum(p.valor for p in self._pagamentos[viagem_id])
    
    def calcular_saldo_devedor(self, viagem_id: str) -> float:
        viagem = self.buscar_por_id(viagem_id)
        if viagem is None:
            return 0.0
        
        total_pago = self.calcular_total_pago(viagem_id)
        return viagem.valor_total - total_pago
    
    def listar_viagens_em_andamento(self, data_atual: date) -> List[Viagem]:
        return [v for v in self._viagens.values() if v.data_fim >= data_atual]
    
    def reordenar_destinos(self, viagem_id: str, nova_ordem: Dict[str, int]) -> bool:
        """
        Reordena os destinos de uma viagem.
        
        Args:
            viagem_id: ID da viagem
            nova_ordem: Dicionário {destino_id: nova_ordem}
        
        Returns:
            True se a reordenação foi bem-sucedida
        """
        try:
            viagem = self.buscar_por_id_obrigatorio(viagem_id)
            
            for destino_viagem in viagem.destinos:
                destino_id = destino_viagem.destino.id
                if destino_id in nova_ordem:
                    destino_viagem.ordem = nova_ordem[destino_id]
            
            viagem._destinos.sort(key=lambda d: d.ordem)
            
            return True
            
        except (ViagemNaoEncontradaException, ValueError):
            return False
