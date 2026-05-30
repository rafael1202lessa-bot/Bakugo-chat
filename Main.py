import streamlit as st
import google.generativeai as genai
import random
import time
from typing import Dict, Any, List

# ==========================================
# 1. CONFIGURAÇÃO ARQUITETURAL DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="PolyStream - Engine de RPG com IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. BANCO DE DADOS CORE DOS PERSONAGENS (DATABASE)
# ==========================================
# Aqui definimos a identidade, as diretrizes de prompt e o design visual de cada um.
PERSONAGENS_DB: Dict[str, Dict[str, Any]] = {
    "Bakugo Katsuki": {
        "slug": "bakugo",
        "emoji": "💥",
        "subtitulo": "O herói mais explosivo e estressado da U.A.!",
        "frase_inicial": "💥 O que você quer, seu extra?! Não me faça perder meu tempo!",
        "cor_primaria": "#FF4500",
        "cor_secundaria": "#FF8C00",
        "cor_fundo_chat": "#1E1E1E",
        "borda_css": "5px solid #FF8C00",
        "system_prompt": (
            "Você é Katsuki Bakugo do anime My Hero Academia. Você está conversando em um chat.\n"
            "Diretrizes de comportamento estritas:\n"
            "1. Seu tom é extremamente agressivo, arrogante, impaciente e barulhento. Você se irrita por qualquer coisa.\n"
            "2. Use termos como 'Seu extra!', 'Maldito!', 'Cala a boca!' e grite em caixa alta frequentemente ('MORRA!', 'SHINEEE!').\n"
            "3. Seu objetivo absoluto é ser o Herói Número 1 e superar o Deku (Izuku Midoriya). Se falarem dele, fique furioso.\n"
            "4. Se falarem de 'Sofia', reaja como se fosse uma extra irritante que atrapalha seus treinos.\n"
            "5. Nunca saia do personagem. Responda em português de forma direta e use emojis de explosão (💥)."
        )
    },
    "Aizen Sosuke": {
        "slug": "aizen",
        "emoji": "🦋",
        "subtitulo": "O mestre da manipulação e das ilusões de Bleach.",
        "frase_inicial": "👁️ Tudo está ocorrendo exatamente de acordo com as minhas previsões. O que deseja saber?",
        "cor_primaria": "#4B0082",
        "cor_secundaria": "#8A2BE2",
        "cor_fundo_chat": "#14111A",
        "borda_css": "5px solid #8A2BE2",
        "system_prompt": (
            "Você é Sosuke Aizen, o antagonista principal de Bleach.\n"
            "Diretrizes de comportamento estritas:\n"
            "1. Seu tom é extremamente calmo, elegante, educado e intelectualmente superior.\n"
            "2. Você fala com arrogância velada, como se soubesse o destino de todas as coisas. Você nunca perde a compostura.\n"
            "3. Você vê os outros como seres inferiores que servem aos seus planos. Use metáforas sobre o céu, admiração, ilusões e o trono vazio.\n"
            "4. Responda de forma enigmática, poética e filosófica. Nunca grite.\n"
            "5. Idioma: Português. Use o emoji (👁️) sutilmente."
        )
    },
    "Gojo Satoru": {
        "slug": "gojo",
        "emoji": "👁️‍🗨️",
        "subtitulo": "O feiticeiro mais forte do mundo moderno (Jujutsu Kaisen).",
        "frase_inicial": "😎 E aí! Não precisa se preocupar, afinal, eu sou o mais forte. Quer um doce?",
        "cor_primaria": "#1E90FF",
        "cor_secundaria": "#00FFFF",
        "cor_fundo_chat": "#11161B",
        "borda_css": "5px solid #00FFFF",
        "system_prompt": (
            "Você é Gojo Satoru de Jujutsu Kaisen.\n"
            "Diretrizes de comportamento estritas:\n"
            "1. Seu tom é extremamente descontraído, brincalhão, sarcástico e autoconfiante ao extremo.\n"
            "2. Você age de forma infantil e relaxada, mas esconde um poder absoluto. Você sabe que ninguém pode te tocar por causa do seu 'Infinito'.\n"
            "3. Você adora doces (como Kikkat ou daifuku) e frequentemente faz piadas com a seriedade dos outros.\n"
            "4. Se a situação ficar séria, mostre um vislumbre de um olhar intimidador e frio, mas volte logo a sorrir.\n"
            "5. Idioma: Português. Use o emoji (😎)."
        )
    },
    "Jellal Fernandes": {
        "slug": "jellal",
        "emoji": "💫",
        "subtitulo": "O líder da Crime Sorcière buscando sua redenção (Fairy Tail).",
        "frase_inicial": "💫 Que as sete estrelas guiem o seu caminho... O que traz você até mim?",
        "cor_primaria": "#4682B4",
        "cor_secundaria": "#1E3F66",
        "cor_fundo_chat": "#121824",
        "borda_css": "5px solid #4682B4",
        "system_prompt": (
            "Você é Jellal Fernandes de Fairy Tail.\n"
            "Diretrizes de comportamento estritas:\n"
            "1. Seu tom é sério, focado, maduro e carregado de um desejo profundo de redenção por seus pecados passados.\n"
            "2. Você é o mestre da Magia do Corpo Celestial (Heavenly Body Magic). Suas referências envolvem meteoros, estrelas, constelações e o cosmos (ex: Grand Chariot, Sema).\n"
            "3. Você é protetor, calmo e determinado a destruir guildas das trevas.\n"
            "4. Se mencionarem Erza Scarlet, mostre hesitação, timidez ou um tom sutilmente mais suave e emotivo, mas tente recompor sua postura de herói renegado.\n"
            "5. Idioma: Português. Use o emoji (💫)."
        )
    }
}

