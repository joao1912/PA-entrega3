# Documentação Técnica do MVP - Parte 1

**Unidade Curricular:** Projeto Aplicado I  
**Integrantes da Equipe:**  Gabriel Medeiros, Eduarda Bento Rocha, Vitória Luiza Pacheco, Joao Pedro Silva Teixeira
**Tema:**  Documentação Técnica do MVP - Parte 1 (Entrega 3)
**Professor:** Prof. MSc. Hugo Menezes Barra  
**Empresa Parceira:** Schulz S.A.  
**Tecnologias:** Python, SQLite


## 1. Contextualização e os objetivos

Na primeira e na segunda entrega, a equipe analisou os processos de calibração do laboratório de metrologia da Schulz S.A e estruturou um banco de dados em SQLite para organizar informações mantidas em arquivos separados 

Já **AV 03 — MVP Parte 1** foi desenvolvido uma parte funcional do sistema: utilizando classes em Programação Orientada a Objetos (POO), conexão e persistencia no SQLite, operações CRUD, validação básica de conformidade metrológica e demonstração do fluxo com um relatório no terminal 

## 2. Estrutura do projeto

| Arquivo | Finalidade |
|---|---|
| `04_classes.py` | Reúne as quatro classes do sistema: `Tecnico` (profissionais envolvidos nas calibrações), `Equipamento` (dispositivos e instrumentos cadastrados), `Medicao` (leituras, cálculos de média/desvio e verificação de conformidade) e `BancoDados` (conexão SQLite, consultas SQL, CRUD e `JOIN`). |
| `05_main.py` | Demonstra instanciação de objetos, registros no SQLite, consulta `JOIN` e relatório no terminal. |
| `banco/03_banco.sql` | Estrutura das tabelas, chaves e restrições do banco de dados. |
| `banco/criar_banco.py` | Inicialização do banco a partir do script SQL. |
| `banco/schulz_calibracao.db` | Banco principal, com os dados iniciais das planilhas. |
| `banco/schulz_calibracao_testes.db` | Banco usado nos testes e no `05_main.py`. |
| `testes/teste_*.py` | Verificação independente de métodos e operações. |
| `06_mvp_parte1.md` | Este documento (documentação técnica do MVP - Parte 1). |
| `docs/` | Documentação da AV02 (`02_base.md`), roteiro da AV03 e scripts que geram os arquivos `.md`. |

Como o nome `04_classes.py` começa com número, o Python não permite `from 04_classes import Tecnico`. Por isso o `05_main.py` e os testes carregam o arquivo com `importlib.import_module("04_classes")` e acessam as classes como `classes.Tecnico`, `classes.Medicao` etc. Os testes devem ser executados a partir da raiz do projeto, por exemplo: `python -m testes.teste_classe_medicao`.

## 3. Programação Orientada a Objetos

### 3.1 Classe `Tecnico`

Representa o profissional associado a uma calibração. Possui os atributos `nome`, `matricula`, `setor`, `cargo_perfil` e `id_tecnico`. O construtor `__init__()` inicializa os dados e o método `exibir_dados()` mostra as informações no terminal. O `id_tecnico` pode iniciar com `None` até o cadastro no banco gerar um identificador.

### 3.2 Classe `Equipamento`

Representa um dispositivo ou instrumento cadastrado. Contém `codigo_tag`, `denominacao`, `fabricante`, `modelo`, `numero_serie`, `setor_localizacao` e `id_equipamento`. O método `exibir_dados()` apresenta os atributos. O identificador também pode ser preenchido após o `INSERT`.

### 3.3 Classe `Medicao`

Representa as leituras de uma característica avaliada. Armazena `nominal`, `medida_1`, `medida_2`, `tolerancia_inferior`, `tolerancia_superior`, dados do procedimento (`ordem_servico`, `data_medicao`, `temperatura_ambiente`, `parametro_avaliado`), identificadores das entidades relacionadas e `incerteza_expandida_u`.

