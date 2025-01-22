import streamlit as st
import requests

TIPOS_ARQUIVOS_VALIDOS = [
    'Tech',
    'Social Media',
    'Gestor de Tráfego',
    'Account',
    'Vendas'
]

posi = {'Gestores de Projetos ou Accounts' : 'Responsáveis pelo planejamento, execução e acompanhamento de projetos. Atuam como ponto de contato entre a equipe interna e os clientes, garantindo que entregas sejam realizadas dentro do prazo e conforme as expectativas. Gerenciam recursos e cronogramas, e solucionam problemas para assegurar o sucesso dos projetos.',
    'Gestores de Tráfego' : 'Focados em estratégias de mídia paga e orgânica, eles gerenciam campanhas publicitárias em plataformas como Google Ads, Facebook Ads, e outros canais de mídia. Trabalham para aumentar o tráfego qualificado e otimizar o ROI (Retorno sobre Investimento).',
    'Analista de CRM' : 'Especialista em gerenciar as relações com clientes por meio de sistemas de CRM (Customer Relationship Management). É responsável por segmentar públicos, planejar campanhas e otimizar a jornada do cliente para aumentar retenção e engajamento.',
    'Designers' : 'Criam materiais visuais, como peças gráficas, layouts de sites, posts para redes sociais e outros ativos visuais. Trabalham para garantir que a comunicação visual esteja alinhada com a identidade da marca e os objetivos estratégicos.',
    'Copywriters' : 'Especialistas em redação persuasiva. Criam textos para anúncios, e-mails, páginas de vendas, blogs e outros materiais, com foco em atrair, engajar e converter leads.',
    'Analista de UX/UI' : 'Responsável pela experiência do usuário (UX) e design de interface do usuário (UI). Conduz pesquisas, testes e análises para garantir que produtos digitais sejam funcionais, intuitivos e esteticamente agradáveis.',
    'Analista de Site' : 'Cuida da manutenção, performance e otimização de sites. Garante que o site esteja funcional, seguro e rápido, além de implementar melhorias baseadas em dados de análise de desempenho.',
    'Head' : 'Gestor da vertente ou da equipe, responsável por liderar e gerenciar o time. Define estratégias, alinha metas, supervisiona as entregas e garante que os objetivos da equipe estejam alinhados com os objetivos gerais da empresa. Atua como um elo entre a alta gestão e os membros do time.',
    'CAP' : 'Profissional que auxilia a vertente ou o time, proporcionando suporte estratégico e operacional. Trabalha em conjunto com o Head e a equipe para garantir a execução eficiente das tarefas, contribuindo com insights e ações práticas para o sucesso do grupo',
    'Analista de Growth' : 'Focado em identificar oportunidades de crescimento para o negócio. Trabalha com experimentos, otimizações e estratégias de aquisição e retenção de clientes para impulsionar resultados.',
    'Closers' : 'Especialistas em vendas, responsáveis por finalizar negociações e converter leads em clientes. Possuem alta capacidade de persuasão e foco em alcançar metas comerciais.',
    'BDR (Business Development Representative)' : 'Profissionais focados em prospectar e qualificar leads para a equipe de vendas. Trabalham na geração de oportunidades e no fortalecimento de relacionamentos comerciais.',
    'Financeiro' : 'Gerencia os recursos financeiros da empresa. Cuida do fluxo de caixa, orçamentos, pagamento de contas, faturamento e planejamento financeiro.',
    'People & Performance' : 'Área responsável por cuidar das pessoas da empresa. Atua em recrutamento, treinamento, desenvolvimento de colaboradores e gestão de desempenho, promovendo um ambiente de trabalho saudável e produtivo.',
    'Analista de BI (Business Intelligence)' : 'Responsável por coletar, organizar e analisar dados para fornecer insights estratégicos que apoiem a tomada de decisão. Cria dashboards, relatórios e análises que ajudam a empresa a identificar tendências, medir resultados e otimizar processos. Trabalha em estreita colaboração com outros times para garantir que os dados sejam utilizados de forma eficaz para atingir os objetivos da empresa.'
}

MEMORIA = []

# URLs de exemplo para as áreas
ARQUIVOS = {
    'Tech': ['https://vendas.v4company.com/glossario-marketing/', 'https://heyzine.com/flip-book/87da189f45.html'],
    'Social Media': ['https://vendas.v4company.com/glossario-marketing/', 'https://v4company.com/marketing-digital/como-criar-criativos-que-convertem'],
    'Gestor de Tráfego': ['https://vendas.v4company.com/glossario-marketing/', 'https://heyzine.com/flip-book/87da189f45.html'],
    'Account': ['https://vendas.v4company.com/glossario-marketing/', 'https://heyzine.com/flip-book/87da189f45.html'],
    'Vendas': ['https://vendas.v4company.com/glossario-marketing/', 'https://heyzine.com/flip-book/87da189f45.html'],
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

# Função para carregar modelo e configurar a API
def carrega_modelo(api_key, tipo_arquivo, arquivos):
    context = "\n".join([carrega_site(url) for url in arquivos])
    system_message = f"""
    Você é um assistente chamado Oráculo, utilizado pela empresa V4 Ferraz Piai & CO.
    Suas informações vêm das seguintes fontes:\n{context}\n
    Use-as para responder com precisão.
    """
    st.session_state['context'] = system_message
    st.session_state['api_key'] = api_key

def pagina_chat():
    st.title("🤖 Bem-vindo ao Oráculo")
    st.divider()

    # Inicializar contexto
    context = st.session_state.get('context', None)
    if context is None:
        st.error("Carregue o Oráculo antes de iniciar.")
        st.stop()

    # Exibição do histórico de mensagens
    for mensagem in MEMORIA:
        st.chat_message(mensagem['autor']).markdown(mensagem['conteudo'])

    # Entrada de usuário
    input_usuario = st.chat_input("Fale com o Oráculo")
    if input_usuario:
        MEMORIA.append({'autor': 'human', 'conteudo': input_usuario})
        st.chat_message("human").markdown(input_usuario)

        # Simulação de resposta (substitua com chamada real à API do Groq)
        resposta = f"Você perguntou: {input_usuario}. (Simulação baseada no contexto fornecido.)"
        MEMORIA.append({'autor': 'ai', 'conteudo': resposta})
        st.chat_message("ai").markdown(resposta)

def sidebar():
    st.sidebar.title("Configuração")
    tipo_arquivo = st.sidebar.selectbox("Selecione sua Área", TIPOS_ARQUIVOS_VALIDOS)
    arquivos = ARQUIVOS.get(tipo_arquivo, [])
    api_key = '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'

    if st.sidebar.button("Inicializar Oráculo"):
        carrega_modelo(api_key, tipo_arquivo, arquivos)
    if st.sidebar.button("Apagar Histórico"):
        MEMORIA.clear()

def main():
    sidebar()
    pagina_chat()

if __name__ == "__main__":
    main()
