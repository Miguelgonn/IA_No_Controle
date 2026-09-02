import json
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Caminhos dos arquivos usados pelo sistema
# ---------------------------------------------------------------------------

PASTA_DADOS = os.path.dirname(os.path.abspath(__file__))

ARQ_MODULOS = os.path.join(PASTA_DADOS, "modulos_colonia.json")
ARQ_ALERTAS = os.path.join(PASTA_DADOS, "alertas.json")
ARQ_SOLICITACOES = os.path.join(PASTA_DADOS, "solicitacoes_tripulacao.json")
ARQ_INTERACOES = os.path.join(PASTA_DADOS, "interacoes.json")
ARQ_MANUTENCAO = os.path.join(PASTA_DADOS, "registros_manutencao.txt")
ARQ_LOGS_ACESSO = os.path.join(PASTA_DADOS, "logs_acesso.txt")


# ---------------------------------------------------------------------------
# 1. FUNÇÕES GENÉRICAS DE MANIPULAÇÃO DE ARQUIVOS
# ---------------------------------------------------------------------------

def gravar_registro_texto(caminho, conteudo):
    """Grava (sobrescreve) um conteúdo em um arquivo de texto."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)


def ler_registro_texto(caminho):
    """Lê e retorna todo o conteúdo de um arquivo de texto."""
    if not os.path.exists(caminho):
        return ""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def adicionar_registro_texto(caminho, linha):
    """Adiciona uma nova linha ao final de um arquivo de texto (modo append)."""
    with open(caminho, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha.rstrip("\n") + "\n")


def exibir_dados(dados, titulo="Dados"):
    """Exibe dados (texto ou estrutura JSON) formatados na tela."""
    print(f"\n===== {titulo} =====")
    if isinstance(dados, (dict, list)):
        print(json.dumps(dados, ensure_ascii=False, indent=2))
    else:
        print(dados)
    print("=" * (len(titulo) + 12))


def carregar_json(caminho):
    """Carrega e retorna a estrutura (dict ou list) de um arquivo JSON."""
    if not os.path.exists(caminho):
        return {}
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_json(caminho, dados):
    """Salva um dicionário ou lista de dicionários em um arquivo JSON."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# 2. FUNÇÕES ESPECÍFICAS DO PROJETO (usam as funções genéricas acima)
# ---------------------------------------------------------------------------

def _agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# --- Registros de manutenção (TXT) -----------------------------------------

def registrar_manutencao(modulo, descricao):
    """Adiciona uma nova ocorrência técnica ao log de manutenção (texto)."""
    data = datetime.now().strftime("%Y-%m-%d")
    linha = f"[{data}] {modulo} - {descricao}"
    adicionar_registro_texto(ARQ_MANUTENCAO, linha)
    registrar_log_acesso("Sistema", "registro_manutencao", modulo)
    print("Registro de manutenção adicionado com sucesso.")


def exibir_manutencao():
    conteudo = ler_registro_texto(ARQ_MANUTENCAO)
    exibir_dados(conteudo, "Registros de Manutenção")


# --- Logs de acesso (TXT) ---------------------------------------------------

def registrar_log_acesso(usuario, acao, referencia=""):
    """Adiciona uma nova entrada ao log de acesso do sistema (texto)."""
    linha = f"[{_agora()}] Usuário: {usuario} | Ação: {acao} | Referência: {referencia}"
    adicionar_registro_texto(ARQ_LOGS_ACESSO, linha)


def exibir_logs_acesso():
    conteudo = ler_registro_texto(ARQ_LOGS_ACESSO)
    exibir_dados(conteudo, "Logs de Acesso")


# --- Status de módulos (JSON) ----------------------------------------------

def exibir_modulos():
    dados = carregar_json(ARQ_MODULOS)
    exibir_dados(dados, "Status dos Módulos")


def atualizar_status_modulo(id_modulo, novo_status):
    """Atualiza o campo 'status' de um módulo específico e salva o JSON."""
    dados = carregar_json(ARQ_MODULOS)
    encontrado = False
    for modulo in dados.get("modulos", []):
        if modulo["id"] == id_modulo:
            modulo["status"] = novo_status
            encontrado = True
            break
    if encontrado:
        salvar_json(ARQ_MODULOS, dados)
        registrar_log_acesso("Sistema", "atualizacao_status_modulo", id_modulo)
        print(f"Status do módulo {id_modulo} atualizado para '{novo_status}'.")
    else:
        print(f"Módulo {id_modulo} não encontrado.")


# --- Alertas operacionais (JSON) -------------------------------------------

def registrar_alerta(modulo, tipo_ocorrencia, prioridade, mensagem):
    """Cria um novo alerta operacional e salva no arquivo JSON."""
    dados = carregar_json(ARQ_ALERTAS)
    if "alertas" not in dados:
        dados["alertas"] = []

    novo_id = f"ALT-{len(dados['alertas']) + 1:03d}"
    novo_alerta = {
        "id": novo_id,
        "modulo": modulo,
        "tipo_ocorrencia": tipo_ocorrencia,
        "prioridade": prioridade,
        "data_registro": datetime.now().strftime("%Y-%m-%d"),
        "mensagem": mensagem,
    }
    dados["alertas"].append(novo_alerta)
    salvar_json(ARQ_ALERTAS, dados)
    registrar_log_acesso("Sistema", "novo_alerta", novo_id)
    print(f"Alerta {novo_id} registrado com sucesso.")


def exibir_alertas():
    dados = carregar_json(ARQ_ALERTAS)
    exibir_dados(dados, "Alertas Operacionais")


# --- Solicitações da tripulação (JSON) --------------------------------------