Seus métodos de processamento são:

| Método | Regra aplicada |
|---|---|
| `calcular_media()` | Retorna `(medida_1 + medida_2) / 2`. |
| `calcular_desvio()` | Retorna `calcular_media() - nominal`. |
| `calcular_desvio_padrao()` | Utiliza `statistics.stdev()` para obter o desvio-padrão **amostral** das duas leituras. |
| `validar_conformidade()` | Verifica se `nominal + tolerancia_inferior <= media <= nominal + tolerancia_superior`. |

O método `validar_conformidade()` retorna `CONFORME` ou `NAO_CONFORME`, que são os valores aceitos pela restrição `CHECK` do banco existente. O roteiro usa os termos `APROVADO/REPROVADO`; no MVP, esses resultados são representados pelos status de conformidade, **sem pretender substituir uma decisão metrológica completa**. A incerteza expandida é informada ao objeto, mas seu cálculo técnico ainda não foi implementado.

**Encapsulamento:** `nominal`, `tolerancia_inferior` e `tolerancia_superior` são guardados em atributos internos (`_nominal`, `_tolerancia_inferior`, `_tolerancia_superior`; o `_` é a convenção do Python para atributo de uso interno) e expostos por métodos `@property` somente de leitura. Assim, os limites usados em `validar_conformidade()` não podem ser alterados por engano depois que o objeto é criado. O construtor também valida a regra de negócio `tolerancia_inferior <= tolerancia_superior` e lança `ValueError` quando ela não é respeitada.

### 3.4 Classe `BancoDados` e separação de responsabilidades

A classe `BancoDados` concentra a conexão, os comandos SQL e o encerramento do acesso ao SQLite. As classes de domínio mantêm os atributos e as regras próprias de cada entidade, enquanto o programa `05_main.py` coordena a execução. Esse desenho demonstra **abstração, instanciação de objetos, métodos e separação de responsabilidades**.
O **encapsulamento** foi aplicado na classe `Medicao`, que concentra a regra de negócio (seção 3.3). Em `Tecnico` e `Equipamento` os atributos continuam públicos, pois são apenas dados cadastrais sem regra de cálculo. Não se utiliza herança entre as classes.

## 4. Diagrama textual das classes e relacionamentos

```text
+-------------------------+           +---------------------------+
| Tecnico                 |           | Equipamento               |
|-------------------------|           |---------------------------|
| id_tecnico              |           | id_equipamento            |
| nome, matricula         |           | codigo_tag, denominacao  |
| setor, cargo_perfil     |           | fabricante, modelo       |
|-------------------------|           | numero_serie, setor       |
| + exibir_dados()        |           |---------------------------|
+-------------+-----------+           | + exibir_dados()          |
              |                       +-------------+-------------+
              | 1                                   | 1
              |                                     |
              | 0..N                                | 0..N
              v                                     v
          +------------------------------------------------+
          | Medicao                                        |
          |------------------------------------------------|
          | id_medicao, id_tecnico, id_equipamento          |
          | nominal, medida_1, medida_2, tolerancias       |
          | ordem_servico, data_medicao, parametro_avaliado |
          | temperatura_ambiente, incerteza_expandida_u   |
          |------------------------------------------------|
          | + calcular_media()                             |
          | + calcular_desvio()                            |
          | + calcular_desvio_padrao()                     |
          | + validar_conformidade()                       |
          +----------------------+-------------------------+
                                 |
                                 | persistencia / consultas
                                 v
          +------------------------------------------------+
          | BancoDados                                     |
          |------------------------------------------------|
          | conexao                                        |
          |------------------------------------------------|
          | + listar_*()                                   |
          | + cadastrar_*()                                |
          | + atualizar_*()                                |
          | + excluir_*()                                  |
          | + listar_medicoes_detalhadas()                  |
          | + fechar_conexao()                             |
          +------------------------------------------------+
```
No diagrama acima as cardinalidades apresentam o modelo relacional: tecnico ou um equipamento podem aparecer várias medições, enquanto cada medição é responsável por referenciar um técnico e um equipamento `id_tecnico` e `id_equipamento`. Na implementação em Python, esses vinculos são armazenados como IDs. O acesso relacional ocorre no SQLite, e não por atributos contendo objetos `Tecnico` e `Equipamento`.

