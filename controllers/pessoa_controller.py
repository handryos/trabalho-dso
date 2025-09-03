from typing import Dict, Any, List, Optional
from datetime import date
from controllers.base_controller import BaseController
from models.pessoa import Pessoa
from exceptions import PessoaNaoEncontradaException, IdadeInsuficienteException, CampoObrigatorioException


class PessoaController(BaseController[Pessoa]):
    def __init__(self):
        super().__init__()
        self._pessoas: Dict[str, Pessoa] = {}
    
    def criar(self, dados: Dict[str, Any]) -> str:
        try:
            pessoa = Pessoa(
                nome=dados['nome'],
                celular=dados['celular'],
                identificacao=dados['identificacao'],
                data_nascimento=dados['data_nascimento'],
                tipo_identificacao=dados.get('tipo_identificacao', 'cpf')
            )
            
            self._pessoas[pessoa.id] = pessoa
            return pessoa.id
            
        except KeyError as e:
            raise CampoObrigatorioException(str(e))
        except IdadeInsuficienteException:
            raise 
    
    def buscar_por_id(self, pessoa_id: str) -> Optional[Pessoa]:
        return self._pessoas.get(pessoa_id)
    
    def buscar_por_id_obrigatorio(self, pessoa_id: str) -> Pessoa:
        pessoa = self.buscar_por_id(pessoa_id)
        if pessoa is None:
            raise PessoaNaoEncontradaException(pessoa_id)
        return pessoa
    
    def listar_todos(self) -> List[Pessoa]:
        return list(self._pessoas.values())
    
    def atualizar(self, pessoa_id: str, dados: Dict[str, Any]) -> bool:
        pessoa = self.buscar_por_id(pessoa_id)
        if pessoa is None:
            return False
        
        if 'celular' in dados:
            pessoa._celular = dados['celular']
        
        return True
    
    def deletar(self, pessoa_id: str) -> bool:
        if pessoa_id in self._pessoas:
            del self._pessoas[pessoa_id]
            return True
        return False
    
    def buscar_por_identificacao(self, identificacao: str) -> Optional[Pessoa]:
        for pessoa in self._pessoas.values():
            if pessoa.identificacao == identificacao:
                return pessoa
        return None
    
    def listar_maiores_idade(self) -> List[Pessoa]:
        return [p for p in self._pessoas.values() if p.calcular_idade() >= 18]
