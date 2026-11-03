import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
Tecnico = classes.Tecnico
BancoDados = classes.BancoDados

# Cria um objeto da classe Tecnico.
tecnico1 = Tecnico(
    "Técnico Teste",
    "TESTE-AV03-001",
    "Metrologia",
    "Metrologista"
)

# Conecta ao banco de dados de testes.
banco = BancoDados("schulz_calibracao_testes.db")

try:
    # Cadastra o técnico e recupera seu ID.
    id_gerado = banco.cadastrar_tecnico(tecnico1)

    print("Técnico cadastrado com sucesso!")
    print("ID gerado:", id_gerado)

    # Consulta os técnicos cadastrados.
    tecnicos = banco.listar_tecnicos()

    for tecnico in tecnicos:
        if tecnico["id_tecnico"] == id_gerado:
            print("Nome:", tecnico["nome"])
            print("Matrícula:", tecnico["matricula"])

except ValueError as erro:
    # Erros de validação ou do banco (ex.: matrícula repetida).
    print("ERRO:", erro)

finally:
    # Encerra a conexão com SQLite.
    banco.fechar_conexao()
