from views.sistema_view import SistemaViagensView


def main():
    try:
        sistema = SistemaViagensView()
        sistema.executar()
    except Exception as e:
        print(f"Erro crítico no sistema: {e}")


if __name__ == "__main__":
    main()
