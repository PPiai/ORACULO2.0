import streamlit as st
from langchain-groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
import requests

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

# Configuração da API do Groq Cloud
GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.3-70b-versatile"

# Função para carregar conteúdo das URLs
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

# Carregar os documentos das URLs
def carrega_contexto(tipo_arquivo):
    arquivos = ARQUIVOS.get(tipo_arquivo, [])
    contexto = ""
    for url in arquivos:
        contexto += carrega_site(url) + "\n\n"
    return contexto

# Configuração do modelo LangChain com Groq
@st.cache_resource
def carregar_chain():
    system_message = """
    Você é um assistente chamado Oráculo da V4 Ferraz Piai & CO. 
    Responda com base no contexto fornecido. Se não souber, avise que não encontrou informações suficientes.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{input}")
    ])
    chat = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY)
    memory = ConversationBufferMemory(memory_key="chat_history")
    chain = ConversationChain(llm=chat, memory=memory, prompt=prompt)
    return chain

# Configuração da barra lateral
def sidebar():
    st.sidebar.title("Configuração")
    tipo_arquivo = st.sidebar.selectbox("Selecione sua Área", TIPOS_ARQUIVOS_VALIDOS)
    st.session_state["tipo_arquivo"] = tipo_arquivo

    # Botão para apagar histórico
    if st.sidebar.button("Apagar Histórico"):
        st.session_state["memoria"] = ConversationBufferMemory()

# Página principal do chat
def pagina_chat(chain):
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

        # Carregar contexto baseado na área selecionada
        tipo_arquivo = st.session_state.get("tipo_arquivo", "Tech")
        contexto = carrega_contexto(tipo_arquivo)

        # Adicionar contexto à pergunta
        entrada_completa = f"Contexto: {contexto}\n\nPergunta: {pergunta}"
        resposta = chain.run({"input": entrada_completa})

        # Registrar resposta da IA
        st.session_state["historico"].append({"autor": "ai", "conteudo": resposta})
        st.chat_message("ai").markdown(resposta)

# Função principal
def main():
    sidebar()
    chain = carregar_chain()
    pagina_chat(chain)

if __name__ == "__main__":
    main()
