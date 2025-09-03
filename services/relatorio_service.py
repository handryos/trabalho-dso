from typing import List, Dict, Tuple
from collections import Counter
from controllers.viagem_controller import ViagemController
from controllers.destino_controller import DestinoController
from controllers.pessoa_controller import PessoaController
from controllers.pagamento_controller import PagamentoController
from models.viagem import Viagem
from models.destino import Destino
from models.passeio import Passeio


class RelatorioService:
    def __init__(self, viagem_controller: ViagemController, 
                 destino_controller: DestinoController,
                 pessoa_controller: PessoaController,
                 pagamento_controller: PagamentoController):
        self._viagem_controller = viagem_controller
        self._destino_controller = destino_controller
        self._pessoa_controller = pessoa_controller
        self._pagamento_controller = pagamento_controller
        self._passeios: List[Passeio] = [] 
    
    def adicionar_passeio(self, passeio: Passeio):
        self._passeios.append(passeio)
    
    def destinos_mais_populares(self, limite: int = 10) -> List[Tuple[Destino, int]]:
        contador_destinos = Counter()
        
        for viagem in self._viagem_controller.listar_todos():
            for destino in viagem.destinos:
                contador_destinos[destino.id] += 1
        
        destinos_populares = []
        for destino_id, count in contador_destinos.most_common(limite):
            destino = self._destino_controller.buscar_por_id(destino_id)
            if destino:
                destinos_populares.append((destino, count))
        
        return destinos_populares
    
    def destinos_mais_caros(self, limite: int = 10) -> List[Tuple[Destino, float]]:
        valores_por_destino: Dict[str, List[float]] = {}
        
        for viagem in self._viagem_controller.listar_todos():
            valor_por_destino = viagem.valor_total / len(viagem.destinos) if viagem.destinos else 0
            for destino in viagem.destinos:
                if destino.id not in valores_por_destino:
                    valores_por_destino[destino.id] = []
                valores_por_destino[destino.id].append(valor_por_destino)
        
        medias_destinos = []
        for destino_id, valores in valores_por_destino.items():
            destino = self._destino_controller.buscar_por_id(destino_id)
            if destino:
                valor_medio = sum(valores) / len(valores)
                medias_destinos.append((destino, valor_medio))
        
        medias_destinos.sort(key=lambda x: x[1], reverse=True)
        return medias_destinos[:limite]
    
    def destinos_mais_baratos(self, limite: int = 10) -> List[Tuple[Destino, float]]:
        destinos_caros = self.destinos_mais_caros(len(self._destino_controller.listar_todos()))
        destinos_baratos = list(reversed(destinos_caros))
        return destinos_baratos[:limite]
    
    def passeios_mais_populares(self, limite: int = 10) -> List[Tuple[str, int]]:
        contador_passeios = Counter()
        
        for passeio in self._passeios:
            contador_passeios[passeio.atracao_turistica] += 1
        
        return contador_passeios.most_common(limite)
    
    def passeios_mais_caros(self, limite: int = 10) -> List[Tuple[Passeio, float]]:
        passeios_ordenados = sorted(self._passeios, key=lambda p: p.valor, reverse=True)
        return [(p, p.valor) for p in passeios_ordenados[:limite]]
    
    def passeios_mais_baratos(self, limite: int = 10) -> List[Tuple[Passeio, float]]:
        passeios_ordenados = sorted(self._passeios, key=lambda p: p.valor)
        return [(p, p.valor) for p in passeios_ordenados[:limite]]
    
    def relatorio_financeiro_viagem(self, viagem_id: str) -> Dict[str, float]:
        try:
            viagem = self._viagem_controller.buscar_por_id_obrigatorio(viagem_id)
            total_pago = self._pagamento_controller.calcular_total_por_viagem(viagem_id)
            saldo_devedor = viagem.valor_total - total_pago
            
            return {
                'valor_total': viagem.valor_total,
                'total_pago': total_pago,
                'saldo_devedor': saldo_devedor,
                'percentual_pago': (total_pago / viagem.valor_total) * 100 if viagem.valor_total > 0 else 0
            }
        except Exception:
            return {
                'valor_total': 0.0,
                'total_pago': 0.0,
                'saldo_devedor': 0.0,
                'percentual_pago': 0.0
            }
