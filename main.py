import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# 2. CARREGA A BASE DE DADOS
def carregar_contexto():
    caminho = "data/base_conhecimento.txt"
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Erro: Base de conhecimento não encontrada na pasta data/."

# 3. CONFIGURAÇÃO DA SARA
base_texto = carregar_contexto()

instrucao_sistema = f"""
Você é a SARA, uma consultora especialista em Renda Fixa.
Seu objetivo é ajudar brasileiros a investirem melhor com base em dados oficiais.
Use EXCLUSIVAMENTE as informações abaixo para responder:
---
{base_texto}
---
Regras:
- Seja direta e técnica, mas com linguagem acessível.
- Se o dado for Selic ou CDI, cite que a referência é 18/04/2026.
- Forneça os links das fontes na base se o usuário quiser validar.
"""

model = genai.GenerativeModel(
    model_name="models/gemini-flash-lite-latest",
    system_instruction=instrucao_sistema
)
# 4. LOOP DE EXECUÇÃO (CHAT)
chat = model.start_chat(history=[])

print("--- SARA ONLINE (Digite 'sair' para encerrar) ---")

while True:
    pergunta = input("Você: ")
    if pergunta.lower() in ["sair", "exit"]:
        break
    
    try:
        response = chat.send_message(pergunta)
        print(f"\nSARA: {response.text}\n")
    except Exception as e:
        print(f"Erro na resposta: {e}")