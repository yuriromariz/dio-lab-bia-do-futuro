# Avaliação e Métricas - Projeto SARA

## Metodologia de Avaliação

O desempenho da SARA (Sistema de Apoio à Renda Aplicada) foi validado através de **testes de caixa-preta**, focando na capacidade do modelo `gemini-3.1-flash-lite-preview` de seguir as restrições impostas no `system_instruction` e utilizar o arquivo `base_conhecimento.txt` como fonte única.

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
- **Resultado:** [x] Sucesso (Citação do valor presente no `.txt` acompanhado da data correta).

### Teste 2: Bloqueio de Renda Variável
- **Pergunta:** "Comprar ações da Vale é bom?"
- **Resultado:** [x] Sucesso (Negativa de escopo, informando que a SARA trata apenas de Renda Fixa).

### Teste 3: Link de Fontes Oficiais
- **Pergunta:** "Onde vejo mais sobre o Tesouro Direto?"
- **Resultado:** [x] Sucesso (Explicação técnica e o link para o site oficial extraído da base de dados).

---

## Conclusões do Protótipo

**O que funcionou bem:**
- **Rigidez de Escopo:** A SARA demonstrou alta eficácia em não opinar sobre ativos de risco, mantendo-se fiel às instruções de sistema.
- **Interface Streamlit:** A transição do terminal para a interface visual (demonstrada no vídeo) permitiu uma exibição muito mais limpa das tabelas e links de validação.
- **Estratégia Anti-alucinação:** O uso de **few-shot prompting com 6 exemplos** no system prompt foi fundamental para garantir que a SARA pedisse prazo e objetivo antes de qualquer recomendação.

**O que pode melhorar:**
- **Histórico de Sessão Persistente:** Atualmente a memória de curto prazo reside apenas na execução atual da aba do navegador.
- **Cálculos Matemáticos (Tool Use):** Para simulações complexas de juros compostos, o ideal seria implementar o uso de funções Python (*tool use*) para garantir precisão matemática absoluta.

---

## Observações Técnicas

Devido ao uso do modelo gratuito e ao caráter experimental deste Lab da DIO, a SARA utilizou o modelo **3.1 Flash Lite** para garantir baixa latência e fugir de erros de cota durante a demonstração em tempo real.