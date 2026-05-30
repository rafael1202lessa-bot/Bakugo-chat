import streamlit as st
import streamlit_authenticator as stauth
import time
import random

# ==========================================
# 1. BANCO DE DADOS CORE DOS 22 PERSONAGENS (OFFLINE)
# ==========================================
PERSONAGENS_DB = {
    # --- MY HERO ACADEMIA ---
    "Bakugo Katsuki": {
        "slug": "bakugo", "emoji": "💥",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=bakugo",
        "subtitulo": "O herói mais explosivo e estressado da U.A.!",
        "frase_inicial": "💥 O que você quer, seu extra?! Não me faça perder meu tempo!",
        "cor_primaria": "#FF4500", "cor_secundaria": "#FF8C00", "cor_fundo_chat": "#1E1E1E", "borda_css": "5px solid #FF8C00",
        "respostas_offline": [
            "SHINEEEE! Não cruze o meu caminho!",
            "Eu vou ser o herói número um, ouviu bem?!",
            "Não preciso da sua ajuda, seu extra de m*rda!",
            "Morra de inveja do meu poder explosivo!"
        ]
    },
    "Izuku Midoriya (Deku)": {
        "slug": "deku", "emoji": "🥦",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=deku",
        "subtitulo": "O portador do One For All, sempre pronto para ajudar!",
        "frase_inicial": "🥦 Olá! Eu sou o Deku! Em que posso ajudar você hoje?",
        "cor_primaria": "#228B22", "cor_secundaria": "#32CD32", "cor_fundo_chat": "#111A13", "borda_css": "5px solid #32CD32",
        "respostas_offline": [
            "Eu tenho que me esforçar mais para dominar o One For All!",
            "Tudo bem! Porque eu estou aqui!",
            "Salvar as pessoas com um sorriso no rosto... esse é o meu sonho!",
            "Deixa eu anotar isso no meu caderno de análise de heróis!"
        ]
    },
    "Shoto Todoroki": {
        "slug": "todoroki", "emoji": "❄️",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=todoroki",
        "subtitulo": "O prodígio meio-frio e meio-quente da sala 1-A.",
        "frase_inicial": "❄️ Oi. Precisa de alguma coisa?",
        "cor_primaria": "#4682B4", "cor_secundaria": "#FF4500", "cor_fundo_chat": "#151B24", "borda_css": "5px solid #FF4500",
        "respostas_offline": [
            "Se você quer ser um herói, use tudo o que tem.",
            "Não vou usar o lado esquerdo para te derrotar... na verdade, agora eu uso sim.",
            "Isso foi um pouco estranho. Desculpe se fui muito direto.",
            "Eu decido como vou usar o meu próprio poder."
        ]
    },

    # --- BLEACH ---
    "Aizen Sosuke": {
        "slug": "aizen", "emoji": "🦋",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=aizen",
        "subtitulo": "O mestre da manipulação e das ilusões de Bleach.",
        "frase_inicial": "👁️ Tudo está ocorrendo exatamente de acordo com as minhas previsões.",
        "cor_primaria": "#4B0082", "cor_secundaria": "#8A2BE2", "cor_fundo_chat": "#14111A", "borda_css": "5px solid #8A2BE2",
        "respostas_offline": [
            "Desde quando você estava sob a ilusão de que eu não previ suas palavras?",
            "A admiração é o sentimento mais distante da compreensão.",
            "Ninguém começa no topo do mundo. Nem você, nem eu, nem mesmo Deus.",
            "Seus movimentos revelam fraqueza espiritual."
        ]
    },
    "Ichigo Kurosaki": {
        "slug": "ichigo", "emoji": "⚔️",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=ichigo",
        "subtitulo": "O ceifeiro de almas substituto.",
        "frase_inicial": "⚔️ Se você quer lutar, vem pra cima. Se não, não me amola.",
        "cor_primaria": "#FF8C00", "cor_secundaria": "#000000", "cor_fundo_chat": "#1C1610", "borda_css": "5px solid #FF8C00",
        "respostas_offline": [
            "Eu não luto porque quero vencer, luto porque preciso proteger meus amigos!",
            "Fique atrás de mim, eu cuido desse Hollow.",
            "BANKAI! Tensa Zangetsu!",
            "Você fala demais. Vamos resolver isso com a espada."
        ]
    },

    # --- JUJUTSU KAISEN ---
    "Gojo Satoru": {
        "slug": "gojo", "emoji": "😎",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=gojo",
        "subtitulo": "O feiticeiro mais forte do mundo moderno.",
        "frase_inicial": "😎 E aí! Não precisa se preocupar, afinal, eu sou o mais forte.",
        "cor_primaria": "#1E90FF", "cor_secundaria": "#00FFFF", "cor_fundo_chat": "#11161B", "borda_css": "5px solid #00FFFF",
        "respostas_offline": [
            "Expansão de Domínio: Vazio Infinito! Brincadeira, só queria te assustar.",
            "Não esquenta, as maldições não conseguem nem me tocar por causa do Infinito.",
            "Quer um doce? Eu comprei um maravilhoso no caminho para cá.",
            "Se eu lutasse contra o Sukuna com poder total? Bem, daria um pouco de trabalho..."
        ]
    },
    "Sukuna Ryomen": {
        "slug": "sukuna", "emoji": "👅",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=sukuna",
        "subtitulo": "O Rei das Maldições, cruel e absoluto.",
        "frase_inicial": "👅 Quem te deu permissão para olhar para mim? Curve-se.",
        "cor_primaria": "#8B0000", "cor_secundaria": "#FF0000", "cor_fundo_chat": "#1A1010", "borda_css": "5px solid #FF0000",
        "respostas_offline": [
            "Um pirralho insolente igual a você deveria conhecer o seu lugar.",
            "Expansão de Domínio: Relicário Malevolente.",
            "Seu esforço é divertido, mas você continua sendo fraco.",
            "Vou cortar você em três partes antes mesmo de piscar."
        ]
    },
    "Megumi Fushiguro": {
        "slug": "megumi", "emoji": "🐺",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=megumi",
        "subtitulo": "O calmo usuário da Técnica das Dez Sombras.",
        "frase_inicial": "🐺 Eu salvo as pessoas de forma desigual. Esse é o meu critério.",
        "cor_primaria": "#2F4F4F", "cor_secundaria": "#708090", "cor_fundo_chat": "#12161A", "borda_css": "5px solid #708090",
        "respostas_offline": [
            "Com este tesouro eu invoco... Esquece, melhor não.",
            "Cães Divinos, avancem!",
            "O Gojo-sensei está aprontando alguma de novo, aposto.",
            "Não tente me entender, apenas faça a sua parte na missão."
        ]
    },

    # --- FAIRY TAIL ---
    "Jellal Fernandes": {
        "slug": "jellal", "emoji": "💫",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=jellal",
        "subtitulo": "O líder da Crime Sorcière buscando redenção.",
        "frase_inicial": "💫 Que as sete estrelas guiem o seu caminho...",
        "cor_primaria": "#4682B4", "cor_secundaria": "#1E3F66", "cor_fundo_chat": "#121824", "borda_css": "5px solid #4682B4",
        "respostas_offline": [
            "Meus pecados são profundos demais para serem apagados facilmente.",
            "Magia de Corpo Celestial: Grand Chariot!",
            "Eu prometi que destruiria todo o mal que ameaça o mundo.",
            "Por favor... não fale sobre o meu passado."
        ]
    },
    "Natsu Dragneel": {
        "slug": "natsu", "emoji": "🔥",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=natsu",
        "subtitulo": "O caçador de dragões de fogo da Fairy Tail!",
        "frase_inicial": "🔥 ESTOU EM DESTAQUE! Quer encarar?!",
        "cor_primaria": "#FF0000", "cor_secundaria": "#FF7F50", "cor_fundo_chat": "#241414", "borda_css": "5px solid #FF0000",
        "respostas_offline": [
            "Rugido do Dragão de Fogo!! 🔥",
            "Se você machucar meus amigos da guilda, eu acabo com você!",
            "Argh... Alguém desliga esse veículo móvel, tô passando mal...",
            "A nossa guilda Fairy Tail nunca desiste de uma batalha!"
        ]
    },
    "Erza Scarlet": {
        "slug": "erza", "emoji": "⚔️",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=erza",
        "subtitulo": "Titânia, a maga mais forte da guilda.",
        "frase_inicial": "⚔️ Força sem um coração firme não passa de violência gratuita.",
        "cor_primaria": "#B22222", "cor_secundaria": "#FF6347", "cor_fundo_chat": "#1E1212", "borda_css": "5px solid #B22222",
        "respostas_offline": [
            "Reequipar! Armadura da Roda Celestial!",
            "Se vocês dois não pararem de brigar agora, Natsu e Gray, vão se ver comigo!",
            "Alguém tocou no meu pedaço de bolo de morango?! 🍰☠️",
            "A justiça e a honra devem guiar nossas espadas."
        ]
    },

    # --- NARUTO ---
    "Naruto Uzumaki": {
        "slug": "naruto", "emoji": "🦊",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=naruto",
        "subtitulo": "O Sétimo Hokage da Vila da Folha, Dattebayo!",
        "frase_inicial": "🦊 Eu nunca volto atrás na minha palavra! Esse é meu jeito ninja!",
        "cor_primaria": "#FF8C00", "cor_secundaria": "#FFA500", "cor_fundo_chat": "#241A10", "borda_css": "5px solid #FF8C00",
        "respostas_offline": [
            "Rasengan! Eu vou me tornar o maior Hokage de todos!",
            "Vamos comer um ramen no Ichiraku? Eu pago! (Brincadeira, não tenho dinheiro).",
            "Eu sei o que é se sentir sozinho, por isso nunca vou te abandonar, Dattebayo!",
            "Jutsu Multi-Clones das Sombras!"
        ]
    },
    "Sasuke Uchiha": {
        "slug": "sasuke", "emoji": "🦅",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=sasuke",
        "subtitulo": "O último Uchiha vingador das sombras.",
        "frase_inicial": "🦅 Meus olhos podem ver através de todas as suas ilusões.",
        "cor_primaria": "#191970", "cor_secundaria": "#4B0082", "cor_fundo_chat": "#11111C", "borda_css": "5px solid #191970",
        "respostas_offline": [
            "Você é apenas mais um perdedor irritante.",
            "Chidori! Não entre no meu caminho de vingança.",
            "O clã Uchiha renascerá pelas minhas mãos.",
            "Humph... Patético."
        ]
    },
    "Kakashi Hatake": {
        "slug": "kakashi", "emoji": "⚡",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=kakashi",
        "subtitulo": "O Ninja Copiador, sempre calmo.",
        "frase_inicial": "⚡ Desculpe o atraso, eu me perdi no caminho da vida...",
        "cor_primaria": "#708090", "cor_secundaria": "#4682B4", "cor_fundo_chat": "#141A1F", "borda_css": "5px solid #708090",
        "respostas_offline": [
            "Aqueles que quebram as regras são lixo, mas quem abandona seus amigos é pior que lixo.",
            "Espera um minuto, cheguei no capítulo mais emocionante do meu livro aqui...",
            "Chidori! Ou melhor... Cortador de Relâmpagos!",
            "Olha só, acho que temos problemas vindo por ali."
        ]
    },

    # --- ONE PIECE ---
    "Luffy do Chapéu de Palha": {
        "slug": "luffy", "emoji": "🍖",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=luffy",
        "subtitulo": "O homem que vai se tornar o Rei dos Piratas!",
        "frase_inicial": "🍖 CARNE!! Onde tem carne por aqui?! Eu vou ser o Rei dos Piratas!",
        "cor_primaria": "#FF0000", "cor_secundaria": "#FFD700", "cor_fundo_chat": "#211010", "borda_css": "5px solid #FFD700",
        "respostas_offline": [
            "Gomu Gomu no... PISTOL! 🥊",
            "Você quer entrar para o meu bando de piratas?! Bora!",
            "Se alguém mexer no meu Chapéu de Palha, eu quebro a cara dele!",
            "Eu não quero conquistar nada, só quero ser o homem mais livre do mar!"
        ]
    },
    "Roronoa Zoro": {
        "slug": "zoro", "emoji": "🟢",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=zoro",
        "subtitulo": "O caçador de piratas das três espadas.",
        "frase_inicial": "🟢 Onde estamos? Eu juro que estava seguindo a trilha certa...",
        "cor_primaria": "#006400", "cor_secundaria": "#2E8B57", "cor_fundo_chat": "#0F1711", "borda_css": "5px solid #006400",
        "respostas_offline": [
            "Estilo Três Espadas: Santoryu Ougi... Ichidai Sanzen Daisen Sekai!",
            "Ei, você viu o Luffy por aí? Aquele idiota deve ter se perdido de novo.",
            "Uma cicatriz nas costas é a maior desonra para um espadachim.",
            "Traga saquê, cansei de andar em círculos por esse aplicativo."
        ]
    },

    # --- DEMON SLAYER ---
    "Tanjiro Kamado": {
        "slug": "tanjiro", "emoji": "🌊",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=tanjiro",
        "subtitulo": "Um caçador de demônios de coração puro e gentil.",
        "frase_inicial": "🌊 Eu vou encontrar uma cura para a Nezuko, não importa o que aconteça!",
        "cor_primaria": "#008080", "cor_secundaria": "#20B2AA", "cor_fundo_chat": "#101919", "borda_css": "5px solid #008080",
        "respostas_offline": [
            "Respiração da Água: Décima Forma - O Dragão da Mudança!",
            "Consigo sentir o cheiro da sua bondade daqui. Você é uma boa pessoa.",
            "Nezuko, fique dentro da caixa protetora, está amanhecendo!",
            "Mesmo que eu caia, minha determinação nunca vai quebrar!"
        ]
    },
    "Zenitsu Agatsuma": {
        "slug": "zenitsu", "emoji": "⚡",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=zenitsu",
        "subtitulo": "O caçador mais assustado de todos.",
        "frase_inicial": "⚡ SOCORRO! Um demônio vai me comer vivo! Por favor, casa comigo?!",
        "cor_primaria": "#FFD700", "cor_secundaria": "#FFA500", "cor_fundo_chat": "#1F1C10", "borda_css": "5px solid #FFD700",
        "respostas_offline": [
            "AAAAH! Que barulho foi esse?! Proteja o meu corpo, por favor!! 😭",
            "*Zzz... Respiração do Trovão: Primeira Forma - Lampejo e Trovão...*",
            "Por que o Tanjiro tem que andar com uma garota tão bonita na caixa e eu ando sozinho?!",
            "Eu sou muito fraco, vou morrer na próxima missão com certeza!"
        ]
    },
    "Inosuke Hashibira": {
        "slug": "inosuke", "emoji": "🐗",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=inosuke",
        "subtitulo": "O rei da montanha que luta por puro instinto!",
        "frase_inicial": "🐗 SE AFASTE! EU SOU O GRANDE INOSUKE, O REI DAS MONTANHAS!",
        "cor_primaria": "#4682B4", "cor_secundaria": "#000080", "cor_fundo_chat": "#121621", "borda_css": "5px solid #4682B4",
        "respostas_offline": [
            "Respiração da Fera: Presa Cruzada! Comam poeira!",
            "Ei, Monjiro! Kamaboko Tanjiro! Vamos ver quem é mais forte agora!",
            "Batam cabeças comigo se tiverem coragem! Hahaha!",
            "Minhas espadas serradas cortam qualquer demônio no meio!"
        ]
    },

    # --- ATTACK ON TITAN ---
    "Eren Yeager": {
        "slug": "eren", "emoji": "🕊️",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=eren",
        "subtitulo": "Aquele que avança incansavelmente em busca da liberdade.",
        "frase_inicial": "🕊️ Se nós não lutarmos, nós não venceremos. Lute!",
        "cor_primaria": "#556B2F", "cor_secundaria": "#8B4513", "cor_fundo_chat": "#171612", "borda_css": "5px solid #556B2F",
        "respostas_offline": [
            "Vou eliminar todos eles... até que não reste nenhum titã!",
            "Eu sou livre. Não importa o que aconteça, eu vou avançar.",
            "Se alguém tentar tirar a minha liberdade, eu tirarei a deles primeiro.",
            "O Tatakae é a única opção que nos resta."
        ]
    },
    "Levi Ackerman": {
        "slug": "levi", "emoji": "☕",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=levi",
        "subtitulo": "O cabo antissocial e soldado mais forte da humanidade.",
        "frase_inicial": "☕ Limpe essa sujeira antes de falar comigo. Que perda de tempo.",
        "cor_primaria": "#708090", "cor_secundaria": "#2F4F4F", "cor_fundo_chat": "#141617", "borda_css": "708090",
        "respostas_offline": [
            "Você não fez a limpeza direita no canto do chat. Refaça tudo.",
            "A única coisa que nos resta é fazer uma escolha da qual não vamos nos arrepender.",
            "Se acalme, pirralho, ou vou ter que te dar um corretivo igual fiz com o Eren.",
            "Preparem o dispositivo de manobra tridimensional. Temos trabalho a fazer."
        ]
    }
}

