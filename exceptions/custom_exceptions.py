class SistemaViagensException(Exception):

    pass

class IdadeInsuficienteException(SistemaViagensException):

    def __init__(self, idade: int):
        super().__init__(f"Idade insuficiente: {idade} anos. Necessário 18 anos completos.")

class PagamentoInvalidoException(SistemaViagensException):

    def __init__(self, motivo: str = "Dados de pagamento inválidos"):
        super().__init__(f"Pagamento inválido: {motivo}")

class DataInvalidaException(SistemaViagensException):

    def __init__(self, motivo: str = "Data inválida fornecida"):
        super().__init__(f"Data inválida: {motivo}")

class ViagemNaoEncontradaException(SistemaViagensException):

    def __init__(self, viagem_id: str):
        super().__init__(f"Viagem com ID {viagem_id} não encontrada.")

class PessoaNaoEncontradaException(SistemaViagensException):

    def __init__(self, pessoa_id: str):
        super().__init__(f"Pessoa com ID {pessoa_id} não encontrada.")

class DestinaNaoEncontradoException(SistemaViagensException):

    def __init__(self, destino_id: str):
        super().__init__(f"Destino com ID {destino_id} não encontrado.")

class TransporteNaoEncontradoException(SistemaViagensException):

    def __init__(self, transporte_id: str):
        super().__init__(f"Transporte com ID {transporte_id} não encontrado.")

class EmpresaNaoEncontradaException(SistemaViagensException):

    def __init__(self, empresa_id: str):
        super().__init__(f"Empresa com ID {empresa_id} não encontrada.")

class PasseioNaoEncontradoException(SistemaViagensException):

    def __init__(self, passeio_id: str):
        super().__init__(f"Passeio com ID {passeio_id} não encontrado.")

class ValorInvalidoException(SistemaViagensException):

    def __init__(self, valor: float, motivo: str = ""):
        if motivo:
            super().__init__(f"Valor inválido: {valor}. {motivo}")
        else:
            super().__init__(f"Valor inválido: {valor}")

class CampoObrigatorioException(SistemaViagensException):

    def __init__(self, campo: str):
        super().__init__(f"Campo obrigatório ausente: {campo}")

class CapacidadeExcedidaException(SistemaViagensException):

    def __init__(self, capacidade_maxima: int, tentativa: int):
        super().__init__(f"Capacidade excedida. Máximo: {capacidade_maxima}, Tentativa: {tentativa}")

class PagamentoVencidoException(SistemaViagensException):

    def __init__(self, data_limite: str):
        super().__init__(f"Pagamento não pode ser realizado após {data_limite}")

class HorarioInvalidoException(SistemaViagensException):

    def __init__(self, motivo: str = "Horário inválido"):
        super().__init__(f"Horário inválido: {motivo}")

class PagamentoExcedeSaldoException(SistemaViagensException):

    def __init__(self, valor_pagamento: float, saldo_devedor: float):
        super().__init__(f"Pagamento de R$ {valor_pagamento:.2f} excede o saldo devedor de R$ {saldo_devedor:.2f}")
