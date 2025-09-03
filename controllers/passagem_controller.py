from typing import Dict, Any, List, Optional
from datetime import date, time
from controllers.base_controller import BaseController
from controllers.empresa_controller import EmpresaController
from controllers.pessoa_controller import PessoaController
from controllers.viagem_controller import ViagemController
from models.passagem import Passagem
from models.tipo_transporte import TipoTransporte
from exceptions import (
    CampoObrigatorioException,
    PessoaNaoEncontradaException,
    ViagemNaoEncontradaException,
    EmpresaNaoEncontradaException,
    ValorInvalidoException
)


class PassagemController(BaseController[Passagem]):

    
    def __init__(self, empresa_controller: EmpresaController, 
                 pessoa_controller: PessoaController,
                 viagem_controller: ViagemController):
        super().__init__()
        self._passagens: Dict[str, Passagem] = {}
        self._tipos_transporte: Dict[str, TipoTransporte] = {}
        self._empresa_controller = empresa_controller
        self._pessoa_controller = pessoa_controller
        self._viagem_controller = viagem_controller
    
    def cadastrar_tipo_transporte(self, dados: Dict[str, Any]) -> str:

        try:
            empresa = self._empresa_controller.buscar_por_id_obrigatorio(dados['empresa_id'])
            
            tipo = TipoTransporte(
                tipo=dados['tipo'],
                empresa=empresa
            )
            
            self._tipos_transporte[tipo.id] = tipo
            return tipo.id
            
        except KeyError as e:
            raise CampoObrigatorioException(str(e))
    
    def criar(self, dados: Dict[str, Any]) -> str:

        try:
            self._viagem_controller.buscar_por_id_obrigatorio(dados['viagem_id'])
            
            tipo_transporte = self._tipos_transporte.get(dados['tipo_transporte_id'])
            if not tipo_transporte:
                raise ValueError(f"Tipo de transporte não encontrado: {dados['tipo_transporte_id']}")
            
            if dados.get('responsavel_compra_id'):
                self._pessoa_controller.buscar_por_id_obrigatorio(dados['responsavel_compra_id'])
            
            horario_partida = None
            horario_chegada = None
            
            if dados.get('horario_partida'):
                horario_partida = time.fromisoformat(dados['horario_partida'])
            
            if dados.get('horario_chegada'):
                horario_chegada = time.fromisoformat(dados['horario_chegada'])
            
            passagem = Passagem(
                data_viagem=dados['data_viagem'],
                origem=dados['origem'],
                destino=dados['destino'],
                tipo_transporte=tipo_transporte,
                viagem_id=dados['viagem_id'],
                horario_partida=horario_partida,
                horario_chegada=horario_chegada,
                valor=dados.get('valor'),
                compra_realizada=dados.get('compra_realizada', False),
                responsavel_compra_id=dados.get('responsavel_compra_id'),
                numero_assento=dados.get('numero_assento'),
                codigo_reserva=dados.get('codigo_reserva')
            )
            
            self._passagens[passagem.id] = passagem
            return passagem.id
            
        except KeyError as e:
            raise CampoObrigatorioException(str(e))
        except (ViagemNaoEncontradaException, PessoaNaoEncontradaException, 
                EmpresaNaoEncontradaException, ValorInvalidoException):
            raise
        except ValueError:
            raise
    
    def buscar_por_id(self, passagem_id: str) -> Optional[Passagem]:

        return self._passagens.get(passagem_id)
    
    def buscar_por_id_obrigatorio(self, passagem_id: str) -> Passagem:

        passagem = self.buscar_por_id(passagem_id)
        if passagem is None:
            raise ValueError(f"Passagem com ID {passagem_id} não encontrada")
        return passagem
    
    def listar_todos(self) -> List[Passagem]:

        return list(self._passagens.values())
    
    def listar_por_viagem(self, viagem_id: str) -> List[Passagem]:

        return [p for p in self._passagens.values() if p.viagem_id == viagem_id]
    
    def listar_por_responsavel(self, responsavel_id: str) -> List[Passagem]:

        return [p for p in self._passagens.values() 
                if p.responsavel_compra_id == responsavel_id]
    
    def listar_pendentes(self, viagem_id: Optional[str] = None) -> List[Passagem]:

        passagens = self._passagens.values()
        if viagem_id:
            passagens = [p for p in passagens if p.viagem_id == viagem_id]
        return [p for p in passagens if not p.compra_realizada]
    
    def listar_compradas(self, viagem_id: Optional[str] = None) -> List[Passagem]:

        passagens = self._passagens.values()
        if viagem_id:
            passagens = [p for p in passagens if p.viagem_id == viagem_id]
        return [p for p in passagens if p.compra_realizada]
    
    def marcar_como_comprada(self, passagem_id: str, responsavel_id: str,
                           codigo_reserva: Optional[str] = None,
                           numero_assento: Optional[str] = None) -> bool:

        try:
            passagem = self.buscar_por_id_obrigatorio(passagem_id)
            self._pessoa_controller.buscar_por_id_obrigatorio(responsavel_id)
            
            passagem.marcar_como_comprada(responsavel_id, codigo_reserva, numero_assento)
            return True
            
        except (ValueError, PessoaNaoEncontradaException):
            return False
    
    def cancelar_compra(self, passagem_id: str) -> bool:

        passagem = self.buscar_por_id(passagem_id)
        if passagem:
            passagem.cancelar_compra()
            return True
        return False
    
    def atualizar(self, passagem_id: str, dados: Dict[str, Any]) -> bool:

        passagem = self.buscar_por_id(passagem_id)
        if not passagem:
            return False
        
        try:
            if 'data_viagem' in dados:
                passagem.data_viagem = dados['data_viagem']
            
            if 'origem' in dados:
                passagem.origem = dados['origem']
            
            if 'destino' in dados:
                passagem.destino = dados['destino']
            
            if 'horario_partida' in dados:
                if dados['horario_partida']:
                    passagem.horario_partida = time.fromisoformat(dados['horario_partida'])
                else:
                    passagem.horario_partida = None
            
            if 'horario_chegada' in dados:
                if dados['horario_chegada']:
                    passagem.horario_chegada = time.fromisoformat(dados['horario_chegada'])
                else:
                    passagem.horario_chegada = None
            
            if 'valor' in dados:
                passagem.valor = dados['valor']
            
            if 'numero_assento' in dados:
                passagem.numero_assento = dados['numero_assento']
            
            if 'codigo_reserva' in dados:
                passagem.codigo_reserva = dados['codigo_reserva']
            
            return True
            
        except (ValueError, ValorInvalidoException):
            return False
    
    def deletar(self, passagem_id: str) -> bool:

        if passagem_id in self._passagens:
            del self._passagens[passagem_id]
            return True
        return False
    
    def listar_tipos_transporte(self) -> List[TipoTransporte]:

        return list(self._tipos_transporte.values())
    
    def calcular_valor_total_viagem(self, viagem_id: str) -> float:

        passagens = self.listar_por_viagem(viagem_id)
        return sum(p.valor for p in passagens if p.valor is not None)
    
    def gerar_relatorio_passagens(self, viagem_id: str) -> Dict[str, Any]:

        passagens = self.listar_por_viagem(viagem_id)
        compradas = [p for p in passagens if p.compra_realizada]
        pendentes = [p for p in passagens if not p.compra_realizada]
        
        valor_total = sum(p.valor for p in passagens if p.valor is not None)
        valor_compradas = sum(p.valor for p in compradas if p.valor is not None)
        
        responsaveis = {}
        for passagem in compradas:
            resp_id = passagem.responsavel_compra_id
            if resp_id not in responsaveis:
                responsaveis[resp_id] = []
            responsaveis[resp_id].append(passagem)
        
        return {
            'total_passagens': len(passagens),
            'passagens_compradas': len(compradas),
            'passagens_pendentes': len(pendentes),
            'valor_total': valor_total,
            'valor_compradas': valor_compradas,
            'percentual_compradas': (len(compradas) / len(passagens) * 100) if passagens else 0,
            'responsaveis_compra': responsaveis,
            'passagens_pendentes_lista': pendentes
        }
