import streamlit as st
from llama_index import GPTSimpleVectorIndex, Document, SimpleKeywordTableIndex
from llama_index.indices.base import BaseGPTIndex
from llama_index.llms import LlamaGroq
from llama_index.prompts.prompts import QuestionAnswerPrompt
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

# Função para carregar documentos e criar índice
@st.cache_resource
def criar_indice(tipo_arquivo: str) -> BaseGPTIndex:
    arquivos = ARQUIVOS.get(tipo_arquivo, [])
    documentos = []
    for url in arquivos:
        conteudo = carrega_site(url)
        documentos.append(Document(conteudo))
    
    # Criar índice com os documentos carregados
    index = GPTSimpleVectorIndex(documents=documentos)
    return index

# Configurar modelo Groq com LlamaIndex
@st.cache_resource
def configurar_llm():
    llm = LlamaGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY)
    return llm

# Sidebar do Streamlit
def sidebar():
    st.sidebar.title("Configuração")
    tipo_arquivo = st.sidebar.selectbox("Selecione sua Área", TIPOS_ARQUIVOS_VALIDOS)
    st.session_state["tipo_arquivo"] = tipo_arquivo

    if st.sidebar.button("Apagar Histórico"):
        st.session_state["historico"] = []

# Página principal do chat
def pagina_chat(llm, index):
    st.title("🤖 Bem-vindo ao Oráculo")
    st.divider()

    if "historico" not in st.session_state:
        st.session_state["historico"] = []

    # Exibir histórico de mensagens
    for mensagem in st.session_state["historico"]:
        st.chat_message(mensagem["autor"]).markdown(mensagem["conteudo"])

    pergunta = st.chat_input("Fale com o Oráculo")
    if pergunta:
        # Exibir pergunta no chat
        st.session_state["historico"].append({"autor": "human", "conteudo": pergunta})
        st.chat_message("human").markdown(pergunta)

        # Gerar resposta
        query_prompt = QuestionAnswerPrompt("Pergunta: {query}\n\nResposta:")
        resposta = index.query(query=pergunta, llm=llm, query_prompt=query_prompt)

        # Adicionar resposta ao histórico
        st.session_state["historico"].append({"autor": "ai", "conteudo": resposta.response})
        st.chat_message("ai").markdown(resposta.response)

# Função principal
def main():
    sidebar()

    tipo_arquivo = st.session_state.get("tipo_arquivo", "Tech")
    llm = configurar_llm()
    index = criar_indice(tipo_arquivo)

    pagina_chat(llm, index)

if __name__ == "__main__":
    main()
