import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
Equipamento = classes.Equipamento

# Cria um objeto para testar a classe Equipamento.
equipamento1 = Equipamento(
    "500.011",
    "Máquina de Medição por Coordenadas",
    "Carl Zeiss",
    "Contura G2",
    "SN-001",
    "Metrologia"
)

# Exibe os dados do equipamento criado.
equipamento1.exibir_dados()