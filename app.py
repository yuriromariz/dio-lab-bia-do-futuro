import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="SARA - Sistema de Apoio à Renda Aplicada",
    page_icon="💼",
    layout="centered",
)

st.markdown(
    """
<style>
    .stApp { background-color: #0d1117 !important; }
    h1 {
        font-size: 2.2rem !important; font-weight: 700 !important;
        color: #f0f6fc !important; text-align: center !important;
        margin-bottom: 0.2rem !important; letter-spacing: -0.02em;
    }
    .subtitle {
        font-size: 1.1rem !important; color: #8b949e !important;
        text-align: center !important; margin-bottom: 1rem !important;
    }
    .date-badge {
        display: inline-block; background: linear-gradient(135deg, #1f6feb 0%, #8a2be2 100%);
        color: white; padding: 0.4rem 1.2rem; border-radius: 20px;
        font-size: 0.85rem; font-weight: 500; text-align: center;
        margin: 0 auto; display: block; width: fit-content;
        margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(31, 111, 235, 0.3);
    }
    /* User message - right side, gradient */
    div[data-testid="stChatMessageUser"] {
        background: linear-gradient(135deg, #1f6feb 0%, #8a2be2 100%) !important;
        color: white !important; border-radius: 20px 20px 4px 20px !important;
        margin-left: auto !important; margin-right: 0 !important;
        border: none !important; font-weight: 400 !important;
        max-width: 75% !important; padding: 1rem 1.2rem !important;
        box-shadow: 0 2px 8px rgba(31, 111, 235, 0.2) !important;
        text-align: left !important;
    }
    /* Assistant message - left side, dark */
    div[data-testid="stChatMessageAssistant"] {
        background-color: #161b22 !important; color: #f0f6fc !important;
        border-radius: 20px 20px 20px 4px !important;
        border-left: 4px solid #1f6feb !important;
        margin-left: 0 !important; margin-right: auto !important;
        max-width: 75% !important; padding: 1rem 1.2rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        text-align: left !important;
    }
    /* HIDE AVATARS COMPLETELY */
    [data-testid="stChatMessageAvatar"] { display: none !important; }
    [data-testid="stChatMessage"] > div:first-child { display: none !important; }
    .stChatInputContainer {
        background-color: #161b22 !important; border-radius: 16px !important;
        border: 2px solid #21262d !important; padding: 0.6rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important; margin-top: 1.5rem !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #1f6feb !important; box-shadow: 0 4px 20px rgba(31, 111, 235, 0.3) !important;
    }
    .stChatInput input::placeholder { color: #8b949e !important; }
    .stChatInput textarea { color: #f0f6fc !important; font-size: 1rem !important; }
    .stSpinner { border-color: #1f6feb !important; }
    footer { visibility: hidden; }
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #21262d; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #30363d; }
</style>
""",
    unsafe_allow_html=True,
)


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
        Você é a SARA, uma consultora especialista em Renda Fixa.
        Seu objetivo é ajudar brasileiros a investirem melhor com base em dados oficiais.

        REGRAS OBRIGATÓRIAS:
        1. NUNCA invente informações. Responda APENAS com os dados fornecidos abaixo.
        2. NUNCA use markdown para estruturar respostas (exceto links literais da base).
        3. NUNCA faça recomendações personalizadas sem prazo e objetivo do usuário.
        4. NUNCA devolva perguntas genéricas como "qual é mais importante pra você".
        5. Se o usuário pedir recomendação sem dados suficientes, peça as informações faltantes de forma direta.
        6. Se o usuário perguntar algo fora do escopo (ações, cripto, FIIs, day trade), responda: "Não posso opinar sobre [assunto]. Meu escopo é exclusivamente Renda Fixa: CDB, LCI, LCA, Tesouro Direto e Poupança."

        BASE DE CONHECIMENTO:
        ---
        {base_texto}
        ---
        """
        model = genai.GenerativeModel(
            model_name="models/gemini-flash-lite-latest",
            system_instruction=instrucao_sistema,
        )
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.mensagens = []
        st.session_state.mensagens.append(
            {
                "role": "assistant",
                "content": "Olá! Sou a SARA, sua consultora especialista em Renda Fixa. Como posso ajudar você hoje?",
            }
        )


def exibir_cabecalho():
    st.markdown("<h1>SARA</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subtitle'>Sistema de Apoio à Renda Aplicada</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='subtitle' style='margin-top: -0.8rem; margin-bottom: 1.5rem;'>"
        "Sua consultora especialista em Renda Fixa</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='date-badge'>📊 Dados referentes a 18/04/2026</div>",
        unsafe_allow_html=True,
    )


def exibir_mensagens():
    """Renderiza mensagens usando st.chat_message (componente nativo rápido)"""
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"], avatar=None):
            st.write(msg["content"])


def processar_mensagem(pergunta):
    """Envia pergunta para o Gemini e adiciona resposta ao histórico"""
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    try:
        response = st.session_state.chat.send_message(pergunta)
        st.session_state.mensagens.append(
            {"role": "assistant", "content": response.text}
        )
    except Exception as e:
        st.session_state.mensagens.append(
            {"role": "assistant", "content": f"Erro: {str(e)}"}
        )


def main():
    if not GOOGLE_API_KEY:
        st.markdown(
            """
        <div style='text-align: center; padding: 3rem; background: #161b22; border-radius: 16px; border: 2px solid #21262d;'>
            <h2 style='color: #f85149; margin-bottom: 1rem;'>🔑 API Key não encontrada</h2>
            <p style='font-size: 1.1rem; color: #8b949e; margin-bottom: 1.5rem;'>
                Configure <code style="background: #0d1117; padding: 0.2rem 0.5rem; border-radius: 4px;">GEMINI_API_KEY</code>
                no arquivo <code style="background: #0d1117; padding: 0.2rem 0.5rem; border-radius: 4px;">.env</code>.
            </p>
            <div style='background: #0d1117; padding: 1rem; border-radius: 8px; text-align: left; max-width: 500px; margin: 0 auto; font-family: monospace; color: #f0f6fc;'>
                GEMINI_API_KEY=sua_chave_aqui
            </div>
            <p style='margin-top: 1.5rem; color: #8b949e; font-size: 0.9rem;'>
                Obtenha sua chave em: <a href='https://makersuite.google.com/app/apikey' target='_blank' style='color: #1f6feb;'>Google AI Studio</a>
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.stop()

    inicializar_chat()
    exibir_cabecalho()
    exibir_mensagens()

    pergunta = st.chat_input("Digite sua mensagem para a SARA...")

    if pergunta:
        # Mostra mensagem do usuário
        with st.chat_message("user", avatar=None):
            st.write(pergunta)
        # Processa resposta da SARA
        with st.chat_message("assistant", avatar=None):
            with st.spinner("SARA está digitando..."):
                processar_mensagem(pergunta)
        # Atualiza tela para mostrar a resposta
        st.rerun()


if __name__ == "__main__":
    main()
