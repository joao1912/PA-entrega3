# Sistema de Calibração Schulz - MVP Parte 1 (AV03)

Projeto Aplicado I - UniSENAI / Schulz S.A.
Equipe: Gabriel Medeiros, Eduarda Bento Rocha, Vitória Luiza Pacheco, Joao Pedro Silva Teixeira

Sistema em Python, com Programação Orientada a Objetos e banco SQLite, para registrar técnicos, equipamentos e medições do laboratório de metrologia e validar a conformidade das medições.

## Entregáveis

| Arquivo | Conteúdo |
|---|---|
| `04_classes.py` | Classes `Tecnico`, `Equipamento`, `Medicao` e `BancoDados` (CRUD com `sqlite3`) |
| `05_main.py` | Demonstração: cria os objetos, grava no banco, consulta com `JOIN` e exibe o relatório |
| `06_mvp_parte1.md` | Documentação técnica do MVP |

## Estrutura

```
04_classes.py, 05_main.py, 06_mvp_parte1.md
banco/    script SQL (03_banco.sql), criar_banco.py e bancos .db
testes/   testes de cada classe e de cada operação CRUD
docs/     documentação da AV02, roteiro da AV03 e geradores dos .md
```

## Como executar

Requer Python 3. Não há bibliotecas externas. Rode os comandos a partir da pasta raiz do projeto.

```bash
python 05_main.py
python -m testes.teste_classe_medicao
```

Os testes rodam com `python -m testes.<nome_do_teste>`, sem `.py` no final.

> Atenção: `python banco/criar_banco.py` apaga e recria o banco principal (`banco/schulz_calibracao.db`). O `05_main.py` e os testes usam `banco/schulz_calibracao_testes.db`.
