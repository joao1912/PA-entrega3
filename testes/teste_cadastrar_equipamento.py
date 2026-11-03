import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
Equipamento = classes.Equipamento
BancoDados = classes.BancoDados

# Cria um equipamento para testar o cadastro.
equipamento1 = Equipamento(
    "TESTE-EQ-AV03-001",
    "Equipamento de Teste",
    "Schulz",
    "Modelo Teste",
    "SN-TESTE-001",
    "Metrologia"
)

# Conecta ao banco de testes.
banco = BancoDados("schulz_calibracao_testes.db")

try:
    # Cadastra o equipamento no SQLite.
    id_gerado = banco.cadastrar_equipamento(equipamento1)

    print("Equipamento cadastrado com sucesso!")
    print("ID gerado:", id_gerado)

    # Consulta o equipamento cadastrado.
    equipamentos = banco.listar_equipamentos()

    for equipamento in equipamentos:
        if equipamento["id_equipamento"] == id_gerado:
            print("TAG:", equipamento["codigo_tag"])
            print("Denominação:", equipamento["denominacao"])

except ValueError as erro:
    # Erros de validação ou do banco (ex.: matrícula repetida).
    print("ERRO:", erro)

finally:
    # Encerra a conexão com SQLite.
    banco.fechar_conexao()
