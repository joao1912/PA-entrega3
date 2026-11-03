import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
Medicao = classes.Medicao
BancoDados = classes.BancoDados

# Conecta ao banco de testes.
banco = BancoDados("schulz_calibracao_testes.db")

try:
    # Localiza a medição cadastrada anteriormente.
    registro = next(
        (m for m in banco.listar_medicoes()
         if m["id_medicao"] == 4),
        None
    )

    if registro is None:
        print("Medição de teste não encontrada!")

    else:
        # Cria o objeto com novas leituras.
        medicao1 = Medicao(
            nominal=registro["valor_nominal"],
            medida_1=6.090,
            medida_2=6.092,
            tolerancia_inferior=registro["tolerancia_inferior"],
            tolerancia_superior=registro["tolerancia_superior"],
            id_tecnico=registro["id_tecnico"],
            id_equipamento=registro["id_equipamento"],
            ordem_servico=registro["ordem_servico"],
            data_medicao=registro["data_medicao"],
            temperatura_ambiente=registro["temperatura_ambiente"],
            parametro_avaliado=registro["parametro_avaliado"],
            incerteza_expandida_u=registro["incerteza_expandida_u"],
            id_medicao=4
        )

        # Atualiza a medição no SQLite.
        registros = banco.atualizar_medicao(medicao1)

        print("Registros atualizados:", registros)

        # Confirma os resultados gravados no banco.
        for medicao in banco.listar_medicoes():
            if medicao["id_medicao"] == 4:
                print(f"Média: {medicao['media_obtida']:.4f}")
                print(f"Desvio: {medicao['desvio_calculado']:.4f}")
                print("Status:", medicao["status_conformidade"])

except ValueError as erro:
    # Erros de validação ou do banco (ex.: matrícula repetida).
    print("ERRO:", erro)

finally:
    # Encerra a conexão.
    banco.fechar_conexao()