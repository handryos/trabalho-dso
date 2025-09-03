from abc import ABC, abstractmethod
from typing import Any, List


class BaseView(ABC):
    @abstractmethod
    def exibir_menu(self) -> int:
        pass
    
    @abstractmethod
    def exibir_lista(self, items: List[Any], titulo: str = ""):
        pass
    
    @abstractmethod
    def exibir_mensagem(self, mensagem: str, tipo: str = "info"):
        pass
    
    def exibir_erro(self, erro: str):
        self.exibir_mensagem(f"ERRO: {erro}", "erro")
    
    def exibir_sucesso(self, mensagem: str):
        self.exibir_mensagem(f"SUCESSO: {mensagem}", "sucesso")
    
    def solicitar_entrada(self, prompt: str, tipo: type = str, obrigatorio: bool = True) -> Any:
        while True:
            try:
                entrada = input(f"{prompt}: ")
                
                if not obrigatorio and not entrada.strip():
                    return None
                
                if obrigatorio and not entrada.strip():
                    self.exibir_erro("Este campo é obrigatório.")
                    continue
                
                if tipo == str:
                    return entrada
                elif tipo == int:
                    return int(entrada)
                elif tipo == float:
                    return float(entrada)
                else:
                    return tipo(entrada)
            except ValueError:
                self.exibir_erro(f"Valor inválido. Esperado: {tipo.__name__}")
    
    def confirmar_acao(self, mensagem: str) -> bool:
        resposta = input(f"{mensagem} (s/n): ").lower().strip()
        return resposta in ['s', 'sim', 'y', 'yes']
