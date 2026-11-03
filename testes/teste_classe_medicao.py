import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
Medicao = classes.Medicao

# Cria uma medição dentro dos limites de tolerância.
medicao1 = Medicao(6.075, 6.078, 6.080, -0.010, 0.010)

# Cria uma medição fora dos limites de tolerância.
medicao2 = Medicao(6.075, 6.090, 6.092, -0.010, 0.010)

# Exibe os resultados das duas medições.
print("MEDIÇÃO 1")
print(f"Média: {medicao1.calcular_media():.4f}")
print(f"Desvio: {medicao1.calcular_desvio():.4f}")
print("Status:", medicao1.validar_conformidade())

print("\nMEDIÇÃO 2")
print(f"Média: {medicao2.calcular_media():.4f}")
print(f"Desvio: {medicao2.calcular_desvio():.4f}")
print("Status:", medicao2.validar_conformidade())
