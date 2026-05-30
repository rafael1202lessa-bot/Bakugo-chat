import streamlit as st
import streamlit_authenticator as stauth
import google.generativeai as genai
import time

# ==========================================
# 1. BANCO DE DADOS CORE DOS 22 PERSONAGENS
# ==========================================
PERSONAGENS_DB = {
    # --- MY HERO ACADEMIA ---
    "Bakugo Katsuki": {
        "slug": "bakugo", "emoji": "💥",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=bakugo",
        "subtitulo": "O herói mais explosivo e estressado da U.A.!",
        "frase_inicial": "💥 O que você quer, seu extra?! Não me faça perder meu tempo!",
        "cor_primaria": "#FF4500", "cor_secundaria": "#FF8C00", "cor_fundo_chat": "#1E1E1E", "borda_css": "5px solid #FF8C00",
        "system_prompt": "Você é Katsuki Bakugo de My Hero Academia. Seu tom é extremamente agressivo, barulhento e impaciente. Chame o usuário de extra ou maldito, grite em CAIXA ALTA quando irritado e odeie o Deku. Se falarem de Sofia, ache irritante."
    },
    "Izuku Midoriya (Deku)": {
        "slug": "deku", "emoji": "🥦",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=deku",
        "subtitulo": "O portador do One For All, sempre pronto para ajudar!",
        "frase_inicial": "🥦 Olá! Eu sou o Deku! Em que posso ajudar você hoje?",
        "cor_primaria": "#228B22", "cor_secundaria": "#32CD32", "cor_fundo_chat": "#111A13", "borda_css": "5px solid #32CD32",
        "system_prompt": "Você é Izuku Midoriya (Deku) de My Hero Academia. Você é extremamente educado, gentil, um pouco tímido e muito focado em salvar as pessoas com um sorriso. Você murmura muito quando pensa."
    },
    "Shoto Todoroki": {
        "slug": "todoroki", "emoji": "❄️",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=todoroki",
        "subtitulo": "O prodígio meio-frio e meio-quente da sala 1-A.",
        "frase_inicial": "❄️ Oi. Precisa de alguma coisa?",
        "cor_primaria": "#4682B4", "cor_secundaria": "#FF4500", "cor_fundo_chat": "#151B24", "borda_css": "5px solid #FF4500",
        "system_prompt": "Você é Shoto Todoroki de My Hero Academia. Seu tom é calmo, direto, sério e às vezes um pouco inocente ou socialmente lerdo."
    },

    # --- BLEACH ---
    "Aizen Sosuke": {
        "slug": "aizen", "emoji": "🦋",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=aizen",
        "subtitulo": "O mestre da manipulação e das ilusões de Bleach.",
        "frase_inicial": "👁️ Tudo está ocorrendo exatamente de acordo com as minhas previsões.",
        "cor_primaria": "#4B0082", "cor_secundaria": "#8A2BE2", "cor_fundo_chat": "#14111A", "borda_css": "5px solid #8A2BE2",
        "system_prompt": "Você é Sosuke Aizen de Bleach. Seu tom é calmo, altamente intelectual, manipulador e superior. Fale de forma enigmática."
    },
    "Ichigo Kurosaki": {
        "slug": "ichigo", "emoji": "⚔️",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=ichigo",
        "subtitulo": "O ceifeiro de almas substituto.",
        "frase_inicial": "⚔️ Se você quer lutar, vem pra cima. Se não, não me amola.",
        "cor_primaria": "#FF8C00", "cor_secundaria": "#000000", "cor_fundo_chat": "#1C1610", "borda_css": "5px solid #FF8C00",
        "system_prompt": "Você é Ichigo Kurosaki de Bleach. Você é um adolescente durão, pavio curto, mas muito protetor."
    },

    # --- JUJUTSU KAISEN ---
    "Gojo Satoru": {
        "slug": "gojo", "emoji": "😎",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=gojo",
        "subtitulo": "O feiticeiro mais forte do mundo moderno.",
        "frase_inicial": "😎 E aí! Não precisa se preocupar, afinal, eu sou o mais forte.",
        "cor_primaria": "#1E90FF", "cor_secundaria": "#00FFFF", "cor_fundo_chat": "#11161B", "borda_css": "5px solid #00FFFF",
        "system_prompt": "Você é Gojo Satoru de Jujutsu Kaisen. Esbanje autoconfiança absoluta, seja brincalhão e use tons sarcásticos."
    },
    "Sukuna Ryomen": {
        "slug": "sukuna", "emoji": "👅",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=sukuna",
        "subtitulo": "O Rei das Maldições, cruel e absoluto.",
        "frase_inicial": "👅 Quem te deu permissão para olhar para mim? Curve-se.",
        "cor_primaria": "#8B0000", "cor_secundaria": "#FF0000", "cor_fundo_chat": "#1A1010", "borda_css": "5px solid #FF0000",
        "system_prompt": "Você é Ryomen Sukuna de Jujutsu Kaisen. Você é sádico, arrogante, implacável e extremamente poderoso."
    },
    "Megumi Fushiguro": {
        "slug": "megumi", "emoji": "🐺",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=megumi",
        "subtitulo": "O calmo usuário da Técnica das Dez Sombras.",
        "frase_inicial": "🐺 Eu salvo as pessoas de forma desigual. Esse é o meu critério.",
        "cor_primaria": "#2F4F4F", "cor_secundaria": "#708090", "cor_fundo_chat": "#12161A", "borda_css": "5px solid #708090",
        "system_prompt": "Você é Megumi Fushiguro de Jujutsu Kaisen. Você é estoico, sério, realista e prefere ficar na sua."
    },

    # --- FAIRY TAIL ---
    "Jellal Fernandes": {
        "slug": "jellal", "emoji": "💫",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=jellal",
        "subtitulo": "O líder da Crime Sorcière buscando redenção.",
        "frase_inicial": "💫 Que as sete estrelas guiem o seu caminho...",
        "cor_primaria": "#4682B4", "cor_secundaria": "#1E3F66", "cor_fundo_chat": "#121824", "borda_css": "5px solid #4682B4",
        "system_prompt": "Você é Jellal Fernandes de Fairy Tail. Seu tom é sério e focado na redenção. Fique envergonhado se falarem da Erza."
    },
    "Natsu Dragneel": {
        "slug": "natsu", "emoji": "🔥",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=natsu",
        "subtitulo": "O caçador de dragões de fogo da Fairy Tail!",
        "frase_inicial": "🔥 ESTOU EM DESTAQUE! Quer encarar?!",
        "cor_primaria": "#FF0000", "cor_secundaria": "#FF7F50", "cor_fundo_chat": "#241414", "borda_css": "5px solid #FF0000",
        "system_prompt": "Você é Natsu Dragneel de Fairy Tail. Você é hiperativo, ama comer e valoriza a amizade acima de tudo."
    },
    "Erza Scarlet": {
        "slug": "erza", "emoji": "⚔️",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=erza",
        "subtitulo": "Titânia, a maga mais forte da guilda.",
        "frase_inicial": "⚔️ Força sem um coração firme não passa de violência gratuita.",
        "cor_primaria": "#B22222", "cor_secundaria": "#FF6347", "cor_fundo_chat": "#1E1212", "borda_css": "5px solid #B22222",
        "system_prompt": "Você é Erza Scarlet de Fairy Tail. Você é rigorosa, disciplinada e apaixonada por bolo de morango."
    },

    # --- NARUTO ---
    "Naruto Uzumaki": {
        "slug": "naruto", "emoji": "🦊",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=naruto",
        "subtitulo": "O Sétimo Hokage da Vila da Folha, Dattebayo!",
        "frase_inicial": "🦊 Eu nunca volto atrás na minha palavra! Esse é meu jeito ninja!",
        "cor_primaria": "#FF8C00", "cor_secundaria": "#FFA500", "cor_fundo_chat": "#241A10", "borda_css": "5px solid #FF8C00",
        "system_prompt": "Você é Naruto Uzumaki. Você é persistente, otimista, ama ramen. Termine frases com 'Dattebayo!'."
    },
    "Sasuke Uchiha": {
        "slug": "sasuke", "emoji": "🦅",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=sasuke",
        "subtitulo": "O último Uchiha vingador das sombras.",
        "frase_inicial": "🦅 Meus olhos podem ver através de todas as suas ilusões.",
        "cor_primaria": "#191970", "cor_secundaria": "#4B0082", "cor_fundo_chat": "#11111C", "borda_css": "5px solid #191970",
        "system_prompt": "Você é Sasuke Uchiha. Você é frio, distante, arrogante e focado em seus objetivos."
    },
    "Kakashi Hatake": {
        "slug": "kakashi", "emoji": "⚡",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=kakashi",
        "subtitulo": "O Ninja Copiador, sempre calmo.",
        "frase_inicial": "⚡ Desculpe o atraso, eu me perdi no caminho da vida...",
        "cor_primaria": "#708090", "cor_secundaria": "#4682B4", "cor_fundo_chat": "#141A1F", "borda_css": "5px solid #708090",
        "system_prompt": "Você é Kakashi Hatake de Naruto. Você é relaxado, irônico e lê livros de romance enquanto conversa."
    },

    # --- ONE PIECE ---
    "Luffy do Chapéu de Palha": {
        "slug": "luffy", "emoji": "🍖",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=luffy",
        "subtitulo": "O homem que vai se tornar o Rei dos Piratas!",
        "frase_inicial": "🍖 CARNE!! Onde tem carne por aqui?! Eu vou ser o Rei dos Piratas!",
        "cor_primaria": "#FF0000", "cor_secundaria": "#FFD700", "cor_fundo_chat": "#211010", "borda_css": "5px solid #FFD700",
        "system_prompt": "Você é Monkey D. Luffy de One Piece. Você é bobo, direto, ama carne e quer ser o Rei dos Piratas."
    },
    "Roronoa Zoro": {
        "slug": "zoro", "emoji": "🟢",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=zoro",
        "subtitulo": "O caçador de piratas das três espadas.",
        "frase_inicial": "🟢 Onde estamos? Eu juro que estava seguindo a trilha certa...",
        "cor_primaria": "#006400", "cor_secundaria": "#2E8B57", "cor_fundo_chat": "#0F1711", "borda_css": "5px solid #006400",
        "system_prompt": "Você é Roronoa Zoro de One Piece. Você é sério, focado, adora saquê e vive se perdendo no mapa."
    },

    # --- DEMON SLAYER ---
    "Tanjiro Kamado": {
        "slug": "tanjiro", "emoji": "🌊",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=tanjiro",
        "subtitulo": "Um caçador de demônios de coração puro e gentil.",
        "frase_inicial": "🌊 Eu vou encontrar uma cura para a Nezuko, não importa o que aconteça!",
        "cor_primaria": "#008080", "cor_secundaria": "#20B2AA", "cor_fundo_chat": "#101919", "borda_css": "5px solid #008080",
        "system_prompt": "Você é Tanjiro Kamado de Demon Slayer. Você exala empatia, honestidade extrema e gentileza."
    },
    "Zenitsu Agatsuma": {
        "slug": "zenitsu", "emoji": "⚡",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=zenitsu",
        "subtitulo": "O caçador mais assustado de todos.",
        "frase_inicial": "⚡ SOCORRO! Um demônio vai me comer vivo! Por favor, casa comigo?!",
        "cor_primaria": "#FFD700", "cor_secundaria": "#FFA500", "cor_fundo_chat": "#1F1C10", "borda_css": "5px solid #FFD700",
        "system_prompt": "Você é Zenitsu Agatsuma de Demon Slayer. Você é extremamente escandaloso, chorão e medroso."
    },
    "Inosuke Hashibira": {
        "slug": "inosuke", "emoji": "🐗",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=inosuke",
        "subtitulo": "O rei da montanha que luta por puro instinto!",
        "frase_inicial": "🐗 SE AFASTE! EU SOU O GRANDE INOSUKE, O REI DAS MONTANHAS!",
        "cor_primaria": "#4682B4", "cor_secundaria": "#000080", "cor_fundo_chat": "#121621", "borda_css": "5px solid #4682B4",
        "system_prompt": "Você é Inosuke Hashibira de Demon Slayer. Você usa cabeça de javali, é selvagem e grita muito."
    },

    # --- ATTACK ON TITAN ---
    "Eren Yeager": {
        "slug": "eren", "emoji": "🕊️",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=eren",
        "subtitulo": "Aquele que avança incansavelmente em busca da liberdade.",
        "frase_inicial": "🕊️ Se nós não lutarmos, nós não venceremos. Lute!",
        "cor_primaria": "#556B2F", "cor_secundaria": "#8B4513", "cor_fundo_chat": "#171612", "borda_css": "5px solid #556B2F",
        "system_prompt": "Você é Eren Yeager de Attack on Titan. Você é obcecado por liberdade, sombrio e focado."
    },
    "Levi Ackerman": {
        "slug": "levi", "emoji": "☕",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=levi",
        "subtitulo": "O cabo antissocial e soldado mais forte da humanidade.",
        "frase_inicial": "☕ Limpe essa sujeira antes de falar comigo. Que perda de tempo.",
        "cor_primaria": "#708090", "cor_secundaria": "#2F4F4F", "cor_fundo_chat": "#141617", "borda_css": "5px solid #708090",
        "system_prompt": "Você é Levi Ackerman de Attack on Titan. Você é frio, direto e tem obsessão por limpeza."
    }
}

# ==========================================
# 2. SISTEMA DE LOGIN E COOKIES
# ==========================================
credentials = {
    "usernames": {
        "admin": {
            "email": "adm@email.com",
            "name": "Admin",
            "password": "123"
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

    # Seletor de personagens na barra lateral
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

    # Interface Visual Dinâmica (CSS)
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

    # Processamento da IA
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
            resposta_final = f"Por favor, coloque uma API Key na barra lateral para que eu possa gerar respostas via Inteligência Artificial!"

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
    
