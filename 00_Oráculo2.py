import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader as web

from langchain_groq import ChatGroq

TIPOS_ARQUIVOS_VALIDOS = [
    'Tech',
    'Social Media',
    'Gestor de Tráfego',
    'Account',
    'Vendas'
]

CONFIG_MODELOS = {'Groq': 
                        {'modelos': 'llama-3.3-70b-versatile',
                         'chat': ChatGroq}
                         }

MEMORIA = ConversationBufferMemory()

def carrega_site(url):
    loader = web(url)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento


def carrega_arquivos(tipo_arquivo, arquivo):
        documento = carrega_site(arquivo)

def carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo):
    # Prompt corrigido com variáveis escapadas corretamente
    system_message = f'''Você é um assistente amigável chamado Oráculo que é utilizado pela empresa v4 ferraz piai & CO.
Você possui acesso às seguintes informações vindas 
de um documento: 

####
{arquivo}
####

Utilize as informações fornecidas para basear as suas respostas. Você não pode buscar informações fora dos documentos fornecidos e deve utilizar o contexto para responder.

1. **{{{{'Gestores de Projetos ou Accounts'}}}}:**  
   Responsáveis pelo planejamento, execução e acompanhamento de projetos. Atuam como ponto de contato entre a equipe interna e os clientes, garantindo que entregas sejam realizadas dentro do prazo e conforme as expectativas. Gerenciam recursos e cronogramas, e solucionam problemas para assegurar o sucesso dos projetos.

...
'''

    # Template atualizado
    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])

    chat = CONFIG_MODELOS[provedor]['chat'](model=modelo, api_key=api_key)
    chain = template | chat

    # Salva no estado da sessão
    st.session_state['chain'] = chain


def pagina_chat():
    st.markdown(f'<h2 style="text-align: center;">🤖Bem-vindo ao Oráculo</h2>', unsafe_allow_html=True)
    st.divider()

    # Verifica se a chain está inicializada
    chain = st.session_state.get('chain')
    if chain is None:
        st.error('Carregue o Oráculo')
        st.markdown(f'<h6 style="text-align: center;">Para evitar erros, envie uma mensagem como "olá" para inicializar a memória do chat.</h6>', unsafe_allow_html=True)
        st.stop()

    memoria = st.session_state.get('memoria', MEMORIA)

    # Exibe mensagens do histórico
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    # Entrada do usuário
    input_usuario = st.chat_input('Fale com o oráculo')
    if input_usuario:
        # Exibe mensagem do usuário
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        # Processa resposta do modelo
        try:
            chat = st.chat_message('ai')
            resposta = chain.invoke({'input': input_usuario, 'chat_history': memoria.buffer_as_messages})
            chat.markdown(resposta)
            
            # Atualiza memória
            memoria.chat_memory.add_user_message(input_usuario)
            memoria.chat_memory.add_ai_message(resposta)
            st.session_state['memoria'] = memoria
        except KeyError as e:
            st.error(f"Erro no processamento: {str(e)}")
        except Exception as e:
            st.error(f"Erro inesperado: {str(e)}")


def main():
    with st.sidebar:
        sidebar()
    pagina_chat()


if __name__ == '__main__':
    main()
