import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai


# Carrega variáveis de ambiente
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)


# Configuração da página Streamlit
st.set_page_config(
    page_title="SARA - Sistema de Apoio à Renda Aplicada",
    page_icon="💼",
    layout="centered",
)

# ---------- CSS ----------
st.markdown(
    """
<style>
    /* Fundo geral */
    .stApp {
        background-color: #0d1117 !important;
    }

    /* Título principal */
    h1 {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #f0f6fc !important;
        text-align: center !important;
        margin-bottom: 0.2rem !important;
        letter-spacing: -0.02em;
    }

    /* Subtítulo */
    .subtitle {
        font-size: 1.1rem !important;
        color: #8b949e !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
    }

    /* Badge de data */
    .date-badge {
        display: block;
        background-color: #21262d !important;
        border: 1px solid #30363d !important;
        color: #8b949e !important;
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        text-align: center;
        margin: 0 auto 2rem auto;
        width: fit-content;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }

    /* Balão do usuário */
    .user-bubble {
        background: linear-gradient(135deg, #0969da 0%, #1f6feb 100%) !important;
        color: white;
        border-radius: 20px 20px 4px 20px;
        padding: 1rem 1.2rem;
        margin: 0 0 1rem auto;
        max-width: 75%;
        box-shadow: 0 2px 8px rgba(31, 111, 235, 0.2);
        text-align: left;
        word-wrap: break-word;
    }

    /* Balão do assistente */
    .assistant-bubble {
        background-color: #161b22;
        color: #f0f6fc;
        border-radius: 20px 20px 20px 4px;
        border-left: 4px solid #1f6feb;
        padding: 1rem 1.2rem;
        margin: 0 auto 1rem 0;
        max-width: 85%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        text-align: left;
        word-wrap: break-word;
        line-height: 1.6 !important; 
        font-size: 0.95rem !important;
    }

    .assistant-bubble a {
        color: #58a6ff !important;
        text-decoration: none !important;
        font-weight: 500;
    }
    
    .assistant-bubble a:hover {
        text-decoration: underline !important;
    }

    /* Campo de input */
    .stChatInputContainer {
        background-color: #161b22 !important;
        border-radius: 16px !important;
        border: 1px solid #30363d !important;
        padding: 0.4rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
    }

    .stChatInputContainer:focus-within, 
    .stChatInputContainer:hover {
        border-color: #1f6feb !important;
        box-shadow: 0 0 10px rgba(31, 111, 235, 0.3) !important;
    }

    .stChatInput textarea {
        color: #f0f6fc !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Esconder rodapé e Spinner */
    footer {visibility: hidden;}
    .stSpinner i { color: #1f6feb !important; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #21262d; border-radius: 4px; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- FUNÇÕES AUXILIARES ----------

@st.cache_data
def carregar_contexto():
    caminho = "data/base_conhecimento.txt"
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Erro: Base de conhecimento não encontrada."

def inicializar_chat():
    if "chat" not in st.session_state:
        base_texto = carregar_contexto()
        instrucao_sistema = f"""
Você é a SARA, especialista em Renda Fixa.

REGRAS OBRIGATÓRIAS:
1. NUNCA invente informações. Responda APENAS com os dados fornecidos abaixo.
2. NUNCA use markdown para estruturar respostas (exceto links literais da base).
3. NUNCA faça recomendações personalizadas sem prazo e objetivo do usuário.
4. NUNCA devolva perguntas genéricas como "qual é mais importante pra você".
5. Se o usuário pedir recomendação sem dados suficientes, peça as informações faltantes de forma direta.
6. Se o usuário perguntar algo fora do escopo (ações, cripto, FIIs, day trade), responda: "Não posso opinar sobre [assunto]. Meu escopo é exclusivamente Renda Fixa: CDB, LCI, LCA, Tesouro Direto e Poupança."

BASE:
{base_texto}

EXEMPLOS:
[Exemplo 1 - Sem prazo]
Usuário: "onde invisto 5 mil reais?"
SARA: "Para orientar você, preciso saber: (1) por quanto tempo pode deixar o dinheiro aplicado? (2) esse dinheiro é para reserva de emergência ou para longo prazo?"

[Exemplo 2 - Com prazo definido]
Usuário: "posso deixar 10 mil parados por 2 anos"
SARA: "Com prazo de 2 anos e Selic em 14,75% a.a. (referência 18/04/2026), as melhores opções são: CDB pós-fixado (100% do CDI, com IR de 15% após 720 dias) ou LCI/LCA (90% do CDI, isento de IR). O Tesouro Selic 2031 também é uma opção segura com liquidez D+1."

[Exemplo 3 - Fora de escopo]
Usuário: "devo comprar Bitcoin?"
SARA: "Não posso opinar sobre criptoativos. Meu escopo é exclusivamente Renda Fixa: CDB, LCI, LCA, Tesouro Direto e Poupança."

[Exemplo 4 - Rentabilidade]
Usuário: "quanto rende 1.000 reais no CDB por 6 meses?"
SARA: "Com CDI a 14,65% a.a. e IR de 22,5%, R$ 1.000 renderia aproximadamente R$ 1.054,80 líquido após 6 meses. Esse é um valor estimado baseado na taxa atual."

[Exemplo 5 - Comparação entre produtos]
Usuário: "LCI ou CDB? Qual compensa mais?"
SARA: "LCI é isento de IR, mas tem carência mínima de 90 dias e rentabilidade típica de 90% do CDI. CDB paga IR pela tabela regressiva (22,5% a 15%), mas tem liquidez diária e rentabilidade típica de 100% do CDI. Para prazos acima de 2 anos, o LCI costuma compensar mais pela isenção. Para prazos curtos ou necessidade de liquidez, o CDB é melhor."

[Exemplo 6 - Pergunta sobre poupança]
Usuário: "vale a pena deixar na poupança?"
SARA: "Com a Selic em 14,75% a.a., a poupança rende 0,5% ao mês + TR (cerca de 9% ao ano). Um CDB de 100% do CDI rende 14,65% ao ano bruto. Mesmo com IR de 22,5% (menos de 180 dias), o CDB rende mais que a poupança. A poupança só é vantajosa para prazos muito curtos (menos de 30 dias) ou para quem não quer pensar em investimentos."
"""
        model = genai.GenerativeModel(
            model_name="models/gemini-3.1-flash-lite-preview",
            system_instruction=instrucao_sistema,
        )
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.mensagens = [{"role": "assistant", "content": "Olá! Sou a SARA. Como posso ajudar?"}]

def exibir_mensagens():
    for msg in st.session_state.mensagens:
        classe = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
        st.markdown(f"<div class='{classe}'>{msg['content']}</div>", unsafe_allow_html=True)

# ---------- LÓGICA PRINCIPAL ----------

def main():
    if not GOOGLE_API_KEY:
        st.error("API Key não encontrada no arquivo .env")
        st.stop()

    inicializar_chat()
    
    # Exibe cabeçalho
    st.markdown("<h1>SARA</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Sistema de Apoio à Renda Aplicada</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle' style='margin-top: -0.8rem;'>Sua consultora especialista em Renda Fixa</p>", unsafe_allow_html=True)
    st.markdown("<div class='date-badge'>📊 Dados referentes a 18/04/2026</div>", unsafe_allow_html=True)

    # Exibe histórico
    exibir_mensagens()

    # Input do usuário
    pergunta = st.chat_input("Digite sua mensagem para a SARA...")

    if pergunta:
        # Mostra a pergunta imediatamente
        st.markdown(f"<div class='user-bubble'>{pergunta}</div>", unsafe_allow_html=True)
        
        with st.spinner("SARA está consultando a base de dados..."):
            try:
                response = st.session_state.chat.send_message(pergunta)
                resposta_texto = response.text
                
                st.session_state.mensagens.append({"role": "user", "content": pergunta})
                st.session_state.mensagens.append({"role": "assistant", "content": resposta_texto})
                
                st.markdown(f"<div class='assistant-bubble'>{resposta_texto}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro: {e}")
        
        #st.rerun()

if __name__ == "__main__":
    main()