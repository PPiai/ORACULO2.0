import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import requests
from bs4 import BeautifulSoup

# Configuração do pipeline do modelo Hugging Face
@st.cache_resource
def carregar_pipeline():
    modelo = "gpt2"  # Substitua por "flan-t5-base" para respostas mais específicas
    tokenizer = AutoTokenizer.from_pretrained(modelo)
    modelo_transformers = AutoModelForCausalLM.from_pretrained(modelo)
    return pipeline("text-generation", model=modelo_transformers, tokenizer=tokenizer, max_length=500)

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

# Função para carregar conteúdo das URLs e extrair texto
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

# Função para criar uma resposta dinâmica baseada no modelo Hugging Face
def criar_resposta(pergunta, tipo_arquivo, pipeline_ia):
    # Carregar os documentos relacionados ao tipo de arquivo selecionado
    arquivos = ARQUIVOS.get(tipo_arquivo, [])
    contexto = ""
    for url in arquivos:
        contexto += carrega_site(url) + "\n\n"

    # Criar o prompt para o modelo
    prompt = f"Contexto: {contexto}\n\nPergunta: {pergunta}\n\nResposta:"
    
    # Gerar resposta usando o pipeline Hugging Face
    resposta = pipeline_ia(prompt)[0]["generated_text"]
    return resposta

# Exibir mensagens no chat
def pagina_chat(pipeline_ia):
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

        # Gerar resposta
        tipo_arquivo = st.session_state.get("tipo_arquivo", "Tech")
        resposta = criar_resposta(pergunta, tipo_arquivo, pipeline_ia)

        # Construir resposta final
        st.session_state["historico"].append({"autor": "ai", "conteudo": resposta})
        st.chat_message("ai").markdown(resposta)

# Configuração da barra lateral
def sidebar():
    st.sidebar.title("Configuração")
    
    # Seleção da base de conhecimento
    tipo_arquivo = st.sidebar.selectbox("Selecione sua Área", TIPOS_ARQUIVOS_VALIDOS)
    st.session_state["tipo_arquivo"] = tipo_arquivo

    # Botão para apagar histórico
    if st.sidebar.button("Apagar Histórico"):
        st.session_state["historico"] = []

# Executar aplicativo principal
def main():
    pipeline_ia = carregar_pipeline()
    sidebar()
    pagina_chat(pipeline_ia)

if __name__ == "__main__":
    main()
