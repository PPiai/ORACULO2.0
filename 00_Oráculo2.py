import streamlit as st
import requests

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

# Função para carregar documentos diretamente via requests
def carrega_site(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Erro ao carregar o site: {response.status_code}"
    except Exception as e:
        return f"Erro ao conectar: {e}"

# Função para criar resposta baseada no contexto
def criar_resposta(pergunta, tipo_arquivo):
    # Buscar URLs relacionadas ao tipo de arquivo
    arquivos = ARQUIVOS.get(tipo_arquivo, [])
    contexto = [carrega_site(url) for url in arquivos]
    
    # Verificar se a pergunta é sobre cargos
    if pergunta in posi:
        resposta = f"{posi[pergunta]}"
    else:
        resposta = f"Baseado no documento, não encontrei informações diretas. Por favor, revise as URLs:\n" \
                   f"{', '.join(arquivos)}"
    return resposta, arquivos[0] if arquivos else None

# Exibir mensagens de chat
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
        # Registrar mensagem do usuário
        st.session_state["historico"].append({"autor": "human", "conteudo": pergunta})
        st.chat_message("human").markdown(pergunta)
        
        # Gerar resposta
        tipo_arquivo = st.session_state.get("tipo_arquivo", "Tech")
        resposta, url = criar_resposta(pergunta, tipo_arquivo)
        
        # Registrar resposta da IA
        resposta_completa = f"{resposta}\n\n[Leia mais aqui]({url})" if url else resposta
        st.session_state["historico"].append({"autor": "ai", "conteudo": resposta_completa})
        st.chat_message("ai").markdown(resposta_completa)

# Sidebar de configuração
def sidebar():
    st.sidebar.title("Configuração")
    tipo_arquivo = st.sidebar.selectbox("Selecione sua Área", TIPOS_ARQUIVOS_VALIDOS)
    st.session_state["tipo_arquivo"] = tipo_arquivo
    
    if st.sidebar.button("Apagar Histórico"):
        st.session_state["historico"] = []

# Executar aplicativo principal
def main():
    sidebar()
    pagina_chat()

if __name__ == "__main__":
    main()
