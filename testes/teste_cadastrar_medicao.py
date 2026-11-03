import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
Medicao = classes.Medicao
BancoDados = classes.BancoDados

# Cria uma medição com informações da calibração.
medicao1 = Medicao(
    nominal=6.075,
    medida_1=6.078,
    medida_2=6.080,
    tolerancia_inferior=-0.010,
    tolerancia_superior=0.010,
    id_tecnico=4,
    id_equipamento=3,
    ordem_servico="OS-TESTE-001",
    data_medicao="2026-11-01",
    temperatura_ambiente=20.0,
    parametro_avaliado="DIAMETRO_TESTE",
    incerteza_expandida_u=0.002
)

# Conecta ao banco de testes.
banco = BancoDados("schulz_calibracao_testes.db")

try:
    # Cadastra a medição.
    id_gerado = banco.cadastrar_medicao(medicao1)

    print("Medição cadastrada com sucesso!")
    print("ID:", id_gerado)
    print("Média:", medicao1.calcular_media())
    print("Desvio:", medicao1.calcular_desvio())
    print("Status:", medicao1.validar_conformidade())

except ValueError as erro:
    # Erros de validação ou do banco (ex.: matrícula repetida).
    print("ERRO:", erro)

finally:
    # Encerra a conexão com SQLite.
    banco.fechar_conexao()
