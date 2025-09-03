from datetime import date
from typing import Optional, Dict, Any
import uuid
from .tipo_pagamento import TipoPagamento
from .strategy_pagamento import StrategyPagamento
from .strategies_pagamento import (
    StrategyPagamentoDinheiro,
    StrategyPagamentoPix,
    StrategyPagamentoCartao
)
from exceptions import ValorInvalidoException, PagamentoInvalidoException


class Pagamento:
    def __init__(self, data: date, valor: float, pessoa_id: str, viagem_id: str, 
                 tipo: TipoPagamento, dados_pagamento: Optional[Dict[str, Any]] = None):
        
        if valor <= 0:
            raise ValorInvalidoException(valor, "Valor deve ser positivo")
        
        self._id = str(uuid.uuid4())
        self._data = data
        self._valor = valor
        self._pessoa_id = pessoa_id
        self._viagem_id = viagem_id
        self._tipo = tipo
        self._dados_pagamento = dados_pagamento or {}
        
        self._dados_pagamento['valor'] = valor
        
        self._strategy = self._get_strategy(tipo)
        
        if not self._strategy.validar(self._dados_pagamento):
            raise PagamentoInvalidoException("Dados de pagamento inválidos")
    
    def _get_strategy(self, tipo: TipoPagamento) -> StrategyPagamento:
        strategies = {
            TipoPagamento.DINHEIRO: StrategyPagamentoDinheiro(),
            TipoPagamento.PIX: StrategyPagamentoPix(),
            TipoPagamento.CARTAO: StrategyPagamentoCartao()
        }
        
        strategy = strategies.get(tipo)
        if not strategy:
            raise PagamentoInvalidoException(f"Tipo de pagamento não suportado: {tipo}")
        
        return strategy
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def data(self) -> date:
        return self._data
    
    @property
    def valor(self) -> float:
        return self._valor
    
    @property
    def pessoa_id(self) -> str:
        return self._pessoa_id
    
    @property
    def viagem_id(self) -> str:
        return self._viagem_id
    
    @property
    def tipo(self) -> TipoPagamento:
        return self._tipo
    
    def processar_pagamento(self) -> bool:
        return self._strategy.processar(self._dados_pagamento)
    
    def get_detalhes_pagamento(self) -> str:
        return self._strategy.get_detalhes(self._dados_pagamento)
    
    def __str__(self) -> str:
        return f"Pagamento de R$ {self._valor:.2f} em {self._data} - {self.get_detalhes_pagamento()}"
    
    def __repr__(self) -> str:
        return f"Pagamento(id={self._id}, valor={self._valor}, tipo={self._tipo.value}, data={self._data})"
