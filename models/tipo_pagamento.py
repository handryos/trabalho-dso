from enum import Enum


class TipoPagamento(Enum):
    DINHEIRO = "dinheiro"
    PIX = "pix"
    CARTAO = "cartao"
    
    def __str__(self):
        return self.value
    
    @classmethod
    def from_string(cls, value: str):
        value_lower = value.lower().strip()
        for tipo in cls:
            if tipo.value == value_lower:
                return tipo
        raise ValueError(f"Tipo de pagamento inválido: {value}")
    
    def get_display_name(self) -> str:
        display_names = {
            TipoPagamento.DINHEIRO: "Dinheiro",
            TipoPagamento.PIX: "PIX",
            TipoPagamento.CARTAO: "Cartão de Crédito"
        }
        return display_names.get(self, self.value)
