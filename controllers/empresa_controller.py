from typing import Dict, Any, List, Optional
from controllers.base_controller import BaseController
from models.empresa import Empresa
from exceptions import (
    EmpresaNaoEncontradaException,
    CampoObrigatorioException
)


class EmpresaController(BaseController[Empresa]):

    
    def __init__(self):
        super().__init__()
        self._empresas: Dict[str, Empresa] = {}
    
    def criar(self, dados: Dict[str, Any]) -> str:

        try:
            empresa = Empresa(
                nome=dados['nome'],
                cnpj=dados['cnpj'],
                telefone=dados['telefone']
            )
            
            for emp in self._empresas.values():
                if emp.cnpj == empresa.cnpj:
                    raise ValueError(f"Já existe uma empresa cadastrada com o CNPJ {empresa.cnpj}")
            
            self._empresas[empresa.id] = empresa
            return empresa.id
            
        except KeyError as e:
            raise CampoObrigatorioException(str(e))
        except ValueError:
            raise
    
    def buscar_por_id(self, empresa_id: str) -> Optional[Empresa]:

        return self._empresas.get(empresa_id)
    
    def buscar_por_id_obrigatorio(self, empresa_id: str) -> Empresa:

        empresa = self.buscar_por_id(empresa_id)
        if empresa is None:
            raise EmpresaNaoEncontradaException(empresa_id)
        return empresa
    
    def buscar_por_cnpj(self, cnpj: str) -> Optional[Empresa]:

        for empresa in self._empresas.values():
            if empresa.cnpj == cnpj:
                return empresa
        return None
    
    def buscar_por_nome(self, nome: str) -> List[Empresa]:

        nome_lower = nome.lower()
        return [emp for emp in self._empresas.values() 
                if nome_lower in emp.nome.lower()]
    
    def listar_todos(self) -> List[Empresa]:

        return list(self._empresas.values())
    
    def atualizar(self, empresa_id: str, dados: Dict[str, Any]) -> bool:

        empresa = self.buscar_por_id(empresa_id)
        if empresa is None:
            return False
        
        try:
            if 'nome' in dados:
                empresa.nome = dados['nome']
            
            if 'cnpj' in dados:
                novo_cnpj = dados['cnpj'].strip()
                for emp_id, emp in self._empresas.items():
                    if emp_id != empresa_id and emp.cnpj == novo_cnpj:
                        raise ValueError(f"Já existe uma empresa cadastrada com o CNPJ {novo_cnpj}")
                empresa.cnpj = novo_cnpj
            
            if 'telefone' in dados:
                empresa.telefone = dados['telefone']
            
            return True
            
        except ValueError:
            raise
    
    def deletar(self, empresa_id: str) -> bool:

        if empresa_id in self._empresas:
            del self._empresas[empresa_id]
            return True
        return False
    
    def contar_total(self) -> int:

        return len(self._empresas)
