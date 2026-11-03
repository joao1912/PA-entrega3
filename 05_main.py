import importlib

# Importa o arquivo 04_classes.py. O importlib é necessário porque
# o Python não aceita "from 04_classes import ..." (nome começa com número).
classes = importlib.import_module("04_classes")
Tecnico = classes.Tecnico
Equipamento = classes.Equipamento
Medicao = classes.Medicao
BancoDados = classes.BancoDados


# Função principal do sistema.
def main():

    # Conecta ao banco de dados de testes.
    banco = BancoDados("schulz_calibracao_testes.db")

    try:
        print("=== SISTEMA DE CALIBRAÇÃO SCHULZ ===")

        # Cria um objeto da classe Tecnico.
        tecnico = Tecnico(
            "Técnico MVP",
            "MVP-TEC-001",
            "Metrologia",
            "Metrologista"
        )

        # Verifica se o técnico já está cadastrado.
        existente = next(
            (t for t in banco.listar_tecnicos()
             if t["matricula"] == tecnico.matricula),
            None
        )

        if existente is None:
            banco.cadastrar_tecnico(tecnico)
        else:
            tecnico.id_tecnico = existente["id_tecnico"]

        # Cria um objeto da classe Equipamento.
        equipamento = Equipamento(
            "MVP-EQ-001",
            "Equipamento de Demonstração",
            "Schulz",
            "Modelo MVP",
            "SN-MVP-001",
            "Metrologia"
        )

        # Verifica se o equipamento já está cadastrado.
        existente = next(
            (e for e in banco.listar_equipamentos()
             if e["codigo_tag"] == equipamento.codigo_tag),
            None
        )

        if existente is None:
            banco.cadastrar_equipamento(equipamento)
        else:
            equipamento.id_equipamento = existente["id_equipamento"]

        # Cria um objeto da classe Medicao.
        medicao = Medicao(
            nominal=6.075,
            medida_1=6.078,
            medida_2=6.080,
            tolerancia_inferior=-0.010,
            tolerancia_superior=0.010,
            id_tecnico=tecnico.id_tecnico,
            id_equipamento=equipamento.id_equipamento,
            ordem_servico="OS-MVP-001",
            data_medicao="2026-11-01",
            temperatura_ambiente=20.0,
            parametro_avaliado="DIAMETRO_MVP",
            incerteza_expandida_u=0.002
        )

        # Evita repetir a mesma medição de demonstração.
        existe_medicao = any(
            m["ordem_servico"] == medicao.ordem_servico
            and m["parametro_avaliado"] == medicao.parametro_avaliado
            and m["id_equipamento"] == equipamento.id_equipamento
            for m in banco.listar_medicoes()
        )

        if not existe_medicao:
            banco.cadastrar_medicao(medicao)

        # Consulta as medições utilizando JOIN.
        medicoes = banco.listar_medicoes_detalhadas()

        # Exibe o relatório no terminal.
        print("\n=== RELATÓRIO DE CALIBRAÇÃO ===")

        for registro in medicoes:
            if (registro["ordem_servico"] == "OS-MVP-001"
                    and registro["codigo_tag"] == "MVP-EQ-001"):

                print("Técnico:", registro["nome_tecnico"])
                print("Equipamento:", registro["denominacao"])
                print("TAG:", registro["codigo_tag"])
                print("Ordem de serviço:", registro["ordem_servico"])
                print("Parâmetro:", registro["parametro_avaliado"])
                print(f"Média: {registro['media_obtida']:.4f}")
                print(f"Desvio: {registro['desvio_calculado']:.4f}")
                print("Status:", registro["status_conformidade"])

    except ValueError as erro:
        # Erros de validação ou do banco (ex.: matrícula repetida).
        print("ERRO:", erro)

    finally:
        # Encerra a conexão com SQLite.
        banco.fechar_conexao()


# Executa a função principal.
if __name__ == "__main__":
    main()