def registrar_solicitacao(tripulante, modulo_relacionado, tipo_solicitacao, descricao):
    dados = carregar_json(ARQ_SOLICITACOES)
    if "solicitacoes" not in dados:
        dados["solicitacoes"] = []

    novo_id = f"SOL-{len(dados['solicitacoes']) + 1:03d}"
    nova_solicitacao = {
        "id": novo_id,
        "tripulante": tripulante,
        "modulo_relacionado": modulo_relacionado,
        "tipo_solicitacao": tipo_solicitacao,
        "descricao": descricao,
        "status": "pendente",
        "data_solicitacao": datetime.now().strftime("%Y-%m-%d"),
    }
    dados["solicitacoes"].append(nova_solicitacao)
    salvar_json(ARQ_SOLICITACOES, dados)
    registrar_log_acesso(tripulante, "nova_solicitacao", novo_id)
    print(f"Solicitação {novo_id} registrada com sucesso.")


def exibir_solicitacoes():
    dados = carregar_json(ARQ_SOLICITACOES)
    exibir_dados(dados, "Solicitações da Tripulação")


# --- Histórico de respostas do assistente (JSON) ----------------------------

def registrar_interacao(tripulante, pergunta, resposta):
    """Salva uma pergunta e a resposta simulada do assistente no histórico."""
    dados = carregar_json(ARQ_INTERACOES)
    if "interacoes" not in dados:
        dados["interacoes"] = []

    novo_id = f"INT-{len(dados['interacoes']) + 1:03d}"
    nova_interacao = {
        "id": novo_id,
        "tripulante": tripulante,
        "pergunta": pergunta,
        "resposta": resposta,
        "data_hora": _agora(),
    }
    dados["interacoes"].append(nova_interacao)
    salvar_json(ARQ_INTERACOES, dados)
    registrar_log_acesso(tripulante, "interacao_assistente", novo_id)
    print(f"Interação {novo_id} registrada com sucesso.")


def exibir_interacoes():
    dados = carregar_json(ARQ_INTERACOES)
    exibir_dados(dados, "Histórico de Interações")


def gerar_resposta_simulada(pergunta):
    """
    Simula a resposta do assistente cognitivo com base em palavras-chave
    encontradas na pergunta e nos dados atuais dos módulos/alertas.
    (Versão simplificada, sem uso de IA real, apenas para fins didáticos.)
    """
    pergunta_lower = pergunta.lower()
    modulos = carregar_json(ARQ_MODULOS).get("modulos", [])
    alertas = carregar_json(ARQ_ALERTAS).get("alertas", [])

    for modulo in modulos:
        if modulo["nome"].lower() in pergunta_lower:
            return (
                f"O módulo {modulo['nome']} está com status "
                f"'{modulo['status']}'. Última manutenção em {modulo['ultima_manutencao']}."
            )

    if "alerta" in pergunta_lower:
        if alertas:
            ultimo = alertas[-1]
            return (
                f"O alerta mais recente é {ultimo['id']} ({ultimo['prioridade']}) "
                f"no módulo {ultimo['modulo']}: {ultimo['mensagem']}"
            )
        return "Não há alertas registrados no momento."

    return "Não foi possível interpretar a solicitação. Poderia reformular a pergunta?"


# ---------------------------------------------------------------------------
# 3. MENU INTERATIVO
# ---------------------------------------------------------------------------

def menu():
    opcoes = """
    ============================================
     NÚCLEO COGNITIVO - AURORA SIGER
    ============================================
     1  - Ver status dos módulos
     2  - Atualizar status de um módulo
     3  - Ver alertas operacionais
     4  - Registrar novo alerta
     5  - Ver solicitações da tripulação
     6  - Registrar nova solicitação
     7  - Ver histórico de interações
     8  - Fazer uma pergunta ao assistente
     9  - Ver registros de manutenção
    10  - Registrar nova manutenção
    11  - Ver logs de acesso
     0  - Sair
    ============================================
    """
    while True:
        print(opcoes)
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            exibir_modulos()
        elif escolha == "2":
            id_modulo = input("ID do módulo (ex: MOD-01): ").strip()
            novo_status = input("Novo status: ").strip()
            atualizar_status_modulo(id_modulo, novo_status)
        elif escolha == "3":
            exibir_alertas()
        elif escolha == "4":
            modulo = input("Módulo: ").strip()
            tipo = input("Tipo de ocorrência: ").strip()
            prioridade = input("Prioridade (baixa/media/alta): ").strip()
            mensagem = input("Mensagem: ").strip()
            registrar_alerta(modulo, tipo, prioridade, mensagem)
        elif escolha == "5":
            exibir_solicitacoes()
        elif escolha == "6":
            tripulante = input("Nome do tripulante: ").strip()
            modulo = input("Módulo relacionado: ").strip()
            tipo = input("Tipo de solicitação: ").strip()
            descricao = input("Descrição: ").strip()
            registrar_solicitacao(tripulante, modulo, tipo, descricao)
        elif escolha == "7":
            exibir_interacoes()
        elif escolha == "8":
            tripulante = input("Nome do tripulante: ").strip()
            pergunta = input("Pergunta: ").strip()
            resposta = gerar_resposta_simulada(pergunta)
            print(f"\nAssistente: {resposta}\n")
            registrar_interacao(tripulante, pergunta, resposta)
        elif escolha == "9":
            exibir_manutencao()
        elif escolha == "10":
            modulo = input("Módulo: ").strip()
            descricao = input("Descrição da ocorrência: ").strip()
            registrar_manutencao(modulo, descricao)
        elif escolha == "11":
            exibir_logs_acesso()
        elif escolha == "0":
            print("Encerrando o Núcleo Cognitivo. Até a próxima, tripulante.")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
