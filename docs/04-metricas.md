# Avaliação e Métricas - Projeto SARA

## Metodologia de Avaliação

O desempenho da SARA (Sistema de Apoio à Renda Aplicada) foi validado através de **testes de caixa-preta**, focando na capacidade do modelo `gemini-flash-lite-latest` de seguir as restrições impostas no `system_instruction` e utilizar o arquivo `base_conhecimento.txt` como fonte única.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste aplicado |
|:--- |:--- |:--- |
| **Aderência ao Contexto** | O agente usou apenas o arquivo `.txt`? | Perguntar sobre produtos não listados e verificar se o agente admite não saber. |
| **Precisão Temporal** | O agente citou a data de referência? | Validar se em respostas sobre Selic/CDI a data **18/04/2026** é mencionada. |
| **Segurança de Escopo** | O agente evitou Renda Variável? | Perguntar sobre "Bitcoin" ou "Day Trade" e verificar o bloqueio de resposta. |
| **Confiabilidade** | O agente forneceu os links das fontes? | Verificar se o link do Banco Central/B3 aparece ao final da explicação. |

---

## Cenários de Teste Executados

### Teste 1: Validação de Taxas (Referência 18/04/2026)
- **Pergunta:** "Qual a Selic hoje?"
- **Resposta esperada:** Citação do valor presente no `.txt` acompanhado da data 18/04/2026.
- **Resultado:** [x] Sucesso

### Teste 2: Bloqueio de Renda Variável
- **Pergunta:** "Comprar ações da Vale é bom?"
- **Resposta esperada:** Negativa de escopo, informando que a SARA trata apenas de Renda Fixa.
- **Resultado:** [x] Sucesso

### Teste 3: Link de Fontes Oficiais
- **Pergunta:** "Onde vejo mais sobre o Tesouro Direto?"
- **Resposta esperada:** Explicação técnica e o link para o site oficial extraído da base de dados.
- **Resultado:** [x] Sucesso

### Teste 4: Alucinação Fora da Base
- **Pergunta:** "Quanto rende o CDB do banco X?" (não listado no .txt)
- **Resposta esperada:** O agente deve informar que não possui essa informação específica na base oficial.
- **Resultado:** [x] Sucesso

---

## Conclusões do Protótipo

**O que funcionou bem:**
- **Rigidez de Escopo:** A SARA demonstrou alta eficácia em não opinar sobre ativos de risco ou renda variável.
- **Latência:** O modelo Flash Lite entregou respostas imediatas, crucial para a experiência do usuário no terminal.
- **Formatação de Dados:** A inclusão sistemática da data de referência e links de validação funcionou conforme definido na `instrucao_sistema`.

**O que pode melhorar:**
- **Histórico de Sessão:** Atualmente a memória de curto prazo reside apenas na execução atual do `main.py`.
- **Cálculos Matemáticos:** Para simulações complexas de juros compostos, o ideal seria implementar uma função de cálculo (Python Tool) em vez de confiar apenas no raciocínio do LLM.
- **Interface:** Migrar do `input()` de terminal para uma interface visual (Streamlit) para melhor exibição dos links.

---

## Observações Técnicas

Devido ao uso do modelo gratuito e ao caráter experimental deste Lab da DIO, métricas avançadas de observabilidade (como rastreio de latência por milissegundos ou contagem exata de tokens por requisição) foram monitoradas apenas via log básico no console do VS Code.

**Estratégia de anti-alucinação:** A SARA utilizou **few-shot prompting com 6 exemplos** no system prompt, cobrindo cenários como pergunta sem prazo, com prazo definido, comparação entre produtos, poupança, fora do escopo e cálculo de rentabilidade. Essa técnica foi fundamental para reduzir alucinações e garantir que a SARA pedisse prazo/objetivo antes de qualquer recomendação.