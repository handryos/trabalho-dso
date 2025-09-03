from datetime import date, time
from typing import List, Any
from views.base_view import BaseView
from controllers.pessoa_controller import PessoaController
from controllers.destino_controller import DestinoController
from controllers.viagem_controller import ViagemController
from controllers.pagamento_controller import PagamentoController
from controllers.passeio_controller import PasseioController
from controllers.transporte_controller import TransporteController
from controllers.empresa_controller import EmpresaController
from controllers.passagem_controller import PassagemController
from utils.mocked_data import MockedData
from controllers.passagem_controller import PassagemController
from services.relatorio_service import RelatorioService
from models.passeio import Passeio
from exceptions import *


class SistemaViagensView(BaseView):
    def __init__(self):
        self.pessoa_controller = PessoaController()
        self.destino_controller = DestinoController()
        self.empresa_controller = EmpresaController()
        self.viagem_controller = ViagemController(self.pessoa_controller, self.destino_controller)
        self.pagamento_controller = PagamentoController(self.pessoa_controller, self.viagem_controller)
        self.passeio_controller = PasseioController(self.pessoa_controller, self.destino_controller)
        self.transporte_controller = TransporteController(self.empresa_controller)
        self.passagem_controller = PassagemController(self.empresa_controller, self.pessoa_controller, self.viagem_controller)
        self.relatorio_service = RelatorioService(
            self.viagem_controller, 
            self.destino_controller,
            self.pessoa_controller,
            self.pagamento_controller
        )
        
        self.cadastrar_dados_iniciais()
    
    def exibir_menu(self) -> int:
        print("\n" + "="*50)
        print("    SISTEMA DE GERENCIAMENTO DE VIAGENS")
        print("="*50)
        print("1. Gerenciar Pessoas")
        print("2. Gerenciar Destinos")
        print("3. Gerenciar Viagens")
        print("4. Gerenciar Pagamentos")
        print("5. Gerenciar Passeios")
        print("6. Gerenciar Transportes")
        print("7. Gerenciar Passagens")
        print("8. Relatórios")
        print("0. Sair")
        print("-"*50)
        
        return self.solicitar_entrada("Selecione uma opção", int)
    
    def exibir_lista(self, items: List[Any], titulo: str = ""):
        if titulo:
            print(f"\n{titulo}")
            print("-" * len(titulo))
        
        if not items:
            print("Nenhum item encontrado.")
            return
        
        for i, item in enumerate(items, 1):
            print(f"{i:2d}. {item}")
    
    def exibir_mensagem(self, mensagem: str, tipo: str = "info"):
        if tipo == "erro":
            print(f"\n❌ {mensagem}")
        elif tipo == "sucesso":
            print(f"\n✅ {mensagem}")
        else:
            print(f"\nℹ️  {mensagem}")
    
    def executar(self):
        print("Bem-vindo ao Sistema de Gerenciamento de Viagens!")
        
        while True:
            try:
                opcao = self.exibir_menu()
                
                if opcao == 0:
                    self.exibir_mensagem("Obrigado por usar o sistema!")
                    break
                elif opcao == 1:
                    self.menu_pessoas()
                elif opcao == 2:
                    self.menu_destinos()
                elif opcao == 3:
                    self.menu_viagens()
                elif opcao == 4:
                    self.menu_pagamentos()
                elif opcao == 5:
                    self.menu_passeios()
                elif opcao == 6:
                    self.menu_transportes()
                elif opcao == 7:
                    self.menu_passagens()
                elif opcao == 8:
                    self.menu_relatorios()
                else:
                    self.exibir_erro("Opção inválida!")
                    
            except KeyboardInterrupt:
                self.exibir_mensagem("\nOperação cancelada pelo usuário.")
                break
            except Exception as e:
                self.exibir_erro(f"Erro inesperado: {str(e)}")
    
    def menu_pessoas(self):
        while True:
            print("\n=== GERENCIAR PESSOAS ===")
            print("1. Cadastrar Pessoa")
            print("2. Listar Pessoas")
            print("3. Buscar Pessoa")
            print("4. Atualizar Pessoa")
            print("5. Deletar Pessoa")
            print("0. Voltar")
            
            opcao = self.solicitar_entrada("Opção", int)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.cadastrar_pessoa()
            elif opcao == 2:
                self.listar_pessoas()
            elif opcao == 3:
                self.buscar_pessoa()
            elif opcao == 4:
                self.atualizar_pessoa()
            elif opcao == 5:
                self.deletar_pessoa()
    
    def cadastrar_pessoa(self):
        try:
            print("\n=== CADASTRAR PESSOA ===")
            nome = self.solicitar_entrada("Nome completo")
            celular = self.solicitar_entrada("Celular")
            identificacao = self.solicitar_entrada("CPF ou Passaporte")
            tipo_id = self.solicitar_entrada("Tipo (cpf/passaporte)", str).lower()
            
            print("Data de nascimento:")
            dia = self.solicitar_entrada("Dia", int)
            mes = self.solicitar_entrada("Mês", int) 
            ano = self.solicitar_entrada("Ano", int)
            data_nascimento = date(ano, mes, dia)
            
            dados = {
                'nome': nome,
                'celular': celular,
                'identificacao': identificacao,
                'data_nascimento': data_nascimento,
                'tipo_identificacao': tipo_id
            }
            
            pessoa_id = self.pessoa_controller.criar(dados)
            self.exibir_sucesso(f"Pessoa cadastrada com ID: {pessoa_id}")
            
        except IdadeInsuficienteException as e:
            self.exibir_erro(str(e))
        except ValueError as e:
            self.exibir_erro(f"Dados inválidos: {str(e)}")
        except Exception as e:
            self.exibir_erro(f"Erro ao cadastrar pessoa: {str(e)}")
    
    def listar_pessoas(self):
        pessoas = self.pessoa_controller.listar_todos()
        self.exibir_lista(pessoas, "PESSOAS CADASTRADAS")
    
    def buscar_pessoa(self):

        identificacao = self.solicitar_entrada("CPF ou Passaporte")
        pessoa = self.pessoa_controller.buscar_por_identificacao(identificacao)
        
        if pessoa:
            print(f"\nPessoa encontrada:")
            print(f"Nome: {pessoa.nome}")
            print(f"Idade: {pessoa.calcular_idade()} anos")
            print(f"Celular: {pessoa.celular}")
        else:
            self.exibir_mensagem("Pessoa não encontrada.")
    
    def atualizar_pessoa(self):
        pessoas = self.pessoa_controller.listar_todos()
        
        if not pessoas:
            self.exibir_mensagem("Nenhuma pessoa cadastrada.")
            return
        
        print("\nPessoas disponíveis:")
        for i, pessoa in enumerate(pessoas, 1):
            print(f"{i}. {pessoa}")
        
        try:
            indice = self.solicitar_entrada("Selecione a pessoa para atualizar", int) - 1
            if not (0 <= indice < len(pessoas)):
                self.exibir_erro("Índice inválido")
                return
            
            pessoa = pessoas[indice]
            print(f"Dados atuais: {pessoa}")
            
            dados = {}
            self.exibir_mensagem("Deixe em branco para manter o valor atual")
            
            novo_celular = input(f"Novo celular (atual: {pessoa.celular}): ").strip()
            if novo_celular:
                dados['celular'] = novo_celular
            
            if self.pessoa_controller.atualizar(pessoa.id, dados):
                self.exibir_sucesso("Pessoa atualizada com sucesso")
            else:
                self.exibir_erro("Erro ao atualizar pessoa")
                
        except ValueError:
            self.exibir_erro("Valor inválido")
    
    def deletar_pessoa(self):
        pessoas = self.pessoa_controller.listar_todos()
        
        if not pessoas:
            self.exibir_mensagem("Nenhuma pessoa cadastrada.")
            return
        
        print("\nPessoas disponíveis:")
        for i, pessoa in enumerate(pessoas, 1):
            print(f"{i}. {pessoa}")
        
        try:
            indice = self.solicitar_entrada("Selecione a pessoa para deletar", int) - 1
            if not (0 <= indice < len(pessoas)):
                self.exibir_erro("Índice inválido")
                return
            
            pessoa = pessoas[indice]
            
            if self.confirmar_acao(f"Confirma a exclusão de '{pessoa.nome}'?"):
                if self.pessoa_controller.deletar(pessoa.id):
                    self.exibir_sucesso("Pessoa deletada com sucesso")
                else:
                    self.exibir_erro("Erro ao deletar pessoa")
                    
        except ValueError:
            self.exibir_erro("Valor inválido")
    
    def menu_destinos(self):

        while True:
            print("\n=== GERENCIAR DESTINOS ===")
            print("1. Cadastrar Destino")
            print("2. Listar Destinos")
            print("0. Voltar")
            
            opcao = self.solicitar_entrada("Opção", int)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.cadastrar_destino()
            elif opcao == 2:
                self.listar_destinos()
    
    def cadastrar_destino(self):

        try:
            print("\n=== CADASTRAR DESTINO ===")
            cidade = self.solicitar_entrada("Cidade")
            pais = self.solicitar_entrada("País")
            descricao = self.solicitar_entrada("Descrição (opcional)")
            
            dados = {
                'cidade': cidade,
                'pais': pais,
                'descricao': descricao if descricao.strip() else None
            }
            
            destino_id = self.destino_controller.criar(dados)
            self.exibir_sucesso(f"Destino cadastrado com ID: {destino_id}")
            
        except Exception as e:
            self.exibir_erro(f"Erro ao cadastrar destino: {str(e)}")
    
    def listar_destinos(self):

        destinos = self.destino_controller.listar_todos()
        self.exibir_lista(destinos, "DESTINOS CADASTRADOS")
    
    def menu_transportes(self):

        while True:
            print("\n=== GERENCIAR TRANSPORTES ===")
            print("1. Gerenciar Empresas de Transporte")
            print("2. Gerenciar Tipos de Transporte")
            print("3. Gerenciar Trechos de Viagem")
            print("0. Voltar")
            
            opcao = self.solicitar_entrada("Opção", int)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.menu_empresas_transporte()
            elif opcao == 2:
                self.menu_tipos_transporte()
            elif opcao == 3:
                self.menu_trechos_viagem()
            else:
                self.exibir_erro("Opção inválida!")
    
    def menu_empresas_transporte(self):

        while True:
            print("\n=== GERENCIAR EMPRESAS DE TRANSPORTE ===")
            print("1. Cadastrar Empresa")
            print("2. Listar Empresas")
            print("0. Voltar")
            
            opcao = self.solicitar_entrada("Opção", int)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.cadastrar_empresa_transporte()
            elif opcao == 2:
                self.listar_empresas_transporte()
            else:
                self.exibir_erro("Opção inválida!")
    
    def cadastrar_empresa_transporte(self):

        try:
            print("\n=== CADASTRAR EMPRESA DE TRANSPORTE ===")
            
            nome = self.solicitar_entrada("Nome da empresa")
            cnpj = self.solicitar_entrada("CNPJ")
            telefone = self.solicitar_entrada("Telefone")
            
            dados = {
                'nome': nome,
                'cnpj': cnpj,
                'telefone': telefone
            }
            
            empresa_id = self.empresa_controller.criar(dados)
            self.exibir_sucesso(f"Empresa cadastrada com sucesso! ID: {empresa_id}")
            
        except Exception as e:
            self.exibir_erro(f"Erro ao cadastrar empresa: {str(e)}")
    
    def listar_empresas_transporte(self):

        empresas = self.empresa_controller.listar_todos()
        if not empresas:
            self.exibir_mensagem("Nenhuma empresa cadastrada.")
            return
        
        print("\n=== EMPRESAS DE TRANSPORTE ===")
        for empresa in empresas:
            print(f"ID: {empresa.id}")
            print(f"Nome: {empresa.nome}")
            print(f"CNPJ: {empresa.cnpj}")
            print(f"Telefone: {empresa.telefone}")
            print("-" * 40)
    
    def menu_tipos_transporte(self):

        while True:
            print("\n=== GERENCIAR TIPOS DE TRANSPORTE ===")
            print("1. Cadastrar Tipo de Transporte")
            print("2. Listar Tipos de Transporte")
            print("0. Voltar")
            
            opcao = self.solicitar_entrada("Opção", int)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.cadastrar_tipo_transporte()
            elif opcao == 2:
                self.listar_tipos_transporte()
            else:
                self.exibir_erro("Opção inválida!")
    
    def cadastrar_tipo_transporte(self):

        try:
            print("\n=== CADASTRAR TIPO DE TRANSPORTE ===")
            
            empresas = self.empresa_controller.listar_todos()
            if not empresas:
                self.exibir_erro("Nenhuma empresa cadastrada. Cadastre uma empresa primeiro.")
                return
            
            print("\nEmpresas disponíveis:")
            for i, empresa in enumerate(empresas, 1):
                print(f"{i}. {empresa.nome} (CNPJ: {empresa.cnpj})")
            
            escolha = self.solicitar_entrada("Escolha uma empresa (número)", int) - 1
            if escolha < 0 or escolha >= len(empresas):
                self.exibir_erro("Empresa inválida!")
                return
            
            empresa_selecionada = empresas[escolha]
            tipo = self.solicitar_entrada("Tipo de transporte (ex: Avião, Ônibus, Trem)")
            
            dados = {
                'tipo': tipo,
                'empresa_id': empresa_selecionada.id
            }
            
            tipo_id = self.transporte_controller.criar_tipo(dados)
            self.exibir_sucesso(f"Tipo de transporte cadastrado com sucesso! ID: {tipo_id}")
            
        except Exception as e:
            self.exibir_erro(f"Erro ao cadastrar tipo de transporte: {str(e)}")
    
    def listar_tipos_transporte(self):

        tipos = self.transporte_controller.listar_tipos()
        if not tipos:
            self.exibir_mensagem("Nenhum tipo de transporte cadastrado.")
            return
        
        print("\n=== TIPOS DE TRANSPORTE ===")
        for tipo in tipos:
            print(f"ID: {tipo.id}")
            print(f"Tipo: {tipo.tipo}")
            print(f"Empresa: {tipo.empresa.nome}")
            print("-" * 40)
    
    def menu_trechos_viagem(self):

        while True:
            print("\n=== GERENCIAR TRECHOS DE VIAGEM ===")
            print("1. Cadastrar Trecho")
            print("2. Listar Trechos")
            print("3. Atualizar Status de Compra")
            print("4. Deletar Trecho")
            print("0. Voltar")
            
            opcao = self.solicitar_entrada("Opção", int)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.cadastrar_trecho_viagem()
            elif opcao == 2:
                self.listar_trechos_viagem()
            elif opcao == 3:
                self.atualizar_status_compra()
            elif opcao == 4:
                self.deletar_trecho_viagem()
            else:
                self.exibir_erro("Opção inválida!")
    
    def cadastrar_trecho_viagem(self):

        try:
            print("\n=== CADASTRAR TRECHO DE VIAGEM ===")
            
            tipos = self.transporte_controller.listar_tipos()
            if not tipos:
                self.exibir_erro("Nenhum tipo de transporte cadastrado. Cadastre um tipo primeiro.")
                return
            
            origem = self.solicitar_entrada("Local de origem")
            destino = self.solicitar_entrada("Local de destino")
            
            print("Data do trecho:")
            dia = self.solicitar_entrada("Dia", int)
            mes = self.solicitar_entrada("Mês", int)
            ano = self.solicitar_entrada("Ano", int)
            data_trecho = date(ano, mes, dia)
            
            print("\nTipos de transporte disponíveis:")
            for i, tipo in enumerate(tipos, 1):
                print(f"{i}. {tipo.tipo} - {tipo.empresa.nome}")
            
            escolha = self.solicitar_entrada("Escolha um tipo de transporte (número)", int) - 1
            if escolha < 0 or escolha >= len(tipos):
                self.exibir_erro("Tipo de transporte inválido!")
                return
            
            tipo_selecionado = tipos[escolha]
            
            compra_realizada = self.solicitar_entrada("Compra já foi realizada? (s/n)").lower() == 's'
            responsavel_compra = None
            
            if compra_realizada:
                responsavel_compra = self.solicitar_entrada("Nome do responsável pela compra")
            
            dados = {
                'data': data_trecho,
                'origem': origem,
                'destino': destino,
                'tipo_transporte_id': tipo_selecionado.id,
                'compra_realizada': compra_realizada,
                'responsavel_compra': responsavel_compra
            }
            
            trecho_id = self.transporte_controller.criar(dados)
            self.exibir_sucesso(f"Trecho cadastrado com sucesso! ID: {trecho_id}")
            
        except Exception as e:
            self.exibir_erro(f"Erro ao cadastrar trecho: {str(e)}")
    
    def listar_trechos_viagem(self):

        trechos = self.transporte_controller.listar_todos()
        if not trechos:
            self.exibir_mensagem("Nenhum trecho cadastrado.")
            return
        
        print("\n=== TRECHOS DE VIAGEM ===")
        for trecho in trechos:
            print(f"ID: {trecho.id}")
            print(f"Trecho: {trecho.origem} → {trecho.destino}")
            print(f"Data: {trecho.data}")
            print(f"Transporte: {trecho.tipo_transporte.tipo} - {trecho.tipo_transporte.empresa.nome}")
            print(f"Status: {'Comprado' if trecho.compra_realizada else 'Pendente'}")
            if trecho.responsavel_compra:
                print(f"Responsável: {trecho.responsavel_compra}")
            print("-" * 50)
    
    def atualizar_status_compra(self):

        try:
            trechos = self.transporte_controller.listar_todos()
            if not trechos:
                self.exibir_mensagem("Nenhum trecho cadastrado.")
                return
            
            print("\n=== ATUALIZAR STATUS DE COMPRA ===")
            print("\nTrechos disponíveis:")
            for i, trecho in enumerate(trechos, 1):
                status = "Comprado" if trecho.compra_realizada else "Pendente"
                print(f"{i}. {trecho.origem} → {trecho.destino} ({trecho.data}) - {status}")
            
            escolha = self.solicitar_entrada("Escolha um trecho (número)", int) - 1
            if escolha < 0 or escolha >= len(trechos):
                self.exibir_erro("Trecho inválido!")
                return
            
            trecho_selecionado = trechos[escolha]
            
            novo_status = self.solicitar_entrada("Compra realizada? (s/n)").lower() == 's'
            responsavel = None
            
            if novo_status:
                responsavel = self.solicitar_entrada("Nome do responsável pela compra")
            
            dados = {
                'compra_realizada': novo_status,
                'responsavel_compra': responsavel
            }
            
            if self.transporte_controller.atualizar(trecho_selecionado.id, dados):
                self.exibir_sucesso("Status atualizado com sucesso!")
            else:
                self.exibir_erro("Erro ao atualizar status.")
                
        except Exception as e:
            self.exibir_erro(f"Erro ao atualizar status: {str(e)}")
    
    def deletar_trecho_viagem(self):

        try:
            trechos = self.transporte_controller.listar_todos()
            if not trechos:
                self.exibir_mensagem("Nenhum trecho cadastrado.")
                return
            
            print("\n=== DELETAR TRECHO ===")
            print("\nTrechos disponíveis:")
            for i, trecho in enumerate(trechos, 1):
                print(f"{i}. {trecho.origem} → {trecho.destino} ({trecho.data})")
            
            escolha = self.solicitar_entrada("Escolha um trecho para deletar (número)", int) - 1
            if escolha < 0 or escolha >= len(trechos):
                self.exibir_erro("Trecho inválido!")
                return
            
            trecho_selecionado = trechos[escolha]
            
            confirmacao = self.solicitar_entrada(f"Confirma a exclusão do trecho {trecho_selecionado.origem} → {trecho_selecionado.destino}? (s/n)").lower()
            
            if confirmacao == 's':
                if self.transporte_controller.deletar(trecho_selecionado.id):
                    self.exibir_sucesso("Trecho deletado com sucesso!")
                else:
                    self.exibir_erro("Erro ao deletar trecho.")
            else:
                self.exibir_mensagem("Operação cancelada.")
                
        except Exception as e:
            self.exibir_erro(f"Erro ao deletar trecho: {str(e)}")

    def menu_passagens(self):

        while True:
            print("\n=== GERENCIAR PASSAGENS ===")
            print("1. Cadastrar Passagem")
            print("2. Listar Passagens")
            print("3. Listar Passagens por Viagem")
            print("4. Listar Passagens por Responsável")
            print("5. Atualizar Status de Compra")
            print("0. Voltar")
            
            opcao = self.solicitar_entrada("Opção", int)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.cadastrar_passagem()
            elif opcao == 2:
                self.listar_passagens()
            elif opcao == 3:
                self.listar_passagens_por_viagem()
            elif opcao == 4:
                self.listar_passagens_por_responsavel()
            elif opcao == 5:
                self.atualizar_status_compra_passagem()
            else:
                self.exibir_erro("Opção inválida!")

    def cadastrar_passagem(self):

        try:
            print("\n=== CADASTRAR PASSAGEM ===")
            
            viagens = self.viagem_controller.listar_todos()
            if not viagens:
                self.exibir_erro("Nenhuma viagem cadastrada.")
                return
                
            print("\nViagens disponíveis:")
            for i, viagem in enumerate(viagens, 1):
                print(f"{i}. {viagem.titulo} - {viagem.data_inicio} a {viagem.data_fim}")
            
            viagem_index = self.solicitar_entrada("Selecione a viagem", int) - 1
            if viagem_index < 0 or viagem_index >= len(viagens):
                self.exibir_erro("Viagem inválida.")
                return
            
            viagem_selecionada = viagens[viagem_index]
            viagem_id = viagem_selecionada.id
            
            origem = self.solicitar_entrada("Origem", str)
            destino = self.solicitar_entrada("Destino", str)
            
            data_viagem_str = self.solicitar_entrada("Data da viagem (YYYY-MM-DD)", str)
            
            hora_partida_str = self.solicitar_entrada("Hora de partida (HH:MM) - opcional", str, obrigatorio=False)
            hora_chegada_str = self.solicitar_entrada("Hora de chegada (HH:MM) - opcional", str, obrigatorio=False)
            
            empresas = self.empresa_controller.listar_todos()
            if not empresas:
                self.exibir_erro("Nenhuma empresa cadastrada.")
                return
                
            print("\nEmpresas disponíveis:")
            for i, empresa in enumerate(empresas, 1):
                print(f"{i}. {empresa.nome} - CNPJ: {empresa.cnpj}")
            
            empresa_index = self.solicitar_entrada("Selecione a empresa", int) - 1
            if empresa_index < 0 or empresa_index >= len(empresas):
                self.exibir_erro("Empresa inválida.")
                return
            
            empresa_selecionada = empresas[empresa_index]
            empresa_id = empresa_selecionada.id
            
            from models.tipo_transporte import TipoTransporte
            tipos_transporte = list(TipoTransporte)
            print("\nTipos de transporte disponíveis:")
            for i, tipo in enumerate(tipos_transporte, 1):
                print(f"{i}. {tipo.value}")
            
            tipo_index = self.solicitar_entrada("Selecione o tipo de transporte", int) - 1
            if tipo_index < 0 or tipo_index >= len(tipos_transporte):
                self.exibir_erro("Tipo de transporte inválido.")
                return
            tipo_transporte = tipos_transporte[tipo_index]
            
            tipo_transporte_id = self.passagem_controller.cadastrar_tipo_transporte({
                'empresa_id': empresa_id,
                'tipo': tipo_transporte
            })
            
            pessoas = self.pessoa_controller.listar_todos()
            if not pessoas:
                self.exibir_erro("Nenhuma pessoa cadastrada.")
                return
                
            print("\nPessoas disponíveis:")
            print("0. Nenhuma (não definir responsável)")
            for i, pessoa in enumerate(pessoas, 1):
                print(f"{i}. {pessoa.nome} - {pessoa.identificacao}")
            
            responsavel_index = self.solicitar_entrada("Selecione o responsável (0 para nenhum)", int)
            
            responsavel_id = None
            if responsavel_index > 0:
                if responsavel_index <= len(pessoas):
                    responsavel_selecionado = pessoas[responsavel_index - 1]
                    responsavel_id = responsavel_selecionado.id
                else:
                    self.exibir_erro("Pessoa inválida.")
                    return
            
            preco = self.solicitar_entrada("Preço (opcional)", float, obrigatorio=False)
            assento = self.solicitar_entrada("Número do assento (opcional)", str, obrigatorio=False)
            codigo_reserva = self.solicitar_entrada("Código de reserva (opcional)", str, obrigatorio=False)
            
            dados_passagem = {
                'viagem_id': viagem_id,
                'origem': origem,
                'destino': destino,
                'data_viagem': data_viagem_str,
                'tipo_transporte_id': tipo_transporte_id,
                'responsavel_compra_id': responsavel_id if responsavel_id else None,
                'valor': preco,
                'numero_assento': assento,
                'codigo_reserva': codigo_reserva,
                'compra_realizada': False
            }
            
            if hora_partida_str:
                dados_passagem['horario_partida'] = hora_partida_str
            if hora_chegada_str:
                dados_passagem['horario_chegada'] = hora_chegada_str
            
            passagem_id = self.passagem_controller.criar(dados_passagem)
            
            self.exibir_sucesso(f"Passagem criada com sucesso! ID: {passagem_id}")
            
        except Exception as e:
            self.exibir_erro(f"Erro ao cadastrar passagem: {str(e)}")

    def listar_passagens(self):

        try:
            passagens = self.passagem_controller.listar_todos()
            if not passagens:
                self.exibir_mensagem("Nenhuma passagem cadastrada.")
                return
            
            self.exibir_lista(passagens, "=== PASSAGENS CADASTRADAS ===")
            
        except Exception as e:
            self.exibir_erro(f"Erro ao listar passagens: {str(e)}")

    def listar_passagens_por_viagem(self):

        try:
            viagem_id = self.solicitar_entrada("ID da viagem", str)
            
            passagens = self.passagem_controller.listar_por_viagem(viagem_id)
            if not passagens:
                self.exibir_mensagem("Nenhuma passagem encontrada para esta viagem.")
                return
            
            self.exibir_lista(passagens, f"=== PASSAGENS DA VIAGEM {viagem_id} ===")
            
        except Exception as e:
            self.exibir_erro(f"Erro ao listar passagens por viagem: {str(e)}")

    def listar_passagens_por_responsavel(self):

        try:
            responsavel_id = self.solicitar_entrada("ID do responsável", str)
            
            passagens = self.passagem_controller.listar_por_responsavel(responsavel_id)
            if not passagens:
                self.exibir_mensagem("Nenhuma passagem encontrada para este responsável.")
                return
            
            self.exibir_lista(passagens, f"=== PASSAGENS DO RESPONSÁVEL {responsavel_id} ===")
            
        except Exception as e:
            self.exibir_erro(f"Erro ao listar passagens por responsável: {str(e)}")

    def atualizar_status_compra_passagem(self):

        try:
            passagens = self.passagem_controller.listar_todos()
            if not passagens:
                self.exibir_mensagem("Nenhuma passagem cadastrada.")
                return
            
            print("\nPassagens disponíveis:")
            for i, passagem in enumerate(passagens, 1):
                status = "Comprada" if passagem.comprada else "Não comprada"
                print(f"{i}. {passagem.origem} → {passagem.destino} - Status: {status}")
            
            passagem_index = self.solicitar_entrada("Selecione a passagem", int) - 1
            if passagem_index < 0 or passagem_index >= len(passagens):
                self.exibir_erro("Passagem inválida.")
                return
            
            passagem_selecionada = passagens[passagem_index]
            
            print(f"\nPassagem selecionada: {passagem_selecionada.origem} → {passagem_selecionada.destino}")
            print(f"Status atual: {'Comprada' if passagem_selecionada.comprada else 'Não comprada'}")
            
            novo_status = self.solicitar_entrada("Nova situação de compra (s/n)", str).lower() == 's'
            
            if novo_status:
                if passagem_selecionada.responsavel_compra_id:
                    self.passagem_controller.marcar_como_comprada(
                        passagem_selecionada.id, 
                        passagem_selecionada.responsavel_compra_id
                    )
                else:
                    pessoas = self.pessoa_controller.listar_todos()
                    if pessoas:
                        print("\nQuem será o responsável pela compra:")
                        for i, pessoa in enumerate(pessoas, 1):
                            print(f"{i}. {pessoa.nome}")
                        
                        responsavel_index = self.solicitar_entrada("Selecione o responsável", int) - 1
                        if 0 <= responsavel_index < len(pessoas):
                            responsavel = pessoas[responsavel_index]
                            self.passagem_controller.marcar_como_comprada(
                                passagem_selecionada.id, 
                                responsavel.id
                            )
                        else:
                            self.exibir_erro("Responsável inválido.")
                            return
                    else:
                        self.exibir_erro("Nenhuma pessoa cadastrada para ser responsável.")
                        return
            else:
                self.passagem_controller.cancelar_compra(passagem_selecionada.id)
            
            status_texto = "Comprada" if novo_status else "Não comprada"
            self.exibir_sucesso(f"Status da passagem atualizado para: {status_texto}")
            
        except Exception as e:
            self.exibir_erro(f"Erro ao atualizar status da passagem: {str(e)}")

    def cadastrar_dados_iniciais(self):

        try:
            print("Cadastrando dados iniciais...")
            
            clientes_dados = MockedData.get_clientes_dados()
            cliente_ids = []
            for cliente_dados in clientes_dados:
                cliente_id = self.pessoa_controller.criar(cliente_dados)
                cliente_ids.append(cliente_id)
            
            empresas_dados = MockedData.get_empresas_dados()
            empresa_ids = []
            for empresa_dados in empresas_dados:
                empresa_id = self.empresa_controller.criar(empresa_dados)
                empresa_ids.append(empresa_id)
            
            destinos_dados = MockedData.get_destinos_dados()
            destino_ids = []
            for destino_dados in destinos_dados:
                destino_id = self.destino_controller.criar(destino_dados)
                destino_ids.append(destino_id)
            
            viagens_dados = MockedData.get_viagens_dados(destino_ids)
            viagem_ids = []
            for viagem_dados in viagens_dados:
                viagem_id = self.viagem_controller.criar(viagem_dados)
                viagem_ids.append(viagem_id)
                
                for cliente_id in cliente_ids[:3]:  
                    self.viagem_controller.adicionar_participante(viagem_id, cliente_id)
            
            tipos_transporte_dados = MockedData.get_tipos_transporte_dados(empresa_ids)
            
            tipo_transporte_ids = []
            for tipo_dados in tipos_transporte_dados:
                tipo_id = self.transporte_controller.criar_tipo(tipo_dados)
                tipo_transporte_ids.append(tipo_id)
            
            passagem_tipo_transporte_ids = []
            for tipo_dados in tipos_transporte_dados:
                tipo_id = self.passagem_controller.cadastrar_tipo_transporte(tipo_dados)
                passagem_tipo_transporte_ids.append(tipo_id)
            
            passagens_dados = MockedData.get_passagens_dados(viagem_ids, passagem_tipo_transporte_ids, cliente_ids)
            passagem_ids = []
            for passagem_dados in passagens_dados:
                passagem_id = self.passagem_controller.criar(passagem_dados)
                passagem_ids.append(passagem_id)
            
            transportes_dados = MockedData.get_transportes_dados(tipo_transporte_ids)
            transporte_ids = []
            for transporte_dados in transportes_dados:
                try:
                    transporte_id = self.transporte_controller.criar(transporte_dados)
                    transporte_ids.append(transporte_id)
                except Exception as e:
                    print(f"   - Aviso: Erro ao cadastrar transporte {transporte_dados['origem']}->{transporte_dados['destino']}: {e}")
            
            passeios_dados = MockedData.get_passeios_dados(viagem_ids, destino_ids)
            passeio_ids = []
            for i, passeio_dados in enumerate(passeios_dados):
                passeio_dados['pessoa_id'] = cliente_ids[i % len(cliente_ids)]
                passeio_id = self.passeio_controller.criar(passeio_dados)
                passeio_ids.append(passeio_id)
            
            pagamentos_dados = MockedData.get_pagamentos_dados(cliente_ids)
            pagamento_ids = []
            for i, pagamento_dados in enumerate(pagamentos_dados):
                pagamento_dados['viagem_id'] = viagem_ids[i % len(viagem_ids)]
                pagamento_id = self.pagamento_controller.criar(pagamento_dados)
                pagamento_ids.append(pagamento_id)
            
            print("✅ Dados iniciais cadastrados com sucesso!")
            print(f"   - {len(cliente_ids)} clientes cadastrados")
            print(f"   - {len(empresa_ids)} empresas cadastradas")
            print(f"   - {len(destino_ids)} destinos cadastrados")
            print(f"   - {len(viagem_ids)} viagens cadastradas")
            print(f"   - {len(tipo_transporte_ids)} tipos de transporte cadastrados")
            print(f"   - {len(passagem_ids)} passagens cadastradas")
            print(f"   - {len(passeio_ids)} passeios cadastrados")
            print(f"   - {len(pagamento_ids)} pagamentos cadastrados")
            print(f"   - {len(transporte_ids)} trechos de transporte cadastrados")
            print()
            
        except Exception as e:
            print(f"⚠️  Erro ao cadastrar dados iniciais: {e}")
            print("Continuando sem dados pré-cadastrados...")
            print()

    def menu_relatorios(self):

        while True:
            print("\n=== RELATÓRIOS ===")
            print("1. Destinos Mais Populares")
            print("2. Destinos Mais Caros")
            print("3. Destinos Mais Baratos")
            print("4. Passeios Mais Populares")
            print("5. Passeios Mais Caros")
            print("6. Passeios Mais Baratos")
            print("7. Relatório Financeiro de Viagem")
            print("0. Voltar")
            
            opcao = self.solicitar_entrada("Opção", int)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.relatorio_destinos_populares()
            elif opcao == 2:
                self.relatorio_destinos_caros()
            elif opcao == 3:
                self.relatorio_destinos_baratos()
            elif opcao == 4:
                self.relatorio_passeios_populares()
            elif opcao == 5:
                self.relatorio_passeios_caros()
            elif opcao == 6:
                self.relatorio_passeios_baratos()
            elif opcao == 7:
                self.relatorio_financeiro()
    
    def relatorio_destinos_populares(self):
        destinos = self.relatorio_service.destinos_mais_populares(5)
        
        print("\n=== DESTINOS MAIS POPULARES ===")
        if not destinos:
            print("Nenhum destino encontrado.")
            return
        
        for i, (destino, count) in enumerate(destinos, 1):
            print(f"{i}. {destino.nome_completo()} - {count} viagem(ns)")
    
    def relatorio_destinos_caros(self):
        destinos = self.relatorio_service.destinos_mais_caros(5)
        
        print("\n=== DESTINOS MAIS CAROS ===")
        if not destinos:
            print("Nenhum destino encontrado.")
            return
        
        for i, (destino, valor) in enumerate(destinos, 1):
            print(f"{i}. {destino.nome_completo()} - R$ {valor:.2f} (média)")
    
    def relatorio_destinos_baratos(self):
        destinos = self.relatorio_service.destinos_mais_baratos(5)
        
        print("\n=== DESTINOS MAIS BARATOS ===")
        if not destinos:
            print("Nenhum destino encontrado.")
            return
        
        for i, (destino, valor) in enumerate(destinos, 1):
            print(f"{i}. {destino.nome_completo()} - R$ {valor:.2f} (média)")
    
    def relatorio_passeios_populares(self):
        passeios = self.relatorio_service.passeios_mais_populares(5)
        
        print("\n=== PASSEIOS MAIS POPULARES ===")
        if not passeios:
            print("Nenhum passeio encontrado.")
            return
        
        for i, (atracao, count) in enumerate(passeios, 1):
            print(f"{i}. {atracao} - {count} vez(es)")
    
    def relatorio_passeios_caros(self):
        passeios = self.relatorio_service.passeios_mais_caros(5)
        
        print("\n=== PASSEIOS MAIS CAROS ===")
        if not passeios:
            print("Nenhum passeio encontrado.")
            return
        
        for i, (passeio, valor) in enumerate(passeios, 1):
            print(f"{i}. {passeio.atracao_turistica} em {passeio.cidade} - R$ {valor:.2f}")
    
    def relatorio_passeios_baratos(self):
        passeios = self.relatorio_service.passeios_mais_baratos(5)
        
        print("\n=== PASSEIOS MAIS BARATOS ===")
        if not passeios:
            print("Nenhum passeio encontrado.")
            return
        
        for i, (passeio, valor) in enumerate(passeios, 1):
            print(f"{i}. {passeio.atracao_turistica} em {passeio.cidade} - R$ {valor:.2f}")
    
    def relatorio_financeiro(self):
        viagens = self.viagem_controller.listar_todos()
        if not viagens:
            self.exibir_mensagem("Nenhuma viagem cadastrada.")
            return
        
        print("\nViagens disponíveis:")
        for i, viagem in enumerate(viagens, 1):
            print(f"{i}. {viagem}")
        
        try:
            indice = self.solicitar_entrada("Selecione a viagem", int) - 1
            if 0 <= indice < len(viagens):
                viagem = viagens[indice]
                relatorio = self.relatorio_service.relatorio_financeiro_viagem(viagem.id)
                
                print(f"\n=== RELATÓRIO FINANCEIRO - {viagem.titulo} ===")
                print(f"Valor Total: R$ {relatorio['valor_total']:.2f}")
                print(f"Total Pago: R$ {relatorio['total_pago']:.2f}")
                print(f"Saldo Devedor: R$ {relatorio['saldo_devedor']:.2f}")
                print(f"Percentual Pago: {relatorio['percentual_pago']:.1f}%")
            else:
                self.exibir_erro("Índice inválido.")
        except ValueError:
            self.exibir_erro("Valor inválido.")
    
    def menu_viagens(self):
        while True:
            print("\n=== GERENCIAR VIAGENS ===")
            print("1. Criar Viagem")
            print("2. Listar Viagens")
            print("3. Buscar Viagem")
            print("4. Adicionar Participante")
            print("5. Remover Participante")
            print("6. Atualizar Viagem")
            print("7. Deletar Viagem")
            print("0. Voltar")
            
            opcao = self.solicitar_entrada("Opção", int)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.criar_viagem()
            elif opcao == 2:
                self.listar_viagens()
            elif opcao == 3:
                self.buscar_viagem()
            elif opcao == 4:
                self.adicionar_participante_viagem()
            elif opcao == 5:
                self.remover_participante_viagem()
            elif opcao == 6:
                self.atualizar_viagem()
            elif opcao == 7:
                self.deletar_viagem()
    
    def criar_viagem(self):
        try:
            print("\n=== CRIAR VIAGEM ===")
            titulo = self.solicitar_entrada("Título da viagem")
            
            print("Data de início:")
            dia = self.solicitar_entrada("Dia", int)
            mes = self.solicitar_entrada("Mês", int)
            ano = self.solicitar_entrada("Ano", int)
            data_inicio = date(ano, mes, dia)
            
            print("Data de fim:")
            dia = self.solicitar_entrada("Dia", int)
            mes = self.solicitar_entrada("Mês", int)
            ano = self.solicitar_entrada("Ano", int)
            data_fim = date(ano, mes, dia)
            
            valor_total = self.solicitar_entrada("Valor total", float)
            
            destinos = self.destino_controller.listar_todos()
            if not destinos:
                self.exibir_erro("Nenhum destino cadastrado. Cadastre destinos primeiro.")
                return
            
            print("\nDestinos disponíveis:")
            for i, destino in enumerate(destinos, 1):
                print(f"{i}. {destino}")
            
            destino_ids = []
            while True:
                try:
                    indice = self.solicitar_entrada("Selecione destino (0 para finalizar)", int)
                    if indice == 0:
                        break
                    if 1 <= indice <= len(destinos):
                        destino_id = destinos[indice-1].id
                        if destino_id not in destino_ids:
                            destino_ids.append(destino_id)
                            print(f"Destino {destinos[indice-1].nome_completo()} adicionado")
                        else:
                            print("Destino já adicionado")
                    else:
                        print("Índice inválido")
                except ValueError:
                    print("Valor inválido")
            
            if not destino_ids:
                self.exibir_erro("Pelo menos um destino deve ser selecionado")
                return
            
            dados = {
                'titulo': titulo,
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'valor_total': valor_total,
                'destino_ids': destino_ids
            }
            
            viagem_id = self.viagem_controller.criar(dados)
            self.exibir_sucesso(f"Viagem criada com ID: {viagem_id}")
            
        except Exception as e:
            self.exibir_erro(f"Erro ao criar viagem: {str(e)}")
    
    def listar_viagens(self):
        viagens = self.viagem_controller.listar_todos()
        self.exibir_lista(viagens, "VIAGENS CADASTRADAS")
    
    def buscar_viagem(self):
        viagens = self.viagem_controller.listar_todos()
        if not viagens:
            self.exibir_mensagem("Nenhuma viagem cadastrada.")
            return
        
        print("\nViagens disponíveis:")
        for i, viagem in enumerate(viagens, 1):
            print(f"{i}. {viagem}")
        
        try:
            indice = self.solicitar_entrada("Selecione a viagem", int) - 1
            if 0 <= indice < len(viagens):
                viagem = viagens[indice]
                print(f"\n=== DETALHES DA VIAGEM ===")
                print(f"Título: {viagem.titulo}")
                print(f"Período: {viagem.data_inicio} a {viagem.data_fim}")
                print(f"Valor Total: R$ {viagem.valor_total:.2f}")
                print(f"Participantes: {len(viagem.participantes)}")
                print(f"Destinos: {', '.join([d.nome_completo() for d in viagem.destinos])}")
            else:
                self.exibir_erro("Índice inválido")
        except ValueError:
            self.exibir_erro("Valor inválido")
    
    def adicionar_participante_viagem(self):
        viagens = self.viagem_controller.listar_todos()
        pessoas = self.pessoa_controller.listar_todos()
        
        if not viagens:
            self.exibir_mensagem("Nenhuma viagem cadastrada.")
            return
        
        if not pessoas:
            self.exibir_mensagem("Nenhuma pessoa cadastrada.")
            return
        
        print("\nViagens disponíveis:")
        for i, viagem in enumerate(viagens, 1):
            print(f"{i}. {viagem}")
        
        try:
            indice_viagem = self.solicitar_entrada("Selecione a viagem", int) - 1
            if not (0 <= indice_viagem < len(viagens)):
                self.exibir_erro("Índice de viagem inválido")
                return
            
            viagem = viagens[indice_viagem]
            
            print("\nPessoas disponíveis:")
            for i, pessoa in enumerate(pessoas, 1):
                print(f"{i}. {pessoa}")
            
            indice_pessoa = self.solicitar_entrada("Selecione a pessoa", int) - 1
            if not (0 <= indice_pessoa < len(pessoas)):
                self.exibir_erro("Índice de pessoa inválido")
                return
            
            pessoa = pessoas[indice_pessoa]
            
            if self.viagem_controller.adicionar_participante(viagem.id, pessoa.id):
                self.exibir_sucesso(f"Participante {pessoa.nome} adicionado à viagem {viagem.titulo}")
            else:
                self.exibir_erro("Erro ao adicionar participante")
                
        except ValueError:
            self.exibir_erro("Valor inválido")
    
    def remover_participante_viagem(self):
        viagens = self.viagem_controller.listar_todos()
        
        if not viagens:
            self.exibir_mensagem("Nenhuma viagem cadastrada.")
            return
        
        print("\nViagens disponíveis:")
        for i, viagem in enumerate(viagens, 1):
            print(f"{i}. {viagem} - {len(viagem.participantes)} participante(s)")
        
        try:
            indice_viagem = self.solicitar_entrada("Selecione a viagem", int) - 1
            if not (0 <= indice_viagem < len(viagens)):
                self.exibir_erro("Índice de viagem inválido")
                return
            
            viagem = viagens[indice_viagem]
            
            if not viagem.participantes:
                self.exibir_mensagem("Esta viagem não possui participantes.")
                return
            
            print("\nParticipantes da viagem:")
            for i, pessoa in enumerate(viagem.participantes, 1):
                print(f"{i}. {pessoa}")
            
            indice_pessoa = self.solicitar_entrada("Selecione a pessoa para remover", int) - 1
            if not (0 <= indice_pessoa < len(viagem.participantes)):
                self.exibir_erro("Índice de pessoa inválido")
                return
            
            pessoa = viagem.participantes[indice_pessoa]
            
            if self.viagem_controller.remover_participante(viagem.id, pessoa.id):
                self.exibir_sucesso(f"Participante {pessoa.nome} removido da viagem {viagem.titulo}")
            else:
                self.exibir_erro("Erro ao remover participante")
                
        except ValueError:
            self.exibir_erro("Valor inválido")
    
    def atualizar_viagem(self):
        viagens = self.viagem_controller.listar_todos()
        
        if not viagens:
            self.exibir_mensagem("Nenhuma viagem cadastrada.")
            return
        
        print("\nViagens disponíveis:")
        for i, viagem in enumerate(viagens, 1):
            print(f"{i}. {viagem}")
        
        try:
            indice = self.solicitar_entrada("Selecione a viagem para atualizar", int) - 1
            if not (0 <= indice < len(viagens)):
                self.exibir_erro("Índice inválido")
                return
            
            viagem = viagens[indice]
            print(f"Valor atual: R$ {viagem.valor_total:.2f}")
            novo_valor = self.solicitar_entrada("Novo valor total", float)
            
            dados = {'valor_total': novo_valor}
            
            if self.viagem_controller.atualizar(viagem.id, dados):
                self.exibir_sucesso("Viagem atualizada com sucesso")
            else:
                self.exibir_erro("Erro ao atualizar viagem")
                
        except ValueError:
            self.exibir_erro("Valor inválido")
    
    def deletar_viagem(self):
        viagens = self.viagem_controller.listar_todos()
        
        if not viagens:
            self.exibir_mensagem("Nenhuma viagem cadastrada.")
            return
        
        print("\nViagens disponíveis:")
        for i, viagem in enumerate(viagens, 1):
            print(f"{i}. {viagem}")
        
        try:
            indice = self.solicitar_entrada("Selecione a viagem para deletar", int) - 1
            if not (0 <= indice < len(viagens)):
                self.exibir_erro("Índice inválido")
                return
            
            viagem = viagens[indice]
            
            if self.confirmar_acao(f"Confirma a exclusão da viagem '{viagem.titulo}'?"):
                if self.viagem_controller.deletar(viagem.id):
                    self.exibir_sucesso("Viagem deletada com sucesso")
                else:
                    self.exibir_erro("Erro ao deletar viagem")
                    
        except ValueError:
            self.exibir_erro("Valor inválido")
    
    def menu_pagamentos(self):
        while True:
            print("\n=== GERENCIAR PAGAMENTOS ===")
            print("1. Registrar Pagamento")
            print("2. Listar Pagamentos")
            print("3. Buscar Pagamentos por Viagem")
            print("4. Buscar Pagamentos por Pessoa")
            print("5. Estornar Pagamento")
            print("0. Voltar")
            
            opcao = self.solicitar_entrada("Opção", int)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.registrar_pagamento()
            elif opcao == 2:
                self.listar_pagamentos()
            elif opcao == 3:
                self.listar_pagamentos_por_viagem()
            elif opcao == 4:
                self.listar_pagamentos_por_pessoa()
            elif opcao == 5:
                self.estornar_pagamento()
    
    def registrar_pagamento(self):
        try:
            print("\n=== REGISTRAR PAGAMENTO ===")
            
            pessoas = self.pessoa_controller.listar_todos()
            viagens = self.viagem_controller.listar_todos()
            
            if not pessoas:
                self.exibir_erro("Nenhuma pessoa cadastrada.")
                return
            
            if not viagens:
                self.exibir_erro("Nenhuma viagem cadastrada.")
                return
            
            print("Pessoas disponíveis:")
            for i, pessoa in enumerate(pessoas, 1):
                print(f"{i}. {pessoa}")
            
            indice_pessoa = self.solicitar_entrada("Selecione a pessoa", int) - 1
            if not (0 <= indice_pessoa < len(pessoas)):
                self.exibir_erro("Índice de pessoa inválido")
                return
            
            pessoa = pessoas[indice_pessoa]
            
            print("\nViagens disponíveis:")
            for i, viagem in enumerate(viagens, 1):
                print(f"{i}. {viagem}")
            
            indice_viagem = self.solicitar_entrada("Selecione a viagem", int) - 1
            if not (0 <= indice_viagem < len(viagens)):
                self.exibir_erro("Índice de viagem inválido")
                return
            
            viagem = viagens[indice_viagem]
            
            print("Data do pagamento:")
            dia = self.solicitar_entrada("Dia", int)
            mes = self.solicitar_entrada("Mês", int)
            ano = self.solicitar_entrada("Ano", int)
            data_pagamento = date(ano, mes, dia)
            
            valor = self.solicitar_entrada("Valor do pagamento", float)
            
            print("\nTipos de pagamento:")
            print("1. Dinheiro")
            print("2. PIX")
            print("3. Cartão de Crédito")
            
            tipo_opcao = self.solicitar_entrada("Selecione o tipo", int)
            
            dados = {
                'data': data_pagamento,
                'valor': valor,
                'pessoa_id': pessoa.id,
                'viagem_id': viagem.id
            }
            
            if tipo_opcao == 1:
                dados['tipo'] = 'dinheiro'
            elif tipo_opcao == 2:
                dados['tipo'] = 'pix'
                dados['cpf_pagador'] = self.solicitar_entrada("CPF do pagador")
            elif tipo_opcao == 3:
                dados['tipo'] = 'cartao'
                dados['numero_cartao'] = self.solicitar_entrada("Número do cartão")
                dados['bandeira'] = self.solicitar_entrada("Bandeira do cartão")
            else:
                self.exibir_erro("Tipo de pagamento inválido")
                return
            
            pagamento_id = self.pagamento_controller.criar(dados)
            self.exibir_sucesso(f"Pagamento registrado com ID: {pagamento_id}")
            
        except Exception as e:
            self.exibir_erro(f"Erro ao registrar pagamento: {str(e)}")
    
    def listar_pagamentos(self):
        pagamentos = self.pagamento_controller.listar_todos()
        self.exibir_lista(pagamentos, "PAGAMENTOS REGISTRADOS")
    
    def listar_pagamentos_por_viagem(self):
        viagens = self.viagem_controller.listar_todos()
        
        if not viagens:
            self.exibir_mensagem("Nenhuma viagem cadastrada.")
            return
        
        print("\nViagens disponíveis:")
        for i, viagem in enumerate(viagens, 1):
            print(f"{i}. {viagem}")
        
        try:
            indice = self.solicitar_entrada("Selecione a viagem", int) - 1
            if 0 <= indice < len(viagens):
                viagem = viagens[indice]
                pagamentos = self.pagamento_controller.listar_por_viagem(viagem.id)
                
                if pagamentos:
                    print(f"\n=== PAGAMENTOS DA VIAGEM: {viagem.titulo} ===")
                    for pagamento in pagamentos:
                        print(f"- {pagamento}")
                    
                    total = self.pagamento_controller.calcular_total_por_viagem(viagem.id)
                    print(f"\nTotal pago: R$ {total:.2f}")
                    print(f"Saldo devedor: R$ {viagem.valor_total - total:.2f}")
                else:
                    self.exibir_mensagem("Nenhum pagamento encontrado para esta viagem.")
            else:
                self.exibir_erro("Índice inválido")
        except ValueError:
            self.exibir_erro("Valor inválido")
    
    def listar_pagamentos_por_pessoa(self):
        pessoas = self.pessoa_controller.listar_todos()
        
        if not pessoas:
            self.exibir_mensagem("Nenhuma pessoa cadastrada.")
            return
        
        print("\nPessoas disponíveis:")
        for i, pessoa in enumerate(pessoas, 1):
            print(f"{i}. {pessoa}")
        
        try:
            indice = self.solicitar_entrada("Selecione a pessoa", int) - 1
            if 0 <= indice < len(pessoas):
                pessoa = pessoas[indice]
                pagamentos = self.pagamento_controller.listar_por_pessoa(pessoa.id)
                
                if pagamentos:
                    print(f"\n=== PAGAMENTOS DE: {pessoa.nome} ===")
                    for pagamento in pagamentos:
                        print(f"- {pagamento}")
                    
                    total = self.pagamento_controller.calcular_total_por_pessoa(pessoa.id)
                    print(f"\nTotal pago: R$ {total:.2f}")
                else:
                    self.exibir_mensagem("Nenhum pagamento encontrado para esta pessoa.")
            else:
                self.exibir_erro("Índice inválido")
        except ValueError:
            self.exibir_erro("Valor inválido")
    
    def estornar_pagamento(self):
        pagamentos = self.pagamento_controller.listar_todos()
        
        if not pagamentos:
            self.exibir_mensagem("Nenhum pagamento registrado.")
            return
        
        print("\nPagamentos disponíveis:")
        for i, pagamento in enumerate(pagamentos, 1):
            print(f"{i}. {pagamento}")
        
        try:
            indice = self.solicitar_entrada("Selecione o pagamento para estornar", int) - 1
            if 0 <= indice < len(pagamentos):
                pagamento = pagamentos[indice]
                
                if self.confirmar_acao(f"Confirma o estorno do pagamento de R$ {pagamento.valor:.2f}?"):
                    if self.pagamento_controller.deletar(pagamento.id):
                        self.exibir_sucesso("Pagamento estornado com sucesso")
                    else:
                        self.exibir_erro("Erro ao estornar pagamento")
            else:
                self.exibir_erro("Índice inválido")
        except ValueError:
            self.exibir_erro("Valor inválido")
    
    def menu_passeios(self):
        while True:
            print("\n=== GERENCIAR PASSEIOS ===")
            print("1. Cadastrar Passeio")
            print("2. Listar Passeios")
            print("3. Buscar Passeio")
            print("4. Atualizar Passeio")
            print("5. Deletar Passeio")
            print("0. Voltar")
            
            opcao = self.solicitar_entrada("Opção", int)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.cadastrar_passeio()
            elif opcao == 2:
                self.listar_passeios()
            elif opcao == 3:
                self.buscar_passeio()
            elif opcao == 4:
                self.atualizar_passeio()
            elif opcao == 5:
                self.deletar_passeio()
    
    def cadastrar_passeio(self):
        try:
            print("\n=== CADASTRAR PASSEIO ===")
            
            pessoas = self.pessoa_controller.listar_todos()
            destinos = self.destino_controller.listar_todos()
            
            if not pessoas:
                self.exibir_erro("Nenhuma pessoa cadastrada.")
                return
            
            cidade = self.solicitar_entrada("Cidade do passeio")
            atracao = self.solicitar_entrada("Atração turística")
            
            print("Horário de início:")
            hora_inicio = self.solicitar_entrada("Hora (0-23)", int)
            minuto_inicio = self.solicitar_entrada("Minuto (0-59)", int)
            horario_inicio = time(hora_inicio, minuto_inicio)
            
            print("Horário de fim:")
            hora_fim = self.solicitar_entrada("Hora (0-23)", int)
            minuto_fim = self.solicitar_entrada("Minuto (0-59)", int)
            horario_fim = time(hora_fim, minuto_fim)
            
            valor = self.solicitar_entrada("Valor do passeio", float)
            
            print("Data do passeio:")
            dia = self.solicitar_entrada("Dia", int)
            mes = self.solicitar_entrada("Mês", int)
            ano = self.solicitar_entrada("Ano", int)
            data_passeio = date(ano, mes, dia)
            
            print("\nPessoas disponíveis:")
            for i, pessoa in enumerate(pessoas, 1):
                print(f"{i}. {pessoa}")
            
            indice_pessoa = self.solicitar_entrada("Selecione a pessoa", int) - 1
            if not (0 <= indice_pessoa < len(pessoas)):
                self.exibir_erro("Índice de pessoa inválido")
                return
            
            pessoa = pessoas[indice_pessoa]
            
            destino = None
            if destinos:
                print("\nDestinos disponíveis (opcional):")
                print("0. Nenhum")
                for i, dest in enumerate(destinos, 1):
                    print(f"{i}. {dest}")
                
                indice_destino = self.solicitar_entrada("Selecione o destino", int)
                if 1 <= indice_destino <= len(destinos):
                    destino = destinos[indice_destino - 1]
            
            from models.passeio import Passeio
            passeio = Passeio(
                cidade=cidade,
                atracao_turistica=atracao,
                horario_inicio=horario_inicio,
                horario_fim=horario_fim,
                valor=valor,
                pessoa=pessoa,
                data_passeio=data_passeio,
                destino=destino
            )
            
            self.relatorio_service.adicionar_passeio(passeio)
            self.exibir_sucesso(f"Passeio cadastrado: {passeio}")
            
        except Exception as e:
            self.exibir_erro(f"Erro ao cadastrar passeio: {str(e)}")
    
    def listar_passeios(self):
        passeios = self.relatorio_service._passeios
        self.exibir_lista(passeios, "PASSEIOS CADASTRADOS")
    
    def buscar_passeio(self):
        passeios = self.relatorio_service._passeios
        
        if not passeios:
            self.exibir_mensagem("Nenhum passeio cadastrado.")
            return
        
        print("\nPasseios disponíveis:")
        for i, passeio in enumerate(passeios, 1):
            print(f"{i}. {passeio}")
        
        try:
            indice = self.solicitar_entrada("Selecione o passeio", int) - 1
            if 0 <= indice < len(passeios):
                passeio = passeios[indice]
                print(f"\n=== DETALHES DO PASSEIO ===")
                print(f"Atração: {passeio.atracao_turistica}")
                print(f"Cidade: {passeio.cidade}")
                print(f"Data: {passeio.data_passeio}")
                print(f"Horário: {passeio.horario_inicio} às {passeio.horario_fim}")
                print(f"Duração: {passeio.duracao_horas():.1f} horas")
                print(f"Valor: R$ {passeio.valor:.2f}")
                print(f"Pessoa: {passeio.pessoa.nome}")
                if passeio.destino:
                    print(f"Destino: {passeio.destino.nome_completo()}")
            else:
                self.exibir_erro("Índice inválido")
        except ValueError:
            self.exibir_erro("Valor inválido")
    
    def atualizar_passeio(self):
        passeios = self.relatorio_service._passeios
        
        if not passeios:
            self.exibir_mensagem("Nenhum passeio cadastrado.")
            return
        
        print("\nPasseios disponíveis:")
        for i, passeio in enumerate(passeios, 1):
            print(f"{i}. {passeio}")
        
        try:
            indice = self.solicitar_entrada("Selecione o passeio para atualizar", int) - 1
            if not (0 <= indice < len(passeios)):
                self.exibir_erro("Índice inválido")
                return
            
            passeio = passeios[indice]
            print(f"Valor atual: R$ {passeio.valor:.2f}")
            novo_valor = self.solicitar_entrada("Novo valor", float)
            
            passeio.valor = novo_valor
            self.exibir_sucesso("Passeio atualizado com sucesso")
            
        except ValueError:
            self.exibir_erro("Valor inválido")
        except Exception as e:
            self.exibir_erro(f"Erro ao atualizar passeio: {str(e)}")
    
    def deletar_passeio(self):
        passeios = self.relatorio_service._passeios
        
        if not passeios:
            self.exibir_mensagem("Nenhum passeio cadastrado.")
            return
        
        print("\nPasseios disponíveis:")
        for i, passeio in enumerate(passeios, 1):
            print(f"{i}. {passeio}")
        
        try:
            indice = self.solicitar_entrada("Selecione o passeio para deletar", int) - 1
            if not (0 <= indice < len(passeios)):
                self.exibir_erro("Índice inválido")
                return
            
            passeio = passeios[indice]
            
            if self.confirmar_acao(f"Confirma a exclusão do passeio '{passeio.atracao_turistica}'?"):
                self.relatorio_service._passeios.remove(passeio)
                self.exibir_sucesso("Passeio deletado com sucesso")
                
        except ValueError:
            self.exibir_erro("Valor inválido")
