import streamlit as st
import streamlit_authenticator as stauth
import google.generativeai as genai
import time

# IMPORTAÇÃO DO BANCO DE DADOS EXTERNO
from personagens import PERSONAGENS_DB

# Configurações iniciais do login simplificado
credentials = {
    "usernames": {
        "admin": {
            "email": "adm@email.com",
            "name": "Admin",
            "password": "123"  # O sistema processará o texto plano diretamente nesta versão
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "poly_cookie",
    "poly_secret_key",
    cookie_expiry_days=30
)

autenticado, username, name = authenticator.login(location='main', fields={'Form name': 'Acessar Hub de RPG'})
stauth.Hasher.hash_passwords(config['credentials'])
authenticator = stauth.Authenticate(config['credentials'], config['cookie']['name'], config['cookie']['key'], config['cookie']['expiry_days'])

autenticado, username, name = authenticator.login(location='main', fields={'Form name': 'Acessar Hub de RPG'})

if autenticado:
    with st.sidebar:
        authenticator.logout('Sair da Conta', 'sidebar')
        st.divider()

    # Inicialização da Memória
    if "personagem_atual" not in st.session_state:
        st.session_state.personagem_atual = list(PERSONAGENS_DB.keys())[0]
        
    if "historico_global" not in st.session_state:
        st.session_state.historico_global = {}
        for nome, dados in PERSONAGENS_DB.items():
            st.session_state.historico_global[nome] = [{"role": "assistant", "content": dados["frase_inicial"]}]

    # Seletor de personagens organizado na lateral
    with st.sidebar:
        st.markdown("<h3 style='text-align: center;'>🤖 SELECIONE O BOT</h3>", unsafe_allow_html=True)
        for nome, dados in PERSONAGENS_DB.items():
            if st.button(f"{dados['emoji']} {nome}", key=f"btn_{dados['slug']}", use_container_width=True):
                st.session_state.personagem_atual = nome
                st.rerun()
                
        st.divider()
        api_key_input = st.text_input("Insira sua Gemini API Key:", type="password")

    p_nome = st.session_state.personagem_atual
    p_dados = PERSONAGENS_DB[p_nome]

    # Interface Visual Dinâmica
    st.markdown(f"""
        <style>
        .stApp {{ background-color: #0E0E10; color: #F5F5F7; }}
        [data-testid="stChatMessageUser"] {{ background-color: #232329 !important; border-radius: 12px; }}
        [data-testid="stChatMessageAssistant"] {{ background-color: {p_dados['cor_fundo_chat']} !important; border-left: {p_dados['borda_css']} !important; border-radius: 12px; }}
        </style>
    """, unsafe_allow_html=True)

    st.title(f"{p_dados['emoji']} {p_nome}")
    st.write(p_dados['subtitulo'])

    historico_atual = st.session_state.historico_global[p_nome]

    for msg in historico_atual:
        avatar_definido = p_dados["avatar"] if msg["role"] == "assistant" else "user"
        with st.chat_message(msg["role"], avatar=avatar_definido):
            st.markdown(msg["content"])

    # Lógica de processamento da IA
    if pergunta_usuario := st.chat_input(f"Enviar mensagem para {p_nome}..."):
        with st.chat_message("user"):
            st.markdown(pergunta_usuario)
        historico_atual.append({"role": "user", "content": pergunta_usuario})
        
        api_configurada = False
        if api_key_input:
            genai.configure(api_key=api_key_input)
            api_configurada = True
        elif "GOOGLE_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            api_configurada = True

        if api_configurada:
            try:
                model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=p_dados["system_prompt"])
                historico_formatado = []
                for msg in historico_atual:
                    role_conv = "user" if msg["role"] == "user" else "model"
                    historico_formatado.append({"role": role_conv, "parts": [msg["content"]]})
                
                chat_session = model.start_chat(history=historico_formatado[:-1])
                resposta_ia = chat_session.send_message(pergunta_usuario)
                resposta_final = resposta_ia.text
            except Exception:
                resposta_final = f"*(Erro de comunicação com o motor de IA. Verifique sua chave).* "
        else:
            resposta_final = f"Por favor, insira uma API Key na barra lateral para que eu possa gerar falas automáticas via IA!"

        with st.chat_message("assistant", avatar=p_dados["avatar"]):
            container_texto = st.empty()
            texto_acumulado = ""
            for caractere in resposta_final:
                texto_acumulado += caractere
                time.sleep(0.005)
                container_texto.markdown(texto_acumulado + "▌")
            container_texto.markdown(texto_acumulado)

        historico_atual.append({"role": "assistant", "content": resposta_final})
        st.session_state.historico_global[p_nome] = historico_atual

elif autenticado is False:
    st.error('Usuário/Senha incorretos')
elif autenticado is None:
    st.warning('Efetue o login para acessar a central de personagens. (User: admin | Senha: 123)')
                             