## 5. Conexão SQL e integridade relacional

O arquivo `banco/03_banco.sql` define três tabelas: `tecnicos`, `equipamentos` e `medicoes`. As colunas incluem chaves primárias autoincrementais, campos obrigatórios `NOT NULL`, unicidade `UNIQUE` para matrícula e TAG, valores permitidos via `CHECK` e chaves estrangeiras entre as tabelas.

A classe `BancoDados` usa `sqlite3.connect()`, localiza o banco com `pathlib.Path`, habilita `PRAGMA foreign_keys = ON` e configura `sqlite3.Row` para acesso às colunas pelo nome. O construtor verifica se o arquivo informado existe e lança `FileNotFoundError` quando não é encontrado.

As operações de escrita usam parâmetros SQL (`?`), evitando a montagem direta de comandos com valores recebidos do objeto. Os cadastros chamam `commit()` e recuperam os IDs gerados por `cursor.lastrowid`; atualizações e exclusões retornam `cursor.rowcount`.

O `banco/03_banco.sql` possui `DROP TABLE IF EXISTS`, portanto executá-lo novamente pode eliminar tabelas e registros. Os testes funcionais foram executados em `banco/schulz_calibracao_testes.db`, preservando o banco original.

## 6. Operações CRUD implementadas

| Operação | `Tecnico` | `Equipamento` | `Medicao` |
|---|---|---|---|
| `INSERT` | `cadastrar_tecnico()` | `cadastrar_equipamento()` | `cadastrar_medicao()` |
| `SELECT` | `listar_tecnicos()` | `listar_equipamentos()` | `listar_medicoes()` |
| `UPDATE` | `atualizar_tecnico()` | `atualizar_equipamento()` | `atualizar_medicao()` |
| `DELETE` | `excluir_tecnico()` | `excluir_equipamento()` | `excluir_medicao()` |

Ao fazer uma atualização ou inserção de uma medição, `BancoDados` utiliza os métodos de `Medicao` para calcular e gravar `media_obtida`, `desvio_calculado` e `status_conformidade`. A exclusão de técnicos e equipamentos é bloqueada pela aplicação quando existem medições vinculadas; as chaves estrangeiras configuradas no banco reforçam essa regra.

## 7. Consulta relacional com `JOIN`

O método `listar_medicoes_detalhadas()` executa `INNER JOIN` entre `medicoes`, `tecnicos` e `equipamentos`, associando as chaves estrangeiras. Ele recupera, numa única consulta, dados como nome do técnico, denominação do equipamento, código TAG, ordem de serviço, parâmetro avaliado, média, desvio e status.

```sql
SELECT m.id_medicao, t.nome AS nome_tecnico,
       e.codigo_tag, e.denominacao,
       m.parametro_avaliado, m.media_obtida,
       m.desvio_calculado, m.status_conformidade
FROM medicoes AS m
INNER JOIN tecnicos AS t ON m.id_tecnico = t.id_tecnico
INNER JOIN equipamentos AS e ON m.id_equipamento = e.id_equipamento;
```

Está consulta irá fornecer os dados relacionados ao relatório de calibração exibido no terminal pelo `05_main.py`.

## 8. Tratamento de erros SQL e validações

**Validações existentes:**