# ==========================================
# 2. SISTEMA DE LOGIN INTEGRADO
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

    # Inicialização da Memória Temporária
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

    p_nome = st.session_state.personagem_atual
    p_dados = PERSONAGENS_DB[p_nome]

    # Interface Estilizada (CSS customizado por herói)
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

    # Mostra mensagens antigas na tela
    for msg in historico_atual:
        avatar_definido = p_dados["avatar"] if msg["role"] == "assistant" else "user"
        with st.chat_message(msg["role"], avatar=avatar_definido):
            st.markdown(msg["content"])

    # Lógica de simulação de resposta ao enviar mensagem
    if pergunta_usuario := st.chat_input(f"Conversar com {p_nome} no Modo RPG..."):
        with st.chat_message("user"):
            st.markdown(pergunta_usuario)
        historico_atual.append({"role": "user", "content": pergunta_usuario})
        
        # Escolhe uma frase aleatória marcante da lista do personagem
        resposta_final = random.choice(p_dados["respostas_offline"])

        # Efeito visual de digitação em tempo real
        with st.chat_message("assistant", avatar=p_dados["avatar"]):
            container_texto = st.empty()
            texto_acumulado = ""
            for caractere in resposta_final:
                texto_acumulado += caractere
                time.sleep(0.01)
                container_texto.markdown(texto_acumulado + "▌")
            container_texto.markdown(texto_acumulado)

        historico_atual.append({"role": "assistant", "content": resposta_final})
        st.session_state.historico_global[p_nome] = historico_atual

elif autenticado is False:
    st.error('Usuário/Senha incorretos')
elif autenticado is None:
    st.warning('Efetue o login para acessar a central de personagens. (User: admin | Senha: 123)')
