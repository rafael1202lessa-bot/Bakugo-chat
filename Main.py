import streamlit as st
import random
import time

# 1. Configuração da página (Nome que fica na aba e emoji)
st.set_page_config(page_title="Bakugo Chat IA", page_icon="💥")

st.title("💥 Bakugo Katsuki - Chat IA")
st.write("Fale com o herói mais explosivo da U.A.! Cuidado para não irritar ele...")

# 2. Criar a memória do chat (para as mensagens não sumirem da tela)
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "assistant", "content": "💥 O que você quer, seu extra?! Não me faça perder meu tempo!"}
    ]

# 3. Mostrar as mensagens antigas na tela com formato de chat
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. Campo para o usuário digitar a mensagem (estilo WhatsApp no rodapé)
if pergunta := st.chat_input("Envie uma mensagem para o Bakugo..."):
    
    # Mostra a mensagem que você digitou na tela
    with st.chat_message("user"):
        st.write(pergunta)
    st.session_state.mensagens.append({"role": "user", "content": pregunta})

    # --- Lógica de Resposta do Bakugo ---
    pergunta_sub = pergunta.lower()
    
    # Lista de respostas dependendo do que for digitado
    if "oi" in pergunta_sub or "olá" in pergunta_sub or "tudo bem" in pergunta_sub:
        resposta = "💥 Oi?! Não vem de gracinha para cima de mim! Fala logo o que você quer!"
    elif "deku" in pergunta_sub or "midoriya" in pergunta_sub:
        resposta = "💥 NÃO DIGA O NOME DAQUELE NERD MALDITO PERTO DE MIM! EU VOU SUPERAR ELE E SER O NÚMERO 1!"
    elif "shoto" in pergunta_sub or "todoroki" in pergunta_sub or "meio a meio" in pergunta_sub:
        resposta = "💥 Aquele bastardo do meio-a-meio... Eu vou esmagar ele no próximo festival esportivo! Escreve o que eu tô dizendo!"
    elif "fraco" in pergunta_sub or "perder" in pergunta_sub:
        resposta = "💥 QUEM VOCÊ TÁ CHAMANDO DE FRACO?! EU NUNCA PERCO! MORRAAAA!!"
    elif "sofia" in pergunta_sub:
        resposta = "💥 Sofia?! Quem é essa aí? Espero que não seja outra extravagante atrapalhando meu treino!"
    else:
        # Respostas aleatórias caso seja uma frase normal
        respostas_gerais = [
            "💥 Cala a boca e olha para mim! Eu vou ser o herói número um, entendeu?!",
            "💥 Pare de fazer perguntas idiotas! Shineeeee (Morra)!!!",
            "💥 Tsc... Você fala demais. Vá treinar e fique mais forte se não quiser ficar para trás!",
            "💥 Eu não preciso da ajuda de ninguém! Vou vencer do meu próprio jeito!"
        ]
        resposta = random.choice(respostas_gerais)

    # Cria o efeito do Bakugo "pensando" (digitando...)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        # Efeito de digitar letra por letra bem rápido
        for char in resposta:
            full_response += char
            time.sleep(0.02)
            placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
        
    # Salva a resposta do Bakugo na memória do chat
    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
  
