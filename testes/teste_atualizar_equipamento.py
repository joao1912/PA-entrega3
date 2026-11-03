import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
Equipamento = classes.Equipamento
BancoDados = classes.BancoDados

# Cria um equipamento com os dados atualizados.
equipamento1 = Equipamento(
    codigo_tag="TESTE-EQ-AV03-001",
    denominacao="Equipamento de Teste Atualizado",
    fabricante="Schulz",
    modelo="Modelo Teste",
    numero_serie="SN-TESTE-001",
    setor_localizacao="Controle de Qualidade",
    id_equipamento=3
)

# Conecta ao banco de dados de testes.
banco = BancoDados("schulz_calibracao_testes.db")

try:
    # Atualiza o equipamento no SQLite.
    registros = banco.atualizar_equipamento(equipamento1)

    print("Registros atualizados:", registros)

    # Consulta o equipamento após a atualização.
    for equipamento in banco.listar_equipamentos():
        if equipamento["id_equipamento"] == 3:
            print("TAG:", equipamento["codigo_tag"])
            print("Denominação:", equipamento["denominacao"])
            print("Setor:", equipamento["setor_localizacao"])

except ValueError as erro:
    # Erros de validação ou do banco (ex.: matrícula repetida).
    print("ERRO:", erro)

finally:
    # Encerra a conexão com o SQLite.
    banco.fechar_conexao()