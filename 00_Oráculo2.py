import streamlit as st
import requests
from bs4 import BeautifulSoup

TIPOS_ARQUIVOS_VALIDOS = [
    'Tech',
    'Social Media',
    'Gestor de Tráfego',
    'Account',
    'Vendas'
]

posi = {
    'Gestores de Projetos ou Accounts': 'Responsáveis pelo planejamento, execução e acompanhamento de projetos...',
    'Gestores de Tráfego': 'Focados em estratégias de mídia paga e orgânica...',
    'Analista de CRM': 'Especialista em gerenciar as relações com clientes...',
    # Outros cargos...
}

ARQUIVOS = {
    'Tech': ['https://vendas.v4company.com/glossario-marketing/'],
    'Social Media': ['https://vendas.v4company.com/glossario-marketing/'],
    'Gestor de Tráfego': ['https://vendas.v4company.com/glossario-marketing/'],
    'Account': ['https://vendas.v4company.com/glossario-marketing/'],
    'Vendas': ['https://vendas.v4company.com/glossario-marketing/'],
}

# Função para carregar conteúdo de URLs e extrair texto
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

# Função para criar uma resposta dinâmica baseada no contexto
def criar_resposta(pergunta, tipo_arquivo):
    arquivos = ARQUIVOS.get(tipo_arquivo, [])
    resposta_final = None

    # Verificar se a pergunta está no dicionário de cargos
    if pergunta in posi:
        return posi[pergunta], None

    # Procurar a resposta nos documentos carregados
    for url in arquivos:
        conteudo = carrega_site(url)
        if pergunta.lower() in conteudo.lower():  # Busca direta na página
            inicio = conteudo.lower().find(pergunta.lower())
            trecho_relevante = conteudo[inicio:inicio + 300]  # Trecho em torno da pergunta
            resposta_final = f"Baseado no documento, encontrei: {trecho_relevante}..."
            return resposta_final, url

    # Caso nenhuma resposta seja encontrada
    return "Não encontrei informações relevantes nos documentos. Revise as URLs fornecidas.", arquivos[0] if arquivos else None

# Exibir mensagens no chat
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

        # Gerar resposta
        tipo_arquivo = st.session_state.get("tipo_arquivo", "Tech")
        resposta, url = criar_resposta(pergunta, tipo_arquivo)

        # Construir resposta final com link, se disponível
        resposta_completa = f"{resposta}\n\n[Leia mais aqui]({url})" if url else resposta
        st.session_state["historico"].append({"autor": "ai", "conteudo": resposta_completa})
        st.chat_message("ai").markdown(resposta_completa)

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
    sidebar()
    pagina_chat()

if __name__ == "__main__":
    main()
