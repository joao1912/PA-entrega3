import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
Tecnico = classes.Tecnico
BancoDados = classes.BancoDados

# Conecta ao banco de dados de testes.
banco = BancoDados("schulz_calibracao_testes.db")

try:
    # Cria um técnico temporário.
    tecnico1 = Tecnico(
        "Técnico Temporário",
        "TESTE-DELETE-TEC-001",
        "Metrologia",
        "Metrologista"
    )

    # Cadastra o técnico no SQLite.
    id_gerado = banco.cadastrar_tecnico(tecnico1)

    print("Técnico cadastrado. ID:", id_gerado)

    # Exclui o técnico temporário.
    registros = banco.excluir_tecnico(id_gerado)

    print("Registros excluídos:", registros)

    # Consulta os técnicos após a exclusão.
    tecnicos = banco.listar_tecnicos()

    # Verifica se o técnico ainda existe.
    existe = any(
        tecnico["id_tecnico"] == id_gerado
        for tecnico in tecnicos
    )

    print("Técnico ainda existe?", "SIM" if existe else "NÃO")

except ValueError as erro:
    # Erros de validação ou do banco (ex.: matrícula repetida).
    print("ERRO:", erro)

finally:
    # Encerra a conexão com SQLite.
    banco.fechar_conexao()