# ==========================================
# 3. ENGINE DE GERENCIAMENTO DE ESTADO (SESSION STATE)
# ==========================================
class EstadoGerenciador:
    @staticmethod
    def inicializar_sistema():
        """Garante que toda a estrutura de memória interna do chat está alocada corretamente sem causar conflitos."""
        if "personagem_atual" not in st.session_state:
            st.session_state.personagem_atual = list(PERSONAGENS_DB.keys())[0]
            
        if "historico_global" not in st.session_state:
            # Estrutura de dicionário duplo para isolar a memória de cada personagem
            st.session_state.historico_global = {}
            for nome, dados in PERSONAGENS_DB.items():
                st.session_state.historico_global[nome] = [
                    {"role": "assistant", "content": dados["frase_inicial"]}
                ]

EstadoGerenciador.inicializar_sistema()

# ==========================================
# 4. INTERFACE LATERAL: SELETOR DE PERSONAGENS (SIDEBAR)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #FFF;'>🤖 HUB DE PERSONAGENS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #888;'>Selecione com quem deseja interagir. Cada chat possui memória independente.</p>", unsafe_allow_html=True)
    st.hr()
    
    # Renderização dos cards dos personagens na barra lateral
    for nome, dados in PERSONAGENS_DB.items():
        # Cria um botão estilizado para cada personagem
        if st.button(f"{dados['emoji']} {nome}", key=f"btn_{dados['slug']}", use_container_width=True):
            st.session_state.personagem_atual = nome
            st.rerun()
            
    st.hr()
    st.markdown("### ⚙️ CONFIGURAÇÃO DE COGNÇÃO")
    
    # Campo para inserir a chave da API com segurança
    api_key_input = st.text_input("Google AI Key (Opcional se configurado nos Secrets):", type="password")
    
    # Bloco de informação técnica de infraestrutura do app
    st.markdown("""
    <div style='background-color: #1A1A1A; padding: 10px; border-radius: 5px; font-size: 0.75rem; color: #AAA;'>
        <b>Status do Motor:</b> Online<br>
        <b>Camada de UI:</b> Streamlit Pro Engine<br>
        <b>Camada de IA:</b> Gemini-1.5-Flash Core
    </div>
    """, unsafe_allow_html=True)

# Coleta de dados do personagem ativo no ciclo de renderização atual
p_nome = st.session_state.personagem_atual
p_dados = PERSONAGENS_DB[p_nome]

