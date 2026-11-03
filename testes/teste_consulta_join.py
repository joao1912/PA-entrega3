import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
BancoDados = classes.BancoDados

# Conecta ao banco de dados de testes.
banco = BancoDados("schulz_calibracao_testes.db")

try:
    # Consulta as medições com os dados relacionados.
    medicoes = banco.listar_medicoes_detalhadas()

    # Exibe os resultados das medições.
    for medicao in medicoes:
        print("\nRELATÓRIO DE MEDIÇÃO")
        print("ID:", medicao["id_medicao"])
        print("Técnico:", medicao["nome_tecnico"])
        print("Equipamento:", medicao["denominacao"])
        print("Código TAG:", medicao["codigo_tag"])
        print("Ordem de serviço:", medicao["ordem_servico"])
        print("Parâmetro:", medicao["parametro_avaliado"])
        print(f"Média: {medicao['media_obtida']:.4f}")
        print(f"Desvio: {medicao['desvio_calculado']:.4f}")
        print("Status:", medicao["status_conformidade"])

except ValueError as erro:
    # Erros de validação ou do banco (ex.: matrícula repetida).
    print("ERRO:", erro)

finally:
    # Encerra a conexão com SQLite.
    banco.fechar_conexao()