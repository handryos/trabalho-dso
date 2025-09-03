## � Funcionalidades Principais

- **Gestão de Clientes**: Cadastro completo com validação de dados
- **Gestão de Empresas**: Controle de empresas parceiras de transporte
- **Planejamento de Viagens**: Criação de roteiros com múltiplos destinos ordenados
- **Sistema de Passagens**: Controle completo de tickets e reservas
- **Gestão de Transportes**: Diferentes tipos de transporte por empresa
- **Controle de Passeios**: Atividades turísticas por destino
- **Sistema de Pagamentos**: Multiple formas de pagamento com Strategy Pattern
- **Relatórios**: Geração de relatórios detalhados

## 📋 Características Técnicas Implementadas

### ✅ Padrões de Design
- **Strategy Pattern**: Sistema de pagamentos com múltiplas estratégias
- **MVC Pattern**: Separação clara de responsabilidades
- **Repository Pattern**: Controladores como repositórios de dados

### ✅ Associação, Agregação e Composição
- **Associação**: Pessoa ↔ Passeio, Pessoa ↔ Viagem
- **Agregação**: Viagem ↔ Destino (viagem agrupa destinos existentes)
- **Composição**: Viagem → DestinoViagem (ordem dos destinos na viagem)

### ✅ Strategy Pattern para Pagamentos
- **Interface Abstrata**: `StrategyPagamento`
- **Strategies Concretas**: 
  - `StrategyPagamentoDinheiro` 
  - `StrategyPagamentoPix` 
  - `StrategyPagamentoCartao` 
- **Context**: Classe `Pagamento` que usa as strategies

### ✅ Herança e Polimorfismo
- **Classes Base Abstratas**: `BaseController`, `BaseView`
- **Herança**: Todos os controladores herdam funcionalidades comuns
- **Polimorfismo**: Métodos abstratos implementados diferentemente

### ✅ Tratamento Robusto de Exceções
- Exceções customizadas específicas do domínio
- Validação de dados de entrada
- Tratamento gracioso de erros
- Mensagens de erro informativas

## 🏗️ Estrutura do Projeto

```
dso-work/
├── models/                     # Modelos de dados (Model)
│   ├── pessoa.py              # Entidade Cliente/Pessoa
│   ├── empresa.py             # Entidade Empresa de Transporte
│   ├── destino.py             # Entidade Destino Turístico
│   ├── destino_viagem.py      # Relacionamento Viagem-Destino com ordem
│   ├── viagem.py              # Entidade Viagem
│   ├── transporte.py          # Entidade Transporte/Trecho
│   ├── tipo_transporte.py     # Tipos de Transporte por Empresa
│   ├── passagem.py            # Sistema de Passagens
│   ├── passeio.py             # Atividades Turísticas
│   ├── pagamento.py           # Sistema de Pagamentos com Strategy
│   ├── tipo_pagamento.py      # Enum para Tipos de Pagamento
│   ├── strategy_pagamento.py  # Interface Strategy para Pagamentos
│   └── strategies_pagamento.py # Implementações concretas das strategies
├── controllers/               # Controladores (Controller)
│   ├── base_controller.py     # Controlador base abstrato
│   ├── pessoa_controller.py   # CRUD de Pessoas
│   ├── empresa_controller.py  # CRUD de Empresas
│   ├── destino_controller.py  # CRUD de Destinos
│   ├── viagem_controller.py   # CRUD de Viagens + Participantes
│   ├── transporte_controller.py # CRUD de Transportes e Tipos
│   ├── passagem_controller.py # CRUD de Passagens
│   ├── passeio_controller.py  # CRUD de Passeios
│   └── pagamento_controller.py # CRUD de Pagamentos com Strategy
├── views/                     # Interface do usuário (View)
│   ├── base_view.py          # View base com utilitários
│   └── sistema_view.py       # Interface principal do sistema
├── services/                  # Serviços de negócio
│   └── relatorio_service.py  # Geração de relatórios
├── utils/                     # Utilitários
│   ├── __init__.py
│   └── mocked_data.py        # Dados mockados para testes
├── exceptions/                # Exceções 
│   ├── __init__.py
│   └── custom_exceptions.py  # Todas as exceções do domínio
└── main.py                   # Ponto de entrada da aplicação

```

## 🚀 Como Executar

### 1. Executar o Sistema Completo
```bash
cd dso-work

python3 main.py
```
