from typing import Dict, Any, List, Optional
from datetime import date
from controllers.base_controller import BaseController
from controllers.pessoa_controller import PessoaController
from models.pagamento import Pagamento
from models.tipo_pagamento import TipoPagamento
from exceptions import (
    PagamentoInvalidoException,
    ValorInvalidoException,
    CampoObrigatorioException,
    PagamentoExcedeSaldoException
)


class PagamentoController(BaseController[Pagamento]):
    def __init__(self, pessoa_controller: PessoaController, viagem_controller=None):
        super().__init__()
        self._pagamentos: Dict[str, Pagamento] = {}
        self._pessoa_controller = pessoa_controller
        self._viagem_controller = viagem_controller
    
    def criar(self, dados: Dict[str, Any]) -> str:
        try:
            self._pessoa_controller.buscar_por_id_obrigatorio(dados['pessoa_id'])
            
            if self._viagem_controller and 'viagem_id' in dados:
                saldo_devedor = self._viagem_controller.calcular_saldo_devedor(dados['viagem_id'])
                valor_pagamento = dados['valor']
                
                if valor_pagamento > saldo_devedor:
                    raise PagamentoExcedeSaldoException(valor_pagamento, saldo_devedor)
            
            tipo = dados['tipo'].lower()
            tipo_enum = TipoPagamento.from_string(tipo)
            
            dados_pagamento = {}
            
            if tipo_enum == TipoPagamento.PIX:
                dados_pagamento['cpf_pagador'] = dados['cpf_pagador']
            elif tipo_enum == TipoPagamento.CARTAO:
                dados_pagamento['numero_cartao'] = dados['numero_cartao']
                dados_pagamento['bandeira'] = dados['bandeira']
            
            pagamento = Pagamento(
                data=dados['data'],
                valor=dados['valor'],
                pessoa_id=dados['pessoa_id'],
                viagem_id=dados['viagem_id'],
                tipo=tipo_enum,
                dados_pagamento=dados_pagamento
            )
            
            if pagamento.processar_pagamento():
                self._pagamentos[pagamento.id] = pagamento
                return pagamento.id
            else:
                raise PagamentoInvalidoException("Falha ao processar pagamento")
            
        except KeyError as e:
            raise CampoObrigatorioException(str(e))
        except (PagamentoInvalidoException, ValorInvalidoException, PagamentoExcedeSaldoException):
            raise 
    
    def buscar_por_id(self, pagamento_id: str) -> Optional[Pagamento]:
        return self._pagamentos.get(pagamento_id)
    
    def listar_todos(self) -> List[Pagamento]:
        return list(self._pagamentos.values())
    
    def deletar(self, pagamento_id: str) -> bool:
        if pagamento_id in self._pagamentos:
            del self._pagamentos[pagamento_id]
            return True
        return False
    
    def listar_por_viagem(self, viagem_id: str) -> List[Pagamento]:
        return [p for p in self._pagamentos.values() if p.viagem_id == viagem_id]
    
    def listar_por_pessoa(self, pessoa_id: str) -> List[Pagamento]:
        return [p for p in self._pagamentos.values() if p.pessoa_id == pessoa_id]
    
    def calcular_total_por_viagem(self, viagem_id: str) -> float:
        pagamentos = self.listar_por_viagem(viagem_id)
        return sum(p.valor for p in pagamentos)
    
    def calcular_total_por_pessoa(self, pessoa_id: str) -> float:
        pagamentos = self.listar_por_pessoa(pessoa_id)
        return sum(p.valor for p in pagamentos)