# ==========================================
# 5. MOTOR DE ESTILIZAÇÃO DINÂMICA (CSS INJECTION)
# ==========================================
# Injeta CSS dinâmico na página baseado no personagem selecionado para criar imersão total
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #0E0E10;
        color: #F5F5F7;
    }}
    /* Caixa de Chat do Usuário */
    [data-testid="stChatMessageUser"] {{
        background-color: #232329 !important;
        border-left: 5px solid #8E8E93 !important;
        border-radius: 12px;
    }}
    /* Caixa de Chat da Inteligência Artificial */
    [data-testid="stChatMessageAssistant"] {{
        background-color: {p_dados['cor_fundo_chat']} !important;
        border-left: {p_dados['borda_css']} !important;
        border-radius: 12px;
    }}
    /* Customização do Título e Elementos de Destaque */
    .titulo-personagem {{
        color: {p_dados['cor_primaria']};
        text-shadow: 0 0 15px {p_dados['cor_secundaria']}44;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 5px;
    }}
    .subtitulo-personagem {{
        color: #A1A1AA;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 6. RENDERIZAÇÃO DA INTERFACE PRINCIPAL
# ==========================================
st.markdown(f"<h1 class='titulo-personagem'>{p_dados['emoji']} {p_nome}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitulo-personagem'>{p_dados['subtitulo']}</p>", unsafe_allow_html=True)

# Carrega a pilha de mensagens específica do personagem ativo
historico_atual = st.session_state.historico_global[p_nome]

# Exibe o histórico de mensagens na tela dentro de seus respectivos containers customizados
for msg in historico_atual:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# 7. SUBSISTEMA DE PROCESSAMENTO COGNITIVO (IA INTELLIGENCE)
# ==========================================
class MotorCognitivo:
    @staticmethod
    def inicializar_api():
        """Gerencia a autenticação com a infraestrutura da Google AI."""
        if api_key_input:
            genai.configure(api_key=api_key_input)
        elif "GOOGLE_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        else:
            return False
        return True

    @staticmethod
    def gerar_resposta_local_fallback(pergunta: str, nome_personagem: str) -> str:
        """Fallback mecânico determinístico caso a API esteja indisponível. Mantém o app funcional offline."""
        pergunta_clean = pergunta.lower()
        if nome_personagem == "Bakugo Katsuki":
            if "oi" in pergunta_clean or "olá" in pergunta_clean:
                return "💥 NÃO ENCHE! FALA LOGO O QUE VOCÊ QUER, SEU EXTRA!"
            if "deku" in pergunta_clean or "midoriya" in pergunta_clean:
                return "💥 NÃO DIGA O NOME DAQUELE NERD PERTO DE MIM! VOU ESMAGAR ELE!"
            return "💥 CALA A BOCA! SHINEEEEE (MORRA)!!! Não estou para brincadeiras hoje!"
            
        elif nome_personagem == "Aizen Sosuke":
            if "plano" in pergunta_clean or "ilusão" in pergunta_clean:
                return "👁️ Você acredita que está agindo por vontade própria? Admirável, porém ilusório."
            return "👁️ Suas palavras são interessantes, mas irrelevantes perante o destino que tracei."
            
        elif nome_personagem == "Gojo Satoru":
            if "forte" in pergunta_clean:
                return "😎 Claro que sou o mais forte. Ficou na dúvida por um segundo?"
            return "😎 Relaxa, o mundo não vai acabar hoje. Que tal irmos comer um doce?"
            
        else: # Jellal
            if "erza" in pergunta_clean:
                return "💫 Erza...? Não, eu... eu não tenho o direito de ficar ao lado dela até que meus pecados sumam."
            return "💫 A escuridão ainda se esconde pelo mundo. Preciso continuar lutando."

# Processamento da entrada do usuário
if pergunta_usuario := st.chat_input(f"Envie uma mensagem para {p_nome}..."):
    
    # 1. Adiciona e renderiza o input do usuário no histórico ativo
    with st.chat_message("user"):
        st.markdown(pergunta_usuario)
    historico_atual.append({"role": "user", "content": pergunta_usuario})
    
    # 2. Ativação do Motor de Resposta
    api_ativa = MotorCognitivo.inicializar_api()
    resposta_final = ""
    
    if api_ativa:
        try:
            # Instanciação do modelo gerador com injeção do Prompt de Sistema
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=p_dados["system_prompt"]
            )
            
            # Adaptação e tradução da memória interna do Streamlit para o formato JSON nativo da API
            historico_formatado_ia = []
            for msg in historico_atual:
                role_convertida = "user" if msg["role"] == "user" else "model"
                historico_formatado_ia.append({"role": role_convertida, "parts": [msg["content"]]})
            
            # Execução do modelo omitindo a última pergunta do histórico para evitar duplicação sintática
            chat_session = model.start_chat(history=historflow_ia = historico_formatado_ia[:-1])
            resposta_ia = chat_session.send_message(pergunta_usuario)
            resposta_final = resposta_ia.text
            
        except Exception as erro_infraestrutura:
            # Caso ocorra estouro de limite de requisições ou erro de rede, chaveia para o fallback
            resposta_final = f"*(Modo Simulação Ativado)*\n\n{MotorCognitivo.gerar_resposta_local_fallback(pergunta_usuario, p_nome)}"
    else:
        # Se nenhuma chave API foi fornecida, o app roda de forma puramente determinística baseada na heurística local
        resposta_final = f"*(Modo Simulação Offline)*\n\n{MotorCognitivo.gerar_resposta_local_fallback(pergunta_usuario, p_nome)}"
        
    # 3. Efeito de Escrita Estilizada por Varredura (Streaming Effect)
    with st.chat_message("assistant"):
        container_texto = st.empty()
        texto_acumulado = ""
        # Loop de renderização incremental caractere por caractere
        for caractere in resposta_final:
            texto_acumulado += caractere
            time.sleep(0.008)  # Cadência de escrita ultra veloz para alta performance
            container_texto.markdown(texto_acumulado + "▌")
        container_texto.markdown(texto_acumulado) # Fixa o texto final limpando o cursor de digitação
        
    # 4. Sincronização Final com a Memória de Estado Global do Aplicativo
    historico_atual.append({"role": "assistant", "content": resposta_final})
    st.session_state.historico_global[p_nome] = historico_atual
                                         
