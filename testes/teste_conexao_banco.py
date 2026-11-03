import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
BancoDados = classes.BancoDados

# Cria um objeto da classe BancoDados
banco = BancoDados()

try:
    # Consulta os técnicos cadastrados
    tecnicos = banco.listar_tecnicos()

    print("TÉCNICOS CADASTRADOS:")

    for tecnico in tecnicos:
        print(tecnico["nome"])

    # Consulta os equipamentos cadastrados
    equipamentos = banco.listar_equipamentos()

    print("\nEQUIPAMENTOS CADASTRADOS:")

    for equipamento in equipamentos:
        print(equipamento["codigo_tag"])

    # Consulta as medições cadastradas
    medicoes = banco.listar_medicoes()

    print("\nMEDIÇÕES CADASTRADAS:")

    for medicao in medicoes:
        print(medicao["parametro_avaliado"])

except ValueError as erro:
    # Erros de validação ou do banco (ex.: matrícula repetida).
    print("ERRO:", erro)

finally:
    # Encerra a conexão mesmo se ocorrer um erro
    banco.fechar_conexao()