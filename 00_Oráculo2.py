import streamlit as st
import requests
from bs4 import BeautifulSoup

# Configuração inicial
TIPOS_ARQUIVOS_VALIDOS = [
    'Tech',
    'Social Media',
    'Gestor de Tráfego',
    'Account',
    'Vendas'
]

ARQUIVOS = {
    'Tech': ['https://vendas.v4company.com/glossario-marketing/'],
    'Social Media': ['https://vendas.v4company.com/glossario-marketing/'],
    'Gestor de Tráfego': ['https://vendas.v4company.com/glossario-marketing/'],
    'Account': ['https://vendas.v4company.com/glossario-marketing/'],
    'Vendas': ['https://vendas.v4company.com/glossario-marketing/'],
}

GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/v1/chat/completions"

# Função para carregar o conteúdo das URLs
def carrega_site(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text(separator=" ", strip=True)
        else:
            return f"Erro ao carregar o site: {response.status_code}"
    except Exception as e:
        return f"Erro ao conectar: {e}"

# Função para gerar respostas usando a API do Groq Cloud
def criar_resposta_groq(pergunta, contexto):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Você é um assistente chamado Oráculo da V4 Ferraz Piai & CO."},
            {"role": "user", "content": f"Contexto: {contexto}\n\nPergunta: {pergunta}"}
        ]
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        if response.status_code == 200:
            resposta = response.json()
            return resposta["choices"][0]["message"]["content"]
        else:
            return f"Erro na API do Groq: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Erro ao conectar à API do Groq: {e}"

# Configuração da barra lateral
def sidebar():
    st.sidebar.title("Configuração")
    
    # Seleção da base de conhecimento
    tipo_arquivo = st.sidebar.selectbox("Selecione sua Área", TIPOS_ARQUIVOS_VALIDOS)
    st.session_state["tipo_arquivo"] = tipo_arquivo

    # Botão para apagar histórico
    if st.sidebar.button("Apagar Histórico"):
        st.session_state["historico"] = []

# Página principal do chat
def pagina_chat():
    st.title("🤖 Bem-vindo ao Oráculo")
    st.divider()

    # Inicializar histórico de mensagens
    if "historico" not in st.session_state:
        st.session_state["historico"] = []

    # Exibir histórico de mensagens
    for mensagem in st.session_state["historico"]:
        st.chat_message(mensagem["autor"]).markdown(mensagem["conteudo"])

    # Entrada do usuário
    pergunta = st.chat_input("Fale com o Oráculo")
    if pergunta:
        # Registrar pergunta do usuário
        st.session_state["historico"].append({"autor": "human", "conteudo": pergunta})
        st.chat_message("human").markdown(pergunta)

        # Obter o contexto carregado
        tipo_arquivo = st.session_state.get("tipo_arquivo", "Tech")
        arquivos = ARQUIVOS.get(tipo_arquivo, [])
        contexto = ""
        for url in arquivos:
            contexto += carrega_site(url) + "\n\n"

        # Gerar resposta com a API do Groq Cloud
        resposta = criar_resposta_groq(pergunta, contexto)

        # Registrar resposta da IA
        st.session_state["historico"].append({"autor": "ai", "conteudo": resposta})
        st.chat_message("ai").markdown(resposta)

# Função principal
def main():
    sidebar()
    pagina_chat()

if __name__ == "__main__":
    main()
