from typing import Dict, Any, List, Optional
from datetime import date, time
from controllers.base_controller import BaseController
from controllers.pessoa_controller import PessoaController
from controllers.destino_controller import DestinoController
from models.passeio import Passeio
from exceptions import (
    PasseioNaoEncontradoException,
    PessoaNaoEncontradaException,
    DestinaNaoEncontradoException,
    ValorInvalidoException
)


class PasseioController(BaseController[Passeio]):
    def __init__(self, pessoa_controller: PessoaController, destino_controller: DestinoController):
        super().__init__()
        self._passeios: Dict[str, Passeio] = {}
        self._pessoa_controller = pessoa_controller
        self._destino_controller = destino_controller
    
    def criar(self, dados: Dict[str, Any]) -> str:
        try:
            pessoa = self._pessoa_controller.buscar_por_id_obrigatorio(dados['pessoa_id'])
            
            destino = None
            if 'destino_id' in dados and dados['destino_id']:
                destino = self._destino_controller.buscar_por_id_obrigatorio(dados['destino_id'])
            
            passeio = Passeio(
                cidade=dados['cidade'],
                atracao_turistica=dados['atracao_turistica'],
                horario_inicio=dados['horario_inicio'],
                horario_fim=dados['horario_fim'],
                valor=dados['valor'],
                pessoa=pessoa,
                data_passeio=dados['data_passeio'],
                destino=destino
            )
            
            self._passeios[passeio.id] = passeio
            return passeio.id
            
        except KeyError as e:
            raise ValueError(f"Campo obrigatório ausente: {e}")
        except (PessoaNaoEncontradaException, DestinaNaoEncontradoException, ValorInvalidoException):
            raise
    
    def buscar_por_id(self, passeio_id: str) -> Optional[Passeio]:
        return self._passeios.get(passeio_id)
    
    def buscar_por_id_obrigatorio(self, passeio_id: str) -> Passeio:
        passeio = self.buscar_por_id(passeio_id)
        if passeio is None:
            raise PasseioNaoEncontradoException(passeio_id)
        return passeio
    
    def listar_todos(self) -> List[Passeio]:
        return list(self._passeios.values())
    
    def atualizar(self, passeio_id: str, dados: Dict[str, Any]) -> bool:
        passeio = self.buscar_por_id(passeio_id)
        if passeio is None:
            return False
        
        try:
            if 'valor' in dados:
                passeio.valor = dados['valor']
            
            if 'destino_id' in dados:
                if dados['destino_id']:
                    destino = self._destino_controller.buscar_por_id_obrigatorio(dados['destino_id'])
                    passeio.destino = destino
                else:
                    passeio.destino = None
            
            return True
        except (DestinaNaoEncontradoException, ValorInvalidoException):
            return False
    
    def deletar(self, passeio_id: str) -> bool:
        if passeio_id in self._passeios:
            del self._passeios[passeio_id]
            return True
        return False
    
    def listar_por_pessoa(self, pessoa_id: str) -> List[Passeio]:
        return [p for p in self._passeios.values() if p.pessoa.id == pessoa_id]
    
    def listar_por_cidade(self, cidade: str) -> List[Passeio]:
        return [p for p in self._passeios.values() if p.cidade.lower() == cidade.lower()]
    
    def listar_por_atracao(self, atracao: str) -> List[Passeio]:
        return [p for p in self._passeios.values() if atracao.lower() in p.atracao_turistica.lower()]
