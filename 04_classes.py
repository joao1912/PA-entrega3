# ============================================================
# PROJETO APLICADO I - UNISENAI / SCHULZ S.A.
# AV 03 - MVP Parte 1: classes do sistema (POO + SQLite)
# Arquivo: 04_classes.py
# ============================================================
# Para importar (o nome começa com número, então use importlib):
#   classes = importlib.import_module("04_classes")
# ============================================================

import sqlite3
import statistics
from pathlib import Path


# Profissional que realiza as calibrações.
class Tecnico:

    def __init__(self, nome, matricula, setor, cargo_perfil, id_tecnico=None):
        self.nome = nome
        self.matricula = matricula
        self.setor = setor
        self.cargo_perfil = cargo_perfil
        self.id_tecnico = id_tecnico

    def exibir_dados(self):
        print("ID:", self.id_tecnico)
        print("Nome:", self.nome)
        print("Matrícula:", self.matricula)
        print("Setor:", self.setor)
        print("Cargo:", self.cargo_perfil)


# Instrumento ou dispositivo calibrado.
class Equipamento:

    def __init__(self, codigo_tag, denominacao, fabricante, modelo=None, numero_serie=None, setor_localizacao=None, id_equipamento=None):
        self.codigo_tag = codigo_tag
        self.denominacao = denominacao
        self.fabricante = fabricante
        self.modelo = modelo
        self.numero_serie = numero_serie
        self.setor_localizacao = setor_localizacao
        self.id_equipamento = id_equipamento

    def exibir_dados(self):
        print("ID:", self.id_equipamento)
        print("Código TAG:", self.codigo_tag)
        print("Denominação:", self.denominacao)
        print("Fabricante:", self.fabricante)
        print("Modelo:", self.modelo)
        print("Número de série:", self.numero_serie)
        print("Setor:", self.setor_localizacao)


# Leituras de uma característica, cálculos e validação de tolerância.
class Medicao:

    def __init__(self, nominal, medida_1, medida_2,
                 tolerancia_inferior, tolerancia_superior,
                 id_tecnico=None, id_equipamento=None,
                 ordem_servico=None, data_medicao=None,
                 temperatura_ambiente=None, parametro_avaliado=None,
                 incerteza_expandida_u=None, id_medicao=None):

        # Regra de negócio: a tolerância inferior não pode passar a superior.
        if tolerancia_inferior > tolerancia_superior:
            raise ValueError("Tolerância inferior maior que a superior!")

        # Encapsulamento: o "_" indica atributo interno da classe.
        # O acesso de fora é feito pelas @property abaixo (somente leitura),
        # assim os limites usados na validação não são alterados por engano.
        self._nominal = nominal
        self._tolerancia_inferior = tolerancia_inferior
        self._tolerancia_superior = tolerancia_superior

        self.medida_1 = medida_1
        self.medida_2 = medida_2

        self.id_tecnico = id_tecnico
        self.id_equipamento = id_equipamento
        self.ordem_servico = ordem_servico
        self.data_medicao = data_medicao
        self.temperatura_ambiente = temperatura_ambiente
        self.parametro_avaliado = parametro_avaliado

        self.incerteza_expandida_u = incerteza_expandida_u
        self.id_medicao = id_medicao

    @property
    def nominal(self):
        return self._nominal

    @property
    def tolerancia_inferior(self):
        return self._tolerancia_inferior

    @property
    def tolerancia_superior(self):
        return self._tolerancia_superior

    def calcular_media(self):
        return (self.medida_1 + self.medida_2) / 2

    # Desvio da média em relação ao valor nominal.
    def calcular_desvio(self):
        return self.calcular_media() - self.nominal

    # Desvio-padrão amostral das duas leituras.
    def calcular_desvio_padrao(self):
        return statistics.stdev([
            self.medida_1,
            self.medida_2
        ])

    # CONFORME se a média estiver dentro de nominal + tolerâncias.
    def validar_conformidade(self):
        media = self.calcular_media()
        limite_inferior = self.nominal + self.tolerancia_inferior
        limite_superior = self.nominal + self.tolerancia_superior

        if limite_inferior <= media <= limite_superior:
            return "CONFORME"
        else:
            return "NAO_CONFORME"


