import streamlit as st
import google.generativeai as genai
import time

# 1. Configuração da página e Estilo Visual (CSS Customizado)
st.set_page_config(page_title="Bakugo Chat Pro", page_icon="💥", layout="centered")

# CSS para dar uma cara de "Poly.AI" com tema escuro e detalhes alaranjados/explosivos
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    /* Estilizando o chat do usuário */
    [data-testid="stChatMessageUser"] {
        background-color: #2D2D2D !important;
        border-left: 5px solid #FF4B4B !important;
    }
    /* Estilizando o chat do Bakugo */
    [data-testid="stChatMessageAssistant"] {
        background-color: #1E1E1E !important;
        border-left: 5px solid #FF8C00 !important;
    }
    h1 {
        color: #FF4500;
        text-shadow: 0 0 10px rgba(255, 69, 0, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

st.title("💥 Bakugo Katsuki - Chat IA Pro")
st.write("Agora com IA real. Tente conversar sobre qualquer assunto, mas ele ainda é muito estressado!")

# 2. Configuração da Inteligência Artificial (Configuração de Prompt de Sistema)
# IMPORTANTE: Para rodar, você precisa configurar sua API Key nas configurações do Streamlit (Secrets)
# Ou colocar diretamente temporariamente: genai.configure(api_key="SUA_CHAVE_AQUI")
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    # Caso esteja testando localmente e queira colocar a chave direto (não envie essa chave ao GitHub!)
    genai.configure(api_key="Substitua_Pela_Sua_Chave_Da_API_Aqui")

# O segredo do Poly.AI: O "System Prompt" que define como a IA DEVE agir
PROMPT_DE_PERSONALIDADE = """
Você é Katsuki Bakugo do anime My Hero Academia. Você está conversando em um chat.
Diretrizes estritas de comportamento:
1. Seu tom é extremamente agressivo, arrogante, impaciente e barulhento. Você se irrita por qualquer coisa.
2. Você usa termos como "Seu extra!", "Maldito!", "Cala a boca!" e frequentemente grita em caixa alta (ex: "MORRA!", "SHINEEE!").
3. Seu objetivo absoluto é ser o Herói Número 1 e superar o Deku (Izuku Midoriya), a quem você detesta profundamente. Se falarem dele, fique furioso.
4. Se o usuário falar de "Sofia", aja como se fosse uma conhecida irritante ou uma extra que fica te atrapalhando nos treinos da U.A.
5. Nunca quebre o personagem. Responda em português de forma curta, direta e impactante, usando emojis de explosão (💥) de vez em quando.
"""

# 3. Inicializar o modelo de IA e a Memória
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "assistant", "content": "💥 O que você quer, seu extra?! Não me faça perder meu tempo!"}
    ]

# 4. Exibir o histórico de mensagens com o novo design
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Entrada do usuário e processamento da IA
if pergunta := st.chat_input("Envie uma mensagem para o Bakugo..."):
    
    # Exibe a pergunta do usuário
    with st.chat_message("user"):
        st.markdown(pergunta)
    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    # Chamando a Inteligência Artificial para responder dinamicamente
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=PROMPT_DE_PERSONALIDADE
        )
        
        # Formata o histórico para o formato que o Gemini entende
        historico_ia = []
        for msg in st.session_state.mensagens:
            # Converte as funções do Streamlit para o padrão da API (user ou model)
            role_ia = "user" if msg["role"] == "user" else "model"
            historico_ia.append({"role": role_ia, "parts": [msg["content"]]})
        
        # Gera a resposta dinâmica
        chat = model.start_chat(history=historico_ia[:-1]) # Envia o histórico sem a última pergunta
        response = chat.send_message(pergunta)
        resposta_final = response.text

    except Exception as e:
        # Resposta de segurança caso a API dê algum erro ou esteja sem chave
        resposta_final = "💥 O QUE VOCÊ FEZ?! Meu sistema de explosões travou! (Configure a API Key corretamente)."

    # Cria o efeito de digitação na tela
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        for char in resposta_final:
            full_response += char
            time.sleep(0.01)
            placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
        
    st.session_state.mensagens.append({"role": "assistant", "content": resposta_final})
    
