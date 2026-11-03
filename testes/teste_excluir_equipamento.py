import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
Equipamento = classes.Equipamento
BancoDados = classes.BancoDados

# Conecta ao banco de dados de testes.
banco = BancoDados("schulz_calibracao_testes.db")

try:
    # Cria um equipamento temporário.
    equipamento1 = Equipamento(
        codigo_tag="TESTE-DELETE-EQ-001",
        denominacao="Equipamento Temporário",
        fabricante="Schulz",
        modelo="Modelo Teste",
        numero_serie="SN-DELETE-001",
        setor_localizacao="Metrologia"
    )

    # Cadastra o equipamento no SQLite.
    id_gerado = banco.cadastrar_equipamento(equipamento1)

    print("Equipamento cadastrado. ID:", id_gerado)

    # Exclui o equipamento temporário.
    registros = banco.excluir_equipamento(id_gerado)

    print("Registros excluídos:", registros)

    # Consulta os equipamentos após a exclusão.
    equipamentos = banco.listar_equipamentos()

    # Verifica se o equipamento ainda existe.
    existe = any(
        equipamento["id_equipamento"] == id_gerado
        for equipamento in equipamentos
    )

    print("Equipamento ainda existe?", "SIM" if existe else "NÃO")

except ValueError as erro:
    # Erros de validação ou do banco (ex.: matrícula repetida).
    print("ERRO:", erro)

finally:
    # Encerra a conexão com SQLite.
    banco.fechar_conexao()