# Conexão com o SQLite e operações CRUD.
class BancoDados:

    # O banco é procurado na pasta "banco" do projeto.
    def __init__(self, nome_banco="schulz_calibracao.db"):
        pasta_banco = Path(__file__).resolve().parent / "banco"
        caminho_banco = pasta_banco / nome_banco

        if not caminho_banco.exists():
            raise FileNotFoundError(
                "Banco de dados não encontrado!"
            )

        self.conexao = sqlite3.connect(caminho_banco)

        # Permite acessar as colunas pelo nome: registro["nome"]
        self.conexao.row_factory = sqlite3.Row

        # O SQLite só aplica as chaves estrangeiras com isso ativado.
        self.conexao.execute("PRAGMA foreign_keys = ON")

    # ---------- SELECT ----------

    def listar_tecnicos(self):
        cursor = self.conexao.execute("""
            SELECT *
            FROM tecnicos
        """)
        return cursor.fetchall()

    def listar_equipamentos(self):
        cursor = self.conexao.execute("""
            SELECT *
            FROM equipamentos
        """)
        return cursor.fetchall()

    def listar_medicoes(self):
        cursor = self.conexao.execute("""
            SELECT *
            FROM medicoes
        """)
        return cursor.fetchall()

    # JOIN das três tabelas, usado no relatório de calibração.
    def listar_medicoes_detalhadas(self):
        cursor = self.conexao.execute("""
            SELECT
                m.id_medicao,
                t.nome AS nome_tecnico,
                e.codigo_tag,
                e.denominacao,
                m.ordem_servico,
                m.data_medicao,
                m.parametro_avaliado,
                m.media_obtida,
                m.desvio_calculado,
                m.status_conformidade
            FROM medicoes AS m
            INNER JOIN tecnicos AS t
                ON m.id_tecnico = t.id_tecnico
            INNER JOIN equipamentos AS e
                ON m.id_equipamento = e.id_equipamento
            ORDER BY m.id_medicao
        """)
        return cursor.fetchall()

    # ---------- INSERT ----------
    # Os "?" evitam montar o SQL com os valores direto no texto.
    # cursor.lastrowid traz o ID gerado pelo SQLite.
    #
    # Tratamento de erros SQL: se o banco recusar o registro
    # (UNIQUE, NOT NULL, CHECK ou chave estrangeira), o SQLite lança
    # sqlite3.IntegrityError. Nesse caso desfazemos a operação com
    # rollback() e avisamos com um ValueError de mensagem clara.

    def cadastrar_tecnico(self, tecnico):
        try:
            cursor = self.conexao.execute("""
                INSERT INTO tecnicos (nome, matricula, setor, cargo_perfil)
                VALUES (?, ?, ?, ?)
            """, (
                tecnico.nome,
                tecnico.matricula,
                tecnico.setor,
                tecnico.cargo_perfil
            ))
            self.conexao.commit()
        except sqlite3.IntegrityError as erro:
            self.conexao.rollback()
            raise ValueError(f"Não foi possível cadastrar o técnico: {erro}")

        tecnico.id_tecnico = cursor.lastrowid
        return tecnico.id_tecnico

    def cadastrar_equipamento(self, equipamento):
        try:
            cursor = self.conexao.execute("""
                INSERT INTO equipamentos (
                    codigo_tag, denominacao, fabricante,
                    modelo, numero_serie, setor_localizacao
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                equipamento.codigo_tag,
                equipamento.denominacao,
                equipamento.fabricante,
                equipamento.modelo,
                equipamento.numero_serie,
                equipamento.setor_localizacao
            ))
            self.conexao.commit()
        except sqlite3.IntegrityError as erro:
            self.conexao.rollback()
            raise ValueError(f"Não foi possível cadastrar o equipamento: {erro}")

        equipamento.id_equipamento = cursor.lastrowid
        return equipamento.id_equipamento

    # Média, desvio e status são calculados pela classe Medicao.
    def cadastrar_medicao(self, medicao):
        obrigatorios = (
            medicao.id_tecnico,
            medicao.id_equipamento,
            medicao.ordem_servico,
            medicao.data_medicao,
            medicao.temperatura_ambiente,
            medicao.parametro_avaliado,
            medicao.incerteza_expandida_u
        )

        if any(valor is None for valor in obrigatorios):
            raise ValueError("Dados obrigatórios da medição não informados!")

        try:
            cursor = self.conexao.execute("""
                INSERT INTO medicoes (
                    id_equipamento, id_tecnico,
                    ordem_servico, data_medicao,
                    temperatura_ambiente, parametro_avaliado,
                    valor_nominal, tolerancia_superior,
                    tolerancia_inferior, medida_1, medida_2,
                    media_obtida, desvio_calculado,
                    incerteza_expandida_u, status_conformidade
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                medicao.id_equipamento,
                medicao.id_tecnico,
                medicao.ordem_servico,
                medicao.data_medicao,
                medicao.temperatura_ambiente,
                medicao.parametro_avaliado,
                medicao.nominal,
                medicao.tolerancia_superior,
                medicao.tolerancia_inferior,
                medicao.medida_1,
                medicao.medida_2,
                medicao.calcular_media(),
                medicao.calcular_desvio(),
                medicao.incerteza_expandida_u,
                medicao.validar_conformidade()
            ))
            self.conexao.commit()
        except sqlite3.IntegrityError as erro:
            self.conexao.rollback()
            raise ValueError(f"Não foi possível cadastrar a medição: {erro}")

        medicao.id_medicao = cursor.lastrowid
        return medicao.id_medicao

    # ---------- UPDATE ----------
    # Retornam quantos registros foram alterados (cursor.rowcount).

    def atualizar_tecnico(self, tecnico):
        if tecnico.id_tecnico is None:
            raise ValueError("Técnico sem ID para atualização!")

        try:
            cursor = self.conexao.execute("""
                UPDATE tecnicos
                SET nome = ?, matricula = ?, setor = ?, cargo_perfil = ?
                WHERE id_tecnico = ?
            """, (
                tecnico.nome,
                tecnico.matricula,
                tecnico.setor,
                tecnico.cargo_perfil,
                tecnico.id_tecnico
            ))
            self.conexao.commit()
        except sqlite3.IntegrityError as erro:
            self.conexao.rollback()
            raise ValueError(f"Não foi possível atualizar o técnico: {erro}")
        return cursor.rowcount

    def atualizar_equipamento(self, equipamento):
        if equipamento.id_equipamento is None:
            raise ValueError("Equipamento sem ID para atualização!")

        try:
            cursor = self.conexao.execute("""
                UPDATE equipamentos
                SET codigo_tag = ?, denominacao = ?,
                    fabricante = ?, modelo = ?,
                    numero_serie = ?, setor_localizacao = ?
                WHERE id_equipamento = ?
            """, (
                equipamento.codigo_tag,
                equipamento.denominacao,
                equipamento.fabricante,
                equipamento.modelo,
                equipamento.numero_serie,
                equipamento.setor_localizacao,
                equipamento.id_equipamento
            ))
            self.conexao.commit()
        except sqlite3.IntegrityError as erro:
            self.conexao.rollback()
            raise ValueError(f"Não foi possível atualizar o equipamento: {erro}")
        return cursor.rowcount

    def atualizar_medicao(self, medicao):
        if medicao.id_medicao is None:
            raise ValueError("Medição sem ID para atualização!")

        obrigatorios = (
            medicao.id_tecnico,
            medicao.id_equipamento,
            medicao.ordem_servico,
            medicao.data_medicao,
            medicao.temperatura_ambiente,
            medicao.parametro_avaliado,
            medicao.incerteza_expandida_u
        )

        if any(valor is None for valor in obrigatorios):
            raise ValueError("Dados obrigatórios não informados!")

        try:
            cursor = self.conexao.execute("""
                UPDATE medicoes
                SET id_equipamento = ?,
                    id_tecnico = ?,
                    ordem_servico = ?,
                    data_medicao = ?,
                    temperatura_ambiente = ?,
                    parametro_avaliado = ?,
                    valor_nominal = ?,
                    tolerancia_superior = ?,
                    tolerancia_inferior = ?,
                    medida_1 = ?,
                    medida_2 = ?,
                    media_obtida = ?,
                    desvio_calculado = ?,
                    incerteza_expandida_u = ?,
                    status_conformidade = ?
                WHERE id_medicao = ?
            """, (
                medicao.id_equipamento,
                medicao.id_tecnico,
                medicao.ordem_servico,
                medicao.data_medicao,
                medicao.temperatura_ambiente,
                medicao.parametro_avaliado,
                medicao.nominal,
                medicao.tolerancia_superior,
                medicao.tolerancia_inferior,
                medicao.medida_1,
                medicao.medida_2,
                medicao.calcular_media(),
                medicao.calcular_desvio(),
                medicao.incerteza_expandida_u,
                medicao.validar_conformidade(),
                medicao.id_medicao
            ))
            self.conexao.commit()
        except sqlite3.IntegrityError as erro:
            self.conexao.rollback()
            raise ValueError(f"Não foi possível atualizar a medição: {erro}")
        return cursor.rowcount

    # ---------- DELETE ----------
    # Técnico e equipamento com medições vinculadas não podem ser excluídos.

    def excluir_medicao(self, id_medicao):
        if id_medicao is None:
            raise ValueError("ID da medição não informado!")

        cursor = self.conexao.execute("""
            DELETE FROM medicoes
            WHERE id_medicao = ?
        """, (id_medicao,))
        self.conexao.commit()
        return cursor.rowcount

    def excluir_tecnico(self, id_tecnico):
        if id_tecnico is None:
            raise ValueError("ID do técnico não informado!")

        cursor = self.conexao.execute("""
            SELECT 1 FROM medicoes
            WHERE id_tecnico = ?
            LIMIT 1
        """, (id_tecnico,))

        if cursor.fetchone() is not None:
            raise ValueError("Técnico possui medições vinculadas!")

        cursor = self.conexao.execute("""
            DELETE FROM tecnicos
            WHERE id_tecnico = ?
        """, (id_tecnico,))
        self.conexao.commit()
        return cursor.rowcount

    def excluir_equipamento(self, id_equipamento):
        if id_equipamento is None:
            raise ValueError("ID do equipamento não informado!")

        cursor = self.conexao.execute("""
            SELECT 1 FROM medicoes
            WHERE id_equipamento = ?
            LIMIT 1
        """, (id_equipamento,))

        if cursor.fetchone() is not None:
            raise ValueError("Equipamento possui medições vinculadas!")

        cursor = self.conexao.execute("""
            DELETE FROM equipamentos
            WHERE id_equipamento = ?
        """, (id_equipamento,))
        self.conexao.commit()
        return cursor.rowcount

    # ---------- Conexão ----------

    def fechar_conexao(self):
        self.conexao.close()
