from .destino import Destino

class DestinoViagem:
    def __init__(self, destino: Destino, ordem: int):
        if ordem < 1:
            raise ValueError("Ordem deve ser um número positivo (começando em 1)")
        
        self._destino = destino
        self._ordem = ordem
    
    @property
    def id(self) -> str:
        return self._destino.id
    
    @property
    def destino(self) -> Destino:
        return self._destino
    
    @property
    def ordem(self) -> int:
        return self._ordem
    
    @ordem.setter
    def ordem(self, nova_ordem: int):
        if nova_ordem < 1:
            raise ValueError("Ordem deve ser um número positivo (começando em 1)")
        self._ordem = nova_ordem
    
    def nome_completo(self) -> str:
        return self._destino.nome_completo()
    
    def __str__(self) -> str:
        return f"{self._ordem}º - {self._destino.nome_completo()}"
    
    def __repr__(self) -> str:
        return f"DestinoViagem(destino={self._destino}, ordem={self._ordem})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, DestinoViagem):
            return False
        return self._destino == other._destino and self._ordem == other._ordem
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, DestinoViagem):
            return NotImplemented
        return self._ordem < other._ordem
