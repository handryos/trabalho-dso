from datetime import date, datetime


class MockedData:
    @staticmethod
    def get_clientes_dados():

        return [
            {
                'nome': 'João Silva',
                'identificacao': '12345678901',
                'data_nascimento': date(1990, 5, 15),
                'celular': '(11) 99999-1111',
                'tipo_identificacao': 'cpf'
            },
            {
                'nome': 'Maria Santos',
                'identificacao': '98765432109',
                'data_nascimento': date(1985, 8, 20),
                'celular': '(11) 99999-2222',
                'tipo_identificacao': 'cpf'
            },
            {
                'nome': 'Pedro Costa',
                'identificacao': '11122233344',
                'data_nascimento': date(1992, 12, 10),
                'celular': '(11) 99999-3333',
                'tipo_identificacao': 'cpf'
            },
            {
                'nome': 'Ana Oliveira',
                'identificacao': '55566677788',
                'data_nascimento': date(1988, 3, 25),
                'celular': '(11) 99999-4444',
                'tipo_identificacao': 'cpf'
            },
            {
                'nome': 'Carlos Ferreira',
                'identificacao': '44433322211',
                'data_nascimento': date(1995, 11, 8),
                'celular': '(11) 99999-5555',
                'tipo_identificacao': 'cpf'
            }
        ]
    
    @staticmethod
    def get_empresas_dados():
        return [
            {
                'nome': 'Viação São Paulo Express',
                'cnpj': '12345678000199',
                'telefone': '(11) 3333-4444'
            },
            {
                'nome': 'Transportes Rio Sul',
                'cnpj': '23456789000101',
                'telefone': '(11) 3333-5555'
            },
            {
                'nome': 'Companhia Aérea Nacional',
                'cnpj': '34567890000112',
                'telefone': '(11) 3333-6666'
            },
            {
                'nome': 'Turismo Bahia',
                'cnpj': '45678901000123',
                'telefone': '(11) 3333-7777'
            },
            {
                'nome': 'Excursões Nordeste',
                'cnpj': '56789012000134',
                'telefone': '(11) 3333-8888'
            }
        ]
    
    @staticmethod
    def get_destinos_dados():
        return [
            {
                'cidade': 'Rio de Janeiro',
                'pais': 'Brasil',
                'descricao': 'Cidade Maravilhosa com praias deslumbrantes'
            },
            {
                'cidade': 'Salvador',
                'pais': 'Brasil',
                'descricao': 'Capital da Bahia, rica em cultura e história'
            },
            {
                'cidade': 'Recife',
                'pais': 'Brasil',
                'descricao': 'Veneza Brasileira com arquitetura colonial'
            },
            {
                'cidade': 'Fortaleza',
                'pais': 'Brasil',
                'descricao': 'Belas praias e vida noturna agitada'
            },
            {
                'cidade': 'Natal',
                'pais': 'Brasil',
                'descricao': 'Cidade do Sol com dunas espetaculares'
            },
            {
                'cidade': 'João Pessoa',
                'pais': 'Brasil',
                'descricao': 'Ponto mais oriental das Américas'
            },
            {
                'cidade': 'Maceió',
                'pais': 'Brasil',
                'descricao': 'Paraíso tropical com águas cristalinas'
            },
            {
                'cidade': 'Aracaju',
                'pais': 'Brasil',
                'descricao': 'Menor capital do Brasil com belas praias'
            }
        ]
    
    @staticmethod
    def get_viagens_dados(destino_ids):
        return [
            {
                'titulo': 'Nordeste Completo',
                'data_inicio': date(2025, 12, 1),
                'data_fim': date(2025, 12, 15),
                'valor_total': 2500.00,
                'destino_ids': destino_ids[:4],  
                'ordens': [1, 2, 3, 4]
            },
            {
                'titulo': 'Costa Leste',
                'data_inicio': date(2025, 11, 10),
                'data_fim': date(2025, 11, 20),
                'valor_total': 1800.00,
                'destino_ids': destino_ids[4:], 
                'ordens': [1, 2, 3, 4]
            },
            {
                'titulo': 'Bahia Especial',
                'data_inicio': date(2025, 10, 5),
                'data_fim': date(2025, 10, 12),
                'valor_total': 1200.00,
                'destino_ids': [destino_ids[1]],  
                'ordens': [1]
            }
        ]
    
    @staticmethod
    def get_tipos_transporte_dados(empresa_ids):
        return [
            {
                'empresa_id': empresa_ids[0],
                'tipo': 'Ônibus'
            },
            {
                'empresa_id': empresa_ids[1],
                'tipo': 'Ônibus'
            },
            {
                'empresa_id': empresa_ids[2],
                'tipo': 'Avião'
            },
            {
                'empresa_id': empresa_ids[3],
                'tipo': 'Van'
            }
        ]
    
    @staticmethod
    def get_passagens_dados(viagem_ids, passagem_tipo_transporte_ids, cliente_ids):
        return [
            {
                'viagem_id': viagem_ids[0],
                'origem': 'São Paulo',
                'destino': 'Rio de Janeiro',
                'data_viagem': '2025-12-01',
                'tipo_transporte_id': passagem_tipo_transporte_ids[2], 
                'responsavel_compra_id': cliente_ids[0],
                'valor': 450.00,
                'numero_assento': '12A',
                'codigo_reserva': 'BR001',
                'compra_realizada': True,
                'horario_partida': '08:00',
                'horario_chegada': '09:30'
            },
            {
                'viagem_id': viagem_ids[0],
                'origem': 'Rio de Janeiro',
                'destino': 'Salvador',
                'data_viagem': '2025-12-05',
                'tipo_transporte_id': passagem_tipo_transporte_ids[0], 
                'responsavel_compra_id': cliente_ids[1],
                'valor': 280.00,
                'numero_assento': '15',
                'codigo_reserva': 'BR002',
                'compra_realizada': False,
                'horario_partida': '22:00',
                'horario_chegada': '14:00'
            }
        ]
    
    @staticmethod
    def get_transportes_dados(tipo_transporte_ids):
        return [
            {
                'data': date(2025, 12, 1),
                'origem': 'São Paulo',
                'destino': 'Rio de Janeiro',
                'tipo_transporte_id': tipo_transporte_ids[0], 
                'compra_realizada': False
            },
            {
                'data': date(2025, 12, 5),
                'origem': 'Rio de Janeiro',
                'destino': 'Salvador',
                'tipo_transporte_id': tipo_transporte_ids[1], 
                'compra_realizada': True
            },
            {
                'data': date(2025, 12, 1),
                'origem': 'São Paulo',
                'destino': 'Recife',
                'tipo_transporte_id': tipo_transporte_ids[2],  
                'compra_realizada': False
            }
        ]
    
    @staticmethod
    def get_passeios_dados(viagem_ids, destino_ids):
        from datetime import time
        return [
            {
                'cidade': 'Rio de Janeiro',
                'atracao_turistica': 'Cristo Redentor e Pão de Açúcar',
                'horario_inicio': time(9, 0),  
                'horario_fim': time(17, 0),    
                'valor': 150.00,
                'pessoa_id': None,  
                'data_passeio': date(2025, 12, 2),
                'destino_id': destino_ids[0]   
            },
            {
                'cidade': 'Salvador',
                'atracao_turistica': 'Pelourinho e Mercado Modelo',
                'horario_inicio': time(14, 0),
                'horario_fim': time(18, 0),   
                'valor': 80.00,
                'pessoa_id': None, 
                'data_passeio': date(2025, 12, 6),
                'destino_id': destino_ids[1]  
            },
            {
                'cidade': 'Natal',
                'atracao_turistica': 'Dunas de Genipabu',
                'horario_inicio': time(14, 0),
                'horario_fim': time(18, 0),
                'valor': 120.00,
                'pessoa_id': None,  
                'data_passeio': date(2025, 11, 12),
                'destino_id': destino_ids[4]  
            },
            {
                'cidade': 'João Pessoa',
                'atracao_turistica': 'Ponta do Seixas',
                'horario_inicio': time(16, 0),
                'horario_fim': time(18, 0),
                'valor': 60.00,
                'pessoa_id': None,
                'data_passeio': date(2025, 11, 15),
                'destino_id': destino_ids[5]  
            },
            {
                'cidade': 'Salvador',
                'atracao_turistica': 'Praia do Forte',
                'horario_inicio': time(10, 0),
                'horario_fim': time(16, 0),
                'valor': 100.00,
                'pessoa_id': None, 
                'data_passeio': date(2025, 10, 8),
                'destino_id': destino_ids[1]  
            },
            {
                'cidade': 'Salvador',
                'atracao_turistica': 'Capoeira no Terreiro de Jesus',
                'horario_inicio': time(18, 0),
                'horario_fim': time(20, 0),
                'valor': 40.00,
                'pessoa_id': None,  
                'data_passeio': date(2025, 10, 10),
                'destino_id': destino_ids[1]  
            }
        ]
    
    @staticmethod
    def get_pagamentos_dados(cliente_ids):
        return [
            {
                'data': date(2025, 9, 1),
                'valor': 500.00,
                'pessoa_id': cliente_ids[0],
                'viagem_id': None,  
                'tipo': 'dinheiro'
            },
            {
                'data': date(2025, 9, 2),
                'valor': 800.00,
                'pessoa_id': cliente_ids[1],
                'viagem_id': None, 
                'tipo': 'cartao',
                'numero_cartao': '1234567812345678',
                'bandeira': 'Visa'
            },
            {
                'data': date(2025, 9, 3),
                'valor': 1200.00,
                'pessoa_id': cliente_ids[2],
                'viagem_id': None,  
                'tipo': 'pix',
                'cpf_pagador': '11122233344'
            },
            {
                'data': date(2025, 9, 4),
                'valor': 300.00,
                'pessoa_id': cliente_ids[0],
                'viagem_id': None,  
                'tipo': 'pix',
                'cpf_pagador': '12345678901'
            }
        ]
