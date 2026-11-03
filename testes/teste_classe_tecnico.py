import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
Tecnico = classes.Tecnico

# Criando um objeto da classe Tecnico
tecnico1 = Tecnico(
    "José",
    "MET-5001",
    "Metrologia",
    "Metrologista"
)

# Chamando o método do objeto
tecnico1.exibir_dados()