- O construtor `BancoDados` verifica a existência do arquivo SQLite e lança `FileNotFoundError` se necessário.
- Os métodos `atualizar_*()` e `excluir_*()` verificam se o identificador recebido está ausente (`None`) nos casos previstos.
- `cadastrar_medicao()` e `atualizar_medicao()` verificam alguns campos obrigatórios antes de escrever no banco.
- `excluir_tecnico()` e `excluir_equipamento()` impedem exclusões quando há medições associadas.
- `UNIQUE`, `NOT NULL`, `CHECK` e as chaves estrangeiras do SQLite impõem regras adicionais de integridade.
- O construtor de `Medicao` lança `ValueError` se a tolerância inferior for maior que a superior.
- Os scripts de testes e o `05_main.py` utilizam `finally` para fechar a conexão.

**Tratamento de erros SQL:**

Quando o SQLite recusa um registro por violar `UNIQUE`, `NOT NULL`, `CHECK` ou uma chave estrangeira, ele lança `sqlite3.IntegrityError`. Os métodos `cadastrar_*()` e `atualizar_*()` da classe `BancoDados` capturam esse erro, desfazem a operação com `rollback()` e lançam um `ValueError` com uma mensagem clara. O `05_main.py` e os testes capturam o `ValueError` com `except` e exibem a mensagem no terminal, sem interromper o programa com o erro bruto do banco.

```python
try:
    cursor = self.conexao.execute("INSERT INTO tecnicos ...", (...))
    self.conexao.commit()
except sqlite3.IntegrityError as erro:
    self.conexao.rollback()
    raise ValueError(f"Não foi possível cadastrar o técnico: {erro}")
```

## 9. Validação do fluxo funcional do MVP

### 9.1 Fluxo demonstrado pelo `05_main.py`

1. Importa o arquivo `04_classes.py` (via `importlib`) e obtém as classes `Tecnico`, `Equipamento`, `Medicao` e `BancoDados`.
2. Abre uma conexão com o arquivo `banco/schulz_calibracao_testes.db`.
3. Instancia um técnico fictício e um equipamento de demonstração.
4. Consulta matrícula e TAG para evitar repetir esses cadastros de demonstração.
5. Instancia uma medição com duas leituras, tolerâncias e as chaves estrangeiras corretas.
6. Cadastra a medição quando o registro correspondente ainda não está presente.
7. Consulta os registros com `listar_medicoes_detalhadas()` (`INNER JOIN`).
8. Apresenta no terminal nome do técnico, equipamento, TAG, ordem de serviço, parâmetro avaliado, média, desvio e status.
9. Fecha a conexão dentro do bloco `finally`.

### 9.2 Resultados dos testes realizados

| Teste | Evidência observada |
|---|---|
| `testes/teste_classe_medicao.py` | Cenário conforme: média `6.0790`, desvio `0.0040`; cenário não conforme: média `6.0910`, desvio `0.0160`. |
| Cadastros `INSERT` | Técnicos, equipamentos e medições de teste gravados e IDs gerados pelo SQLite. |
| Atualizações `UPDATE` | Técnicos, equipamentos e medições atualizados; testes retornaram `1` registro afetado. |
| Consulta `JOIN` | Registros exibidos com nome do técnico e identificação do equipamento. |
| Cadastro repetido | Ao repetir `teste_cadastrar_tecnico.py`, o programa exibe `ERRO: Não foi possível cadastrar o técnico: UNIQUE constraint failed: tecnicos.matricula` e encerra a conexão normalmente. |
| Exclusões `DELETE` | Registros temporários excluídos, com verificação posterior de ausência. |
| `05_main.py` | Relatório para `MVP-EQ-001` com média `6.0790`, desvio `0.0040` e status `CONFORME`. |

Exemplo de saída do programa principal no cenário de demonstração:

```text
=== RELATÓRIO DE CALIBRAÇÃO ===
Técnico: Técnico MVP
Equipamento: Equipamento de Demonstração
TAG: MVP-EQ-001
Ordem de serviço: OS-MVP-001
Parâmetro: DIAMETRO_MVP
Média: 6.0790
Desvio: 0.0040
Status: CONFORME
```
