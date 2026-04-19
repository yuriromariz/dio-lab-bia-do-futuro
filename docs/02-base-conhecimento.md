# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `base_conhecimento.txt` | TXT | Fonte única de informações sobre taxas, produtos, tributação e escopo do agente. Carregado integralmente no system prompt. |
| `historico_atendimento.csv` | CSV | **Não utilizado.** O agente não possui memória de interações anteriores. |
| `perfil_investidor.json` | JSON | **Não utilizado.** A SARA não personaliza recomendações por perfil, apenas por prazo e objetivo informados no momento da conversa. |
| `produtos_financeiros.json` | JSON | **Não utilizado.** Os produtos estão descritos no `base_conhecimento.txt`. |
| `transacoes.csv` | CSV | **Não utilizado.** O agente não analisa padrões de gastos ou histórico financeiro do usuário. |

## Adaptações nos Dados

Os dados mockados fornecidos pela DIO não foram utilizados. Em vez disso, foi criado um arquivo `base_conhecimento.txt` contendo:

- Indicadores oficiais (Selic e CDI) com fontes do Banco Central
- Produtos de Renda Fixa (Tesouro Selic, CDB, LCI/LCA, Poupança) com rentabilidades, garantias, liquidez e carência
- Tabela regressiva de Imposto de Renda
- Isenções fiscais
- Escopo explícito do que a SARA NÃO cobre (ações, cripto, FIIs, day trade, etc.)

A base é estática e foi construída manualmente com base em dados oficiais (B3, BCB, Receita Federal).

## Estratégia de Integração

### Como os dados são carregados?

O arquivo `data/base_conhecimento.txt` é carregado no início da execução do `main.py` através da função `carregar_contexto()`:

```python
def carregar_contexto():
    caminho = "data/base_conhecimento.txt"
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()