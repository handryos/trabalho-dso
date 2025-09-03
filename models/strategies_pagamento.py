from typing import Dict, Any
from .strategy_pagamento import StrategyPagamento
from exceptions import PagamentoInvalidoException


class StrategyPagamentoDinheiro(StrategyPagamento):
    def validar(self, dados: Dict[str, Any]) -> bool:
        valor = dados.get('valor', 0)
        
        if valor <= 0:
            return False
        
        if valor > 10000:
            raise PagamentoInvalidoException(f"Valor muito alto para pagamento em dinheiro: R$ {valor:.2f}")
        
        return True
    
    def processar(self, dados: Dict[str, Any]) -> bool:
        if self.validar(dados):
            return True
        return False
    
    def get_detalhes(self, dados: Dict[str, Any]) -> str:
        return "Dinheiro"
    
    def get_nome_tipo(self) -> str:
        return "dinheiro"


class StrategyPagamentoPix(StrategyPagamento):
    def validar(self, dados: Dict[str, Any]) -> bool:
        valor = dados.get('valor', 0)
        cpf_pagador = dados.get('cpf_pagador', '')
        
        if valor <= 0:
            return False
        
        if not cpf_pagador or not cpf_pagador.strip():
            raise PagamentoInvalidoException("CPF do pagador é obrigatório para pagamentos PIX")
        
        cpf_numeros = ''.join(filter(str.isdigit, cpf_pagador))
        if len(cpf_numeros) != 11:
            raise PagamentoInvalidoException("CPF deve ter 11 dígitos")
        
        return True
    
    def processar(self, dados: Dict[str, Any]) -> bool:
        if self.validar(dados):
            return True
        return False
    
    def get_detalhes(self, dados: Dict[str, Any]) -> str:
        cpf_pagador = dados.get('cpf_pagador', '')
        return f"PIX - CPF: {cpf_pagador}"
    
    def get_nome_tipo(self) -> str:
        return "pix"


class StrategyPagamentoCartao(StrategyPagamento):
    def validar(self, dados: Dict[str, Any]) -> bool:
        valor = dados.get('valor', 0)
        numero_cartao = dados.get('numero_cartao', '')
        bandeira = dados.get('bandeira', '')
        
        if valor <= 0:
            return False
        
        if not numero_cartao or not numero_cartao.strip():
            raise PagamentoInvalidoException("Número do cartão é obrigatório")
        
        if not bandeira or not bandeira.strip():
            raise PagamentoInvalidoException("Bandeira do cartão é obrigatória")
        
        cartao_numeros = ''.join(filter(str.isdigit, numero_cartao))
        if len(cartao_numeros) < 13 or len(cartao_numeros) > 19:
            raise PagamentoInvalidoException("Número do cartão inválido")
        
        return True
    
    def processar(self, dados: Dict[str, Any]) -> bool:
        if self.validar(dados):
            return True
        return False
    
    def get_detalhes(self, dados: Dict[str, Any]) -> str:
        numero_cartao = dados.get('numero_cartao', '')
        bandeira = dados.get('bandeira', '')
        
        if len(numero_cartao) >= 4:
            numero_mascarado = "*" * (len(numero_cartao) - 4) + numero_cartao[-4:]
        else:
            numero_mascarado = "****"
        
        return f"Cartão {bandeira} - {numero_mascarado}"
    
    def get_nome_tipo(self) -> str:
        return "cartao"
