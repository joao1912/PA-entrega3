import sqlite3
from pathlib import Path

#============================================================
# Este script conecta o Python ao SQLite e executa os
# comandos SQL responsáveis pela criação das tabelas
# de técnicos, equipamentos e medições.
#
# ATENÇÃO: o 03_banco.sql possui DROP TABLE, então rodar
# este script APAGA e recria o banco principal.
# ============================================================

# Pasta onde este arquivo está (pasta "banco")
PASTA_BANCO = Path(__file__).resolve().parent

# Caminho do banco de dados
NOME_BANCO = PASTA_BANCO / "schulz_calibracao.db"

# Caminho do arquivo SQL
ARQUIVO_SQL = PASTA_BANCO / "03_banco.sql"


try:
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    with open(ARQUIVO_SQL, "r", encoding="utf-8") as f:
        script_sql = f.read()

    cursor.executescript(script_sql)
    conexao.commit()

    print("=" * 60)
    print(f"SUCESSO: Banco de dados '{NOME_BANCO}' gerado com sucesso!")
    print("As tabelas 'tecnicos', 'equipamentos' e 'medicoes' foram criadas.")
    print("=" * 60)

except Exception as e:
    print(f"ERRO ao executar o script DDL: {e}")

finally:
    conexao.close()