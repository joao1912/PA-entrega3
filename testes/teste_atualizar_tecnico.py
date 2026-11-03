import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
Tecnico = classes.Tecnico
BancoDados = classes.BancoDados

# Cria um técnico com o ID de um registro existente.
tecnico1 = Tecnico(
    "Técnico Teste",
    "TESTE-AV03-001",
    "Controle de Qualidade",
    "Metrologista",
    id_tecnico=4
)

# Conecta ao banco de testes.
banco = BancoDados("schulz_calibracao_testes.db")

try:
    # Atualiza os dados do técnico no SQLite.
    registros = banco.atualizar_tecnico(tecnico1)

    print("Registros atualizados:", registros)

    # Consulta os dados após a atualização.
    for tecnico in banco.listar_tecnicos():
        if tecnico["id_tecnico"] == 4:
            print("Nome:", tecnico["nome"])
            print("Setor:", tecnico["setor"])

except ValueError as erro:
    # Erros de validação ou do banco (ex.: matrícula repetida).
    print("ERRO:", erro)

finally:
    # Encerra a conexão.
    banco.fechar_conexao()