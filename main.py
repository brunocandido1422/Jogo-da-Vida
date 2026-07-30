import os
import random
import asyncio
from nicegui import ui, app

# ==========================================
# 📁 CONFIGURAÇÃO DE PASTAS E ROTAS
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
app.add_static_files('/assets', ASSETS_DIR)

# ==========================================
# 🧠 DADOS E REGRAS DO JOGO
# ==========================================
TOTAL_CASAS = 40
SALDO_INICIAL = 1621
PREMIOS_CHEGADA = [30000, 20000, 15000, 10000]

CORES_CASAS = ["#E53935", "#8E24AA", "#1E88E5", "#00897B", "#F4511E", "#6D4C41", "#039BE5", "#43A047", "#FB8C00",
               "#3949AB"]
CORES_EQUIPES = ["#E53935", "#1E88E5", "#43A047", "#FB8C00", "#8E24AA", "#00897B", "#F4511E", "#3949AB"]

DILEMAS_FIXOS = {
    1: {"titulo": "A mesada", "cenario": "Você recebeu sua mesada do mês. O que você faz?",
        "opcoes": [{"texto": "👗 Gasto tudo com roupas novas", "saldo": -150.00},
                   {"texto": "🍿 Uso metade com lazer e guardo o restante", "saldo": -75.00},
                   {"texto": "📚 Compro um livro novo", "saldo": -80.00},
                   {"texto": "🐷 Guardo tudo para o futuro", "saldo": 150.00}]},
    2: {"titulo": "Material escolar",
        "cenario": "Início do ano chegou e com ele o momento de comprar cadernos. O que fazer?",
        "opcoes": [{"texto": "📓 Compro cadernos que são lançamentos", "saldo": -80.00},
                   {"texto": "📓 Compro cadernos em promoção", "saldo": -30.00}]},
    3: {"titulo": "Hora do lanche", "cenario": "Bateu uma fome na escola! Que tal um lanchinho entre as aulas?",
        "opcoes": [{"texto": "🍔 Compro um lanche na escola", "saldo": -20.00},
                   {"texto": "🤝 Compro um lanche dividido com um amigo", "saldo": -10.00},
                   {"texto": "🥪 Faço lanche em casa e levo para a escola", "saldo": -8.00},
                   {"texto": "🚫 Não lancho e fico com fome", "saldo": 0.00}]},
    6: {"titulo": "Passeio escolar",
        "cenario": "A escola organizou uma viagem para uma cidade histórica. O que você faz?",
        "opcoes": [{"texto": "🚌 Pago e viajo", "saldo": -150.00}, {"texto": "🏠 Fico em casa", "saldo": 0.00}]},
    7: {"titulo": "O tênis da moda", "cenario": "Teve o lançamento de um tênis desejado.",
        "opcoes": [{"texto": "👟 Compro agora", "saldo": -500.00},
                   {"texto": "🏷️ Espero entrar em promoção", "saldo": -350.00},
                   {"texto": "🥾 Compro um tênis mais barato", "saldo": -250.00},
                   {"texto": "👟 Uso o que tenho e economizo", "saldo": 0.00}]},
    8: {"titulo": "Roupa para festa", "cenario": "Uma festa do colegial está chegando.",
        "opcoes": [{"texto": "👗 Compro roupas novas", "saldo": -200.00},
                   {"texto": "👕 Uso as roupas que já tenho", "saldo": 0.00}]},
    9: {"titulo": "Cinema no final de semana", "cenario": "A turma toda vai ao cinema ver o filme indicado ao Oscar.",
        "opcoes": [{"texto": "🍿 Compro o ingresso, pipoca e refri", "saldo": -60.00},
                   {"texto": "🎟️ Compro somente o Ingresso", "saldo": -40.00},
                   {"texto": "🍔 Compro um lanche e não vou ao cinema", "saldo": -30.00},
                   {"texto": "🏠 Fico em casa", "saldo": 0.00}]},
    11: {"titulo": "Morar na república ou sozinho?",
         "cenario": "É hora de decidir onde morar durante o período da universidade.",
         "opcoes": [{"texto": "🏠 Vou morar em uma Kitnet sozinho", "saldo": -800.00},
                    {"texto": "👥 Vou dividir república", "saldo": -400.00},
                    {"texto": "😒 Vou alugar um quarto na casa de um tio desagradável", "saldo": -100.00},
                    {"texto": "🛏️ Vou morar em um alojamento", "saldo": 0.00}]},
    12: {"titulo": "Xerox ou original", "cenario": "O professor pediu um livro base importante para seu curso.",
         "opcoes": [{"texto": "📖 Compro o original", "saldo": -120.00},
                    {"texto": "📄 Tiro um xerox", "saldo": -15.00},
                    {"texto": "🧠 Não preciso ler, já tenho conhecimento", "saldo": 0.00},
                    {"texto": "📚 Leio na biblioteca", "saldo": 0.00}]},
    13: {"titulo": "Congresso acadêmico", "cenario": "Terá um evento importante em outra cidade.",
         "opcoes": [{"texto": "🌟 Pago a inscrição com área VIP e viajo", "saldo": -750.00},
                    {"texto": "✈️ Pago a inscrição e viajo", "saldo": -500.00},
                    {"texto": "💻 Faço a inscrição para o evento online", "saldo": -200.00},
                    {"texto": "🚫 Não participo", "saldo": 0.00}]},
    14: {"titulo": "Festa ou prova",
         "cenario": "Você sabe que se divertir é importante e surgiu uma festa badalada na véspera de prova.",
         "opcoes": [{"texto": "👗 Vou à festa e compro roupa nova", "saldo": -250.00},
                    {"texto": "🎉 Vou à festa", "saldo": -100.00},
                    {"texto": "🎶 Vou à uma festa menos famosa", "saldo": -50.00},
                    {"texto": "📚 Fico em casa estudando", "saldo": 0.00}]},
    16: {"titulo": "O notebook quebrou",
         "cenario": "Seu computador pifou na semana de entrega de trabalhos importantes.",
         "opcoes": [{"texto": "💻 Compro um novo", "saldo": -2000.00}, {"texto": "🛠️ Mando arrumar", "saldo": -500.00},
                    {"texto": "🖥️ Alugo um tempo na Lan house", "saldo": -100.00},
                    {"texto": "🤝 Pego emprestado com um amigo", "saldo": 0.00}]},
    17: {"titulo": "Atrasado para a aula", "cenario": "Está chovendo muito no horário da aula.",
         "opcoes": [{"texto": "🚕 Vou de carro por aplicativo", "saldo": -30.00},
                    {"texto": "🤝 Divido o aplicativo de carro com um amigo", "saldo": -15.00},
                    {"texto": "🚌 Vou de ônibus", "saldo": -5.00},
                    {"texto": "☔ Encaro a chuva e vou a pé", "saldo": 0.00}]},
    18: {"titulo": "Oportunidade de estágio", "cenario": "Aprendizado ou dinheiro rápido?",
         "opcoes": [{"texto": "💼 Prefiro fazer freelancers", "saldo": 750.00},
                    {"texto": "🎓 Aceito o estágio acadêmico", "saldo": 500.00}]},
    19: {"titulo": "Lançou a Nova Temporada", "cenario": "Lançamento da nova temporada da sua série favorita.",
         "opcoes": [{"texto": "📺 Assino e pago sozinho", "saldo": -40.00},
                    {"texto": "🤝 Divido com os amigos", "saldo": -10.00}]},
    22: {"titulo": "Casamento dos sonhos",
         "cenario": "Você achou o amor da sua vida e chegou a hora de casar! Como será a festa?",
         "opcoes": [{"texto": "🥂 Vou fazer uma festa de luxo", "saldo": -100000.00},
                    {"texto": "💒 Vou fazer uma festa simples", "saldo": -30000.00},
                    {"texto": "✈️ Acho melhor viajar e gastar menos", "saldo": -10000.00},
                    {"texto": "🚫 Prefiro não fazer festa nem viajar", "saldo": 0.00}]},
    23: {"titulo": "Reserva de emergência", "cenario": "Seu eletrodoméstico quebrou de repente.",
         "opcoes": [{"texto": "💳 Vou comprar outro novo", "saldo": -4000.00},
                    {"texto": "♻️ Vou comprar um usado", "saldo": -1800.00},
                    {"texto": "🛠️ Vou mandar consertar", "saldo": -800.00},
                    {"texto": "🚫 Fico um tempo sem", "saldo": 0.00}]},
    24: {"titulo": "O pet fofinho", "cenario": "Quero adotar um animal de estimação.",
         "opcoes": [{"texto": "🐩 Compro uma raça cara", "saldo": -1000.00},
                    {"texto": "🐕‍🦺 Adoto um caramelo", "saldo": -200.00},
                    {"texto": "🐟 Compro um peixe e um aquário", "saldo": -100.00},
                    {"texto": "🚫 Desisti. Dá muito trabalho.", "saldo": 0.00}]},
    26: {"titulo": "Saúde em dia", "cenario": "Você precisa se exercitar!",
         "opcoes": [{"texto": "🏋️ Vou fazer aulas com personal trainer", "saldo": -300.00},
                    {"texto": "💪 Vou fazer o Plano na Academia", "saldo": -200.00},
                    {"texto": "⚽ Vou começar a fazer aulas de algum esporte", "saldo": -150.00},
                    {"texto": "🏃 Prefiro caminhar e correr na rua", "saldo": 0.00}]},
    27: {"titulo": "Filhos!", "cenario": "A família cresceu! Preparativos para o bebê.",
         "opcoes": [{"texto": "🧸 Vou comprar berço novo", "saldo": -2000.00},
                    {"texto": "♻️ Vou comprar berço usado", "saldo": -1500.00}]},
    28: {"titulo": "Férias do trabalho", "cenario": "Chegou a hora de viajar com a família.",
         "opcoes": [{"texto": "✈️ Vou fazer uma viagem internacional", "saldo": -15000.00},
                    {"texto": "🏖️ Vou fazer uma viagem nacional", "saldo": -5000.00},
                    {"texto": "🚗 Vou viajar para uma cidade vizinha", "saldo": -2500.00},
                    {"texto": "🏠 Vou ficar na minha cidade e organizar algumas coisas", "saldo": 0.00}]},
    30: {"titulo": "O testamento",
         "cenario": "Aos 45 anos, você recebeu R$ 30.000 de herança de um parente. O que fazer?",
         "opcoes": [{"texto": "💰 Mantenho o dinheiro na conta corrente", "saldo": 30000.00},
                    {"texto": "🏦 Aplico tudo na Previdência", "aporte_unico": 30000.00}]},
    31: {"titulo": "Hobby novo", "cenario": "É hora de dedicar tempo para uma nova atividade de lazer.",
         "opcoes": [{"texto": "🧰 Compro o material novo", "saldo": -2000.00},
                    {"texto": "🤝 Convenço o amigo e dividir o material", "saldo": -1000.00},
                    {"texto": "♻️ Compro o material usado", "saldo": -800.00},
                    {"texto": "🤲 Pego o material emprestado para testar", "saldo": 0.00}]},
    32: {"titulo": "Ajuda à família", "cenario": "Seu filho pediu R$ 20.000 emprestados para abrir um negócio.",
         "opcoes": [{"texto": "💸 Empresto o valor total sem juros", "saldo": -20000.00},
                    {"texto": "📈 Empresto com juros para ganhar em cima", "saldo": 10000.00},
                    {"texto": "🤝 Ajudo com um valor menor", "saldo": -10000.00},
                    {"texto": "🚫 Não ajudo no momento", "saldo": 0.00}]},
    33: {"titulo": "Viagem dos amigos", "cenario": "Você e seus amigos estão pensando em viajar.",
         "opcoes": [{"texto": "🚢 Vou no cruzeiro de luxo", "saldo": -30000.00},
                    {"texto": "🏖️ Alugo uma casa na praia", "saldo": -15000.00},
                    {"texto": "♨️ Vou para uma excursão de águas termais", "saldo": -10000.00},
                    {"texto": "🏠 Prefiro ficar em casa", "saldo": 0.00}]},
    36: {"titulo": "Presente para os netos", "cenario": "Compra do presente perfeito de natal.",
         "opcoes": [{"texto": "🎁 Compro o melhor videogame", "saldo": -3000.00},
                    {"texto": "🎮 Compro um modelo mais simples", "saldo": -1000.00},
                    {"texto": "🧩 Dou um presente alternativo", "saldo": -500.00},
                    {"texto": "🍫 Compro uma caixa de bombom", "saldo": -30.00}]},
    37: {"titulo": "Dores da idade", "cenario": "Check-up devido a um desconforto físico.",
         "opcoes": [{"texto": "🏥 Vou a um médico particular", "saldo": -400.00},
                    {"texto": "🩺 Vou ao médico do meu plano", "saldo": -100.00},
                    {"texto": "💊 Compro os remédios por minha conta", "saldo": -500.00},
                    {"texto": "⏳ Espero passar e não me cuido", "saldo": 0.00}]},
    38: {"titulo": "Emergência Médica", "cenario": "Um mal-estar súbito te levou direto para a emergência.",
         "opcoes": [{"texto": "🏥 Pago particular", "saldo": -20000.00},
                    {"texto": "🏛️ Utilizo o sistema público de saúde", "saldo": 0.00}]},
    39: {"titulo": "O Refúgio da Família", "cenario": "Você quer um lugar especial para se reunir com sua família.",
         "opcoes": [{"texto": "🏡 Alugo uma casa espaçosa na praia", "saldo": -10000.00},
                    {"texto": "🌳 Alugo uma casa aconchegante na montanha", "saldo": -8000.00}]}
}

EVENTOS_FIXOS = {
    4: {"titulo": "Notas boas",
        "cenario": "Seus pais te deram dinheiro porque você tem tirado notas boas na escola. Parabéns!",
        "saldo": 200.00},
    5: {"titulo": "Mesada inesperada",
        "cenario": "Sua avó resolveu te dar uma mesada até você se formar na faculdade. (Ganha +R$ 200/rodada)",
        "saldo": 0.00, "flag_mesada": True, "emoji": "👵"},
    10: {"titulo": "Aniversário", "cenario": "Você deu uma festa e gastou mais que devia.", "saldo": -600.00},
    15: {"titulo": "Acidente de percurso", "cenario": "Você se acidentou e precisou de remédios.", "saldo": -200.00},
    20: {"titulo": "Trabalho extra", "cenario": "Freelance no fim de semana.", "saldo": 500.00},
    21: {"titulo": "Promoção no trabalho", "cenario": "PARABÉNS! Você recebeu uma promoção e seu salário será dobrado!",
         "saldo": 0.00, "flag_promocao": True},
    25: {"titulo": "Problema mecânico", "cenario": "Que azar! Seu carro ferveu e estragou.", "saldo": -5000.00},
    29: {"titulo": "Hora de Pagar o Imposto de Renda", "cenario": "Hora de acertar as contas com a Receita Federal!",
         "saldo": 0.00, "regra_ir": True},
    34: {"titulo": "Reforma da casa", "cenario": "Sua casa precisa de adaptação.", "saldo": -25000.00},
    35: {"titulo": "Dores da idade", "cenario": "Despesas com fisioterapia e itens ortopédicos.", "saldo": -2000.00}
}


# ==========================================
# 🛡️ PROXY DE SESSÃO (Isolamento 100% por Aba/Link)
# ==========================================
_games_state = {}
_ui_refs_state = {}

class SessionStateProxy:
    def _get_dict(self):
        # Identifica a aba/sessão exata que está fazendo a requisição
        client = ui.context.client
        if client.id not in _games_state:
            _games_state[client.id] = {
                "equipes_nomes": [], "ordem_final": [], "modo_turbo": False,
                "tela_atual": "menu", "equipes": [], "turno_atual": 0,
                "aguardando": False, "passos_atuais": 0, "fila_eventos": [],
                "formados": [], "jogo_finalizado": False, "ranking": [], "ranking_view_idx": 0
            }
            # Evita sobrecarga de memória no Render apagando os dados se a aba for fechada
            client.on_disconnect(lambda: _games_state.pop(client.id, None))
        return _games_state[client.id]

    def __getitem__(self, key): return self._get_dict()[key]
    def __setitem__(self, key, value): self._get_dict()[key] = value
    def get(self, key, default=None): return self._get_dict().get(key, default)
    def update(self, mapping): self._get_dict().update(mapping)
    def __contains__(self, key): return key in self._get_dict()

class UIRefsProxy:
    def _get_dict(self):
        client = ui.context.client
        if client.id not in _ui_refs_state:
            _ui_refs_state[client.id] = {}
            client.on_disconnect(lambda: _ui_refs_state.pop(client.id, None))
        return _ui_refs_state[client.id]

    def __getitem__(self, key): return self._get_dict()[key]
    def __setitem__(self, key, value): self._get_dict()[key] = value
    def get(self, key, default=None): return self._get_dict().get(key, default)
    def __contains__(self, key): return key in self._get_dict()

estado_jogo = SessionStateProxy()
ui_refs = UIRefsProxy()

# ==========================================
# 🧮 FUNÇÕES AUXILIARES MATEMÁTICAS E LÓGICAS
# ==========================================
def fmt_saldo(v):
    sinal = "-" if v < 0 else ""
    return f"{sinal}R$ {int(abs(v)):,}".replace(",", ".") + ",00"

def agrupar_emojis(emoji_str):
    if not emoji_str: return ""
    conhecidos = ["🏦", "📚", "📈", "💼", "🎓", "👵", "🌾", "🧬", "💻", "🎭"]
    res = []
    for e in conhecidos:
        qtd = emoji_str.count(e)
        if qtd == 1:
            res.append(e)
        elif qtd > 1:
            res.append(f"{qtd}x{e}")
    return " ".join(res)

def agrupar_emojis_html(emoji_str, font_size="14px"):
    if not emoji_str: return ""
    conhecidos = ["🏦", "📚", "📈", "💼", "🎓", "👵", "🌾", "🧬", "💻", "🎭"]
    res = []
    for e in conhecidos:
        qtd = emoji_str.count(e)
        if qtd == 1:
            res.append(e)
        elif qtd > 1:
            res.append(f"<span style='font-size: {font_size}; color: #757575;'>{qtd}x</span>{e}")
    return " ".join(res)


def cor_da_casa(num):
    if num == 1: return "#FFD700"
    if num == TOTAL_CASAS: return "#FF4500"
    if num in [3, 13, 20, 24, 30]: return "#1A237E"
    if num % 5 == 0: return "#00BCD4"
    return CORES_CASAS[(num - 1) % len(CORES_CASAS)]


def obter_texto_casa(num):
    texto = str(num)
    if num % 5 == 0 and num != TOTAL_CASAS: texto = f"★\n{num}"
    if num == 10: texto = f"🎓\n{num}"
    if num == 20: texto = f"💼\n{num}"
    if num in [3, 13, 24, 30]: texto = f"❕\n{num}"
    return texto


def calcular_coordenadas_tabuleiro():
    coords = [(0, 0)]
    r, c = 0, 0
    padrao = ['R'] * 9 + ['D'] * 2 + ['L'] * 9 + ['D'] * 2
    seq = padrao * 10
    for i in range(TOTAL_CASAS - 1):
        p = seq[i]
        if p == 'R':
            c += 1
        elif p == 'L':
            c -= 1
        elif p == 'D':
            r += 1
        coords.append((c, r))
    return coords


COORDENADAS = calcular_coordenadas_tabuleiro()
MAX_C = max(c for c, r in COORDENADAS)
MAX_R = max(r for c, r in COORDENADAS)


def obter_pos_pct(num):
    idx = num - 1
    if idx < 0 or idx >= len(COORDENADAS): return 50, 50
    c, r = COORDENADAS[idx]
    x_pct = 8 + (c / MAX_C) * 84
    y_pct = 10 + (r / MAX_R) * 75
    return x_pct, y_pct


def calcular_idade_exata(pos):
    """Calcula a idade de forma proporcional baseada nos marcos de vida."""
    if pos <= 3:
        return 16
    elif pos <= 10:
        return int(16 + (pos - 3) * (2 / 7))
    elif pos <= 13:
        return int(18 + (pos - 10) * (2 / 3))
    elif pos <= 20:
        return int(20 + (pos - 13) * (4 / 7))
    elif pos <= 24:
        return int(24 + (pos - 20) * (6 / 4))
    elif pos <= 30:
        return int(30 + (pos - 24) * (15 / 6))
    elif pos <= 40:
        return int(45 + (pos - 30) * 2)
    return 65


def gerar_svg_caminho():
    pts = [obter_pos_pct(i + 1) for i in range(TOTAL_CASAS)]
    layer1, layer2, layer3 = "", "", ""
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        layer1 += f'<line x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%" stroke="#BCAAA4" stroke-width="46" stroke-linecap="round" />\n'
        layer2 += f'<line x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%" stroke="#FFF3E0" stroke-width="38" stroke-linecap="round" />\n'
        layer3 += f'<line x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%" stroke="#FFCC80" stroke-width="4" stroke-dasharray="8,8" stroke-linecap="round" />\n'
    return f'<svg width="100%" height="100%" style="position: absolute; top: 0; left: 0; pointer-events: none; z-index: 1;">{layer1}{layer2}{layer3}</svg>'


def gerar_card_marco(marco, eq):
    invest_atual = eq.get("investimento_turno", 0)

    if marco == 3:
        return {
            "titulo": "DECISÃO PARA O FUTURO",
            "cenario": "Você está com 16 anos e o tempo está passando rápido. Você já pode fazer sua Previdência Complementar e também focar no seu conhecimento, pensando no futuro. Quais serão suas escolhas a partir de agora?",
            "slider": True, "valor_atual": invest_atual, "idade_marco": 16,
            "opcoes": [
                {"template": "🏦 Apenas Contribuir em Previdência (R$ {val},00)", "emoji": "🏦"},
                {"template": "📚 Comprar Livros (-R$ 500,00) E 🏦 Contribuir (R$ {val},00)", "livros": 1, "saldo": -500,
                 "emoji": "🏦📚"},
                {"texto": "📚 Apenas Comprar Livros (-R$ 500,00)", "livros": 1, "saldo": -500, "invest_set": 0,
                 "emoji": "📚"},
                {"texto": "🚫 Não estudar e Não Contribuir em Previdência", "invest_set": 0}
            ]
        }
    elif marco == 10:
        return {
            "titulo": "VOCÊ ENTROU NA FACULDADE!",
            "cenario": "Aos 18 anos, chegou a hora de escolher o seu caminho acadêmico para o futuro.",
            "opcoes": [
                {"texto": "🌾 Agrárias (Ex: Agronomia; Zootecnia; Agronegócio)", "emoji": "🌾", "saldo": 0},
                {"texto": "🧬 Biológicas (Ex: Medicina; Ed. Física; Nutrição)", "emoji": "🧬", "saldo": 0},
                {"texto": "💻 Exatas (Ex: Engenharia; Matemática; Computação)", "emoji": "💻", "saldo": 0},
                {"texto": "🎭 Humanas (Ex: Direito; Economia; Letras)", "emoji": "🎭", "saldo": 0}
            ]
        }
    elif marco == 13:
        return {
            "titulo": "NOVA DECISÃO DE FUTURO",
            "cenario": "Você está com 20 anos. A faculdade exige mais, e como o tempo está passando, que tal planejar e se preparar para o futuro? Você pode reajustar ou começar a contribuir com a Previdência Complementar.",
            "slider": True, "valor_atual": invest_atual, "idade_marco": 20,
            "opcoes": [
                {"template": "🏦 Apenas Contribuir em Previdência (R$ {val},00)", "emoji": "🏦"},
                {"template": "📚 Comprar Livros (-R$ 500,00) E 🏦 Contribuir (R$ {val},00)", "livros": 1, "saldo": -500,
                 "emoji": "🏦📚"},
                {"texto": "📚 Apenas Comprar Livros (-R$ 500,00)", "livros": 1, "saldo": -500, "invest_set": 0,
                 "emoji": "📚"},
                {"texto": "🚫 Não estudar e Não Contribuir em Previdência", "invest_set": 0}
            ]
        }
    elif marco == 20:
        salario = 3500 if eq["qtd_livros"] == 0 else (3750 if eq["qtd_livros"] == 1 else 4000)
        return {
            "sem_escolha": True, "titulo": "MERCADO DE TRABALHO",
            "cenario": f"Aos 24 anos, você se formou e conseguiu um emprego!\nSua renda base agora é R$ {salario},00/rodada.\n(Caso você tenha mesada da avó, ela será cancelada!)",
            "novo_salario_base": salario, "corta_mesada": True, "saldo": 0, "emoji": "💼"
        }
    elif marco == 24:
        return {
            "titulo": "OS 30 ANOS CHEGARAM",
            "cenario": "Aos 30 anos, você já está consolidado no mercado de trabalho. Vai turbinar a sua carreira ou focar nas suas contribuições?",
            "slider": True, "valor_atual": invest_atual, "idade_marco": 30,
            "opcoes": [
                {"template": "🏦 Apenas Contribuir em Previdência (R$ {val},00)", "emoji": "🏦"},
                {"template": "🎓 Fazer Pós (-R$ 3.000,00) E 🏦 Contribuir (R$ {val},00)", "add_salario": 2000,
                 "saldo": -3000, "emoji": "🏦🎓"},
                {"texto": "🎓 Apenas Pós (-R$ 3.000,00)", "add_salario": 2000, "saldo": -3000,
                 "invest_set": 0, "emoji": "🎓"},
                {"texto": "🚫 Não estudar e Não Contribuir em Previdência", "invest_set": 0}
            ]
        }
    elif marco == 30:
        return {
            "titulo": "A CHEGADA DOS 45 ANOS",
            "cenario": "Você chegou aos 45 anos. É a hora de garantir a aposentadoria ou se capacitar para virar Senior na carreira!",
            "slider": True, "valor_atual": invest_atual, "idade_marco": 45,
            "opcoes": [
                {"template": "🏦 Apenas Contribuir em Previdência (R$ {val},00)", "emoji": "🏦"},
                {"template": "📈 Capacitar para Sênior (-R$ 2.500,00) E 🏦 Contribuir (R$ {val},00)", "add_salario": 2000,
                 "saldo": -2500, "emoji": "🏦📈"},
                {"texto": "📈 Apenas Capacitar para Sênior (-R$ 2.500,00)", "add_salario": 2000,
                 "saldo": -2500, "invest_set": 0, "emoji": "📈"},
                {"texto": "🚫 Não capacitar e Não Contribuir em Previdência", "invest_set": 0}
            ]
        }


# ==========================================
# 🏆 FASE FINAL: RANKING E JUROS COMPOSTOS
# ==========================================
def calcular_ranking_final():
    """Reproduz a matemática exata de juros compostos do seu arquivo PyQt6 para todas as equipes."""
    for e in estado_jogo["equipes"]:
        a16 = e.get("aporte_16", 0)
        a20 = e.get("aporte_20", a16)
        a30 = e.get("aporte_30", a20)
        a45 = e.get("aporte_45", a30)

        saldo_prev = 0
        hist = [0]
        bolso = 0

        # Verifica os aportes únicos e mapeia para o mês exato
        aportes_extras = {}
        for au in e.get("aportes_unicos", []):
            if au["casa"] == 30:
                mes_exato = 348  # (30 anos -> 45 anos reais = 348 meses)
            else:
                mes_exato = int((au["casa"] / 40.0) * 588)

            if mes_exato >= 588: mes_exato = 587
            aportes_extras[mes_exato] = aportes_extras.get(mes_exato, 0) + au["valor"]

        # Loop de 588 meses (dos 16 aos 65 anos) a 1% ao mês
        for mes in range(588):
            if mes < 48:
                pmt = a16  # 16 aos 20
            elif mes < 168:
                pmt = a20  # 20 aos 30
            elif mes < 348:
                pmt = a30  # 30 aos 45
            else:
                pmt = a45  # 45 aos 65

            saldo_prev = saldo_prev * 1.01 + pmt
            bolso += pmt

            if mes in aportes_extras:
                valor_extra = aportes_extras[mes]
                saldo_prev += valor_extra
                bolso += valor_extra

            hist.append(saldo_prev)

        e["prev_hist"] = hist
        e["prev_bolso"] = bolso
        e["prev_juros"] = saldo_prev - bolso

        # Relatório HTML para UI do Ranking
        txt_hist = f"&nbsp;&nbsp;• <b>Dos 16 aos 20 anos:</b> R$ {a16},00/mês<br>&nbsp;&nbsp;• <b>Dos 20 aos 30 anos:</b> R$ {a20},00/mês<br>&nbsp;&nbsp;• <b>Dos 30 aos 45 anos:</b> R$ {a30},00/mês<br>&nbsp;&nbsp;• <b>Dos 45 aos 65 anos:</b> R$ {a45},00/mês"
        if e.get("aportes_unicos"):
            txt_hist += "<br>&nbsp;&nbsp;• <b style='color:#1976D2;'>Aportes Únicos Extras:</b> "
            txt_hist += ", ".join([f"{fmt_saldo(au['valor'])} (Casa {au['casa']})" for au in e["aportes_unicos"]])
        e["historico_aportes_txt"] = txt_hist

        # A regra de Ouro: Se fechar negativo, perde TUDO!
        if e["saldo"] < 0:
            e["patrimonio_total"] = e["saldo"]
        else:
            e["patrimonio_total"] = e["saldo"] + saldo_prev

    # Separando os ganhadores dos desclassificados
    positivos = [e for e in estado_jogo["equipes"] if e["saldo"] >= 0]
    negativados = [e for e in estado_jogo["equipes"] if e["saldo"] < 0]

    positivos.sort(key=lambda e: -e["patrimonio_total"])
    negativados.sort(key=lambda e: -e["patrimonio_total"])
    estado_jogo["ranking"] = positivos + negativados


def mudar_view_ranking(novo_idx):
    estado_jogo["ranking_view_idx"] = novo_idx
    estado_jogo["instancia_telas"].refresh()


def reiniciar_jogo_completo():
    estado_jogo.update({
        "equipes_nomes": [], "ordem_final": [], "modo_turbo": False,
        "tela_atual": "menu", "equipes": [], "turno_atual": 0,
        "aguardando": False, "passos_atuais": 0, "fila_eventos": [],
        "formados": [], "jogo_finalizado": False, "ranking": []
    })
    estado_jogo["instancia_telas"].refresh()


# ==========================================
# ⚙️ MOTOR CENTRAL DE MOVIMENTO E EVENTOS
# ==========================================

def aplicar_movimento(passos):
    if estado_jogo.get("jogo_finalizado"): return

    eq = estado_jogo["equipes"][estado_jogo["turno_atual"]]
    pos_anterior = eq["posicao"]
    nova_pos = min(pos_anterior + passos, TOTAL_CASAS)
    eq["posicao"] = nova_pos

    renda_liquida = eq["salario_base"] + eq.get("renda_extra", 0) - eq["investimento_turno"]
    eq["saldo"] += renda_liquida

    marcos_cruzados = [m for m in [3, 10, 13, 20, 24, 30] if
                       pos_anterior < m <= nova_pos and m not in eq["marcos_passados"]]
    eq["marcos_passados"].extend(marcos_cruzados)

    estado_jogo["fila_eventos"] = []

    for m in marcos_cruzados:
        estado_jogo["fila_eventos"].append({"tipo": "marco", "num": m})

    if nova_pos >= TOTAL_CASAS:
        estado_jogo["fila_eventos"].append({"tipo": "chegada"})
    elif nova_pos in EVENTOS_FIXOS:
        ev = dict(EVENTOS_FIXOS[nova_pos])

        # === NOVO TEXTO GIGANTE E DETALHADO DO IMPOSTO DE RENDA ===
        if ev.get("regra_ir"):
            if eq.get("investimento_turno", 0) > 0:
                ev[
                    "cenario"] = "Chegou a hora de acertar as contas com o Leão e ver como ficará sua declaração de Imposto de Renda. Como você contribuiu ativamente para sua Previdência Complementar, tem o benefício fiscal de dedução de até 12% da renda declarada.\n\n<span style='color:#2E7D32;'>Que bom! Você não pagará imposto de renda e ainda terá devolução de R$ 6.000,00 que foram descontados no seu salário no decorrer do ano anterior. Além disso, juntou dinheiro na Previdência Complementar para o seu futuro!</span>"
                ev["saldo"] = 6000
            else:
                ev[
                    "cenario"] = "Chegou a hora de acertar as contas com o Leão e ver como ficará seu imposto de renda. Como você NÃO contribui ativamente para a Previdência Complementar, NÃO tem o benefício fiscal de dedução de até 12% da renda declarada.\n\n<span style='color:#D32F2F;'>Que pena. Você pagará imposto de renda no valor de R$ 6.000,00 e além disso, NÃO juntou dinheiro na Previdência Complementar para o seu futuro.</span>"
                ev["saldo"] = -6000
        # ==========================================================

        ev["sem_escolha"] = True
        estado_jogo["fila_eventos"].append({"tipo": "card", "dados": ev})
    elif nova_pos in DILEMAS_FIXOS:
        estado_jogo["fila_eventos"].append({"tipo": "card", "dados": dict(DILEMAS_FIXOS[nova_pos])})
    else:
        estado_jogo["fila_eventos"].append({"tipo": "card", "dados": {"titulo": "Dia Tranquilo",
                                                                      "cenario": "Nada de novo no front. Siga em frente!",
                                                                      "opcoes": [{"texto": "Avançar", "saldo": 0}]}})

    estado_jogo["instancia_tabuleiro"].refresh()
    estado_jogo["instancia_painel"].refresh()
    processar_proximo_evento()


def exibir_proxima_equipe():
    eq_prox = estado_jogo["equipes"][estado_jogo["turno_atual"]]
    cor_prox = CORES_EQUIPES[estado_jogo["turno_atual"] % len(CORES_EQUIPES)]

    with ui.dialog().props('persistent') as dialog_proxima:
        with ui.card().classes(
                'w-[380px] bg-[#212121] rounded-2xl border-4 border-[#424242] p-6 items-center flex flex-col'):
            ui.label("PRÓXIMA EQUIPE").classes('text-[11px] font-black text-[#616161] tracking-widest')
            ui.element('div').classes('w-full h-1 mt-1 rounded-sm mb-4').style(f'background-color: {cor_prox};')
            ui.label(eq_prox["nome"]).classes('text-[28px] font-black text-white font-serif')
            ui.label(f"Casa {eq_prox['posicao']} · 💰 {fmt_saldo(eq_prox['saldo'])}").classes(
                'text-[14px] text-[#757575]')

            def liberar_jogo():
                dialog_proxima.close()
                # O timer(0.2) garante que o NiceGUI não trave fechando e abrindo modais ao mesmo tempo
                ui.timer(0.2, lambda: (estado_jogo["instancia_tabuleiro"].refresh(), estado_jogo["instancia_painel"].refresh()), once=True)

            ui.button("Vamos lá!", on_click=liberar_jogo).classes(
                'text-white font-black py-2 px-8 rounded-lg mt-4 cursor-pointer w-full').style(
                'background-color: #43A047 !important;').props('unelevated')
    dialog_proxima.open()


def avancar_turno():
    if all(e.get("formado") for e in estado_jogo["equipes"]):
        if estado_jogo.get("jogo_finalizado"): return  # Previne que chame 2 vezes

        estado_jogo["aguardando"] = False
        estado_jogo["jogo_finalizado"] = True
        estado_jogo["instancia_painel"].refresh()

        ui.notify("🏁 FIM DE JOGO! Calculando os Resultados...", type='positive', position='center', timeout=3000)

        # Chama a matemática Final!
        calcular_ranking_final()
        estado_jogo["ranking_view_idx"] = len(estado_jogo["ranking"]) - 1
        estado_jogo["tela_atual"] = "ranking"

        # Timer generoso para o último modal sumir da tela antes de mudar pro Ranking
        ui.timer(2.0, estado_jogo["instancia_telas"].refresh, once=True)
        return

    n = len(estado_jogo["equipes"])
    prox = (estado_jogo["turno_atual"] + 1) % n

    while estado_jogo["equipes"][prox].get("formado"):
        prox = (prox + 1) % n

    estado_jogo["turno_atual"] = prox
    estado_jogo["aguardando"] = False
    exibir_proxima_equipe()


def abrir_enquete(dados):
    with ui.dialog().props('persistent') as dialog_enquete:
        with ui.card().classes(
                'w-[700px] max-w-[95vw] bg-[#FFFDE7] rounded-[22px] border-4 border-[#FBC02D] p-5 shadow-2xl max-h-[95vh] overflow-y-auto scrollbar-hide'):

            with ui.column().classes('w-full items-center gap-0'):
                eq = estado_jogo["equipes"][estado_jogo["turno_atual"]]

                ui.label(dados.get("titulo", "EVENTO DA VIDA").upper()).classes(
                    'text-[13px] font-black text-[#999] tracking-widest text-center w-full mt-1')
                ui.label(eq["nome"]).classes('text-[16px] font-bold text-[#555] text-center mt-1 w-full')
                ui.html(dados.get("cenario", "").replace('\n', '<br>')).classes(
                    'text-[17px] font-bold text-[#222] font-serif py-2 text-center w-full leading-relaxed')

                slider_val = {"v": dados.get("valor_atual", 0)}
                botoes_dinamicos = []

                if dados.get("slider"):
                    idx_atual = 0 if slider_val["v"] == 0 else int((slider_val["v"] - 50) / 50)

                    with ui.column().classes(
                            'w-full items-center bg-white p-3 rounded-xl border border-gray-200 mb-2 shadow-sm'):
                        lbl_slider = ui.label(
                            f"Reajustar Contribuição Mensal: R$ {slider_val['v']},00 / rodada").classes(
                            'text-[16px] font-black text-[#1976D2] text-center w-full')

                        def on_slider_change(e):
                            v = 0 if e.value == 0 else 50 + e.value * 50
                            slider_val["v"] = v
                            lbl_slider.text = f"Reajustar Contribuição Mensal: R$ {v},00 / rodada"
                            for btn, template in botoes_dinamicos:
                                btn.text = template.format(val=v)

                        ui.slider(min=0, max=19, value=idx_atual, on_change=on_slider_change).classes(
                            'w-full mt-1').props('color="primary"')
                        ui.label("Arraste a barrinha azul para reajustar o valor").classes(
                            'text-[11px] text-gray-500 italic mt-1 w-full text-center')

                botoes_container = ui.column().classes('w-full gap-2 mt-1')
                res_container = ui.column().classes('w-full items-center mt-2 hidden')

                def resolver_escolha(op):
                    botoes_container.classes(add='hidden')
                    res_container.classes(remove='hidden')

                    op_copy = dict(op)

                    if dados.get("slider") and "template" in op_copy:
                        op_copy["invest_set"] = slider_val["v"]
                        if slider_val["v"] == 0 and "emoji" in op_copy:
                            op_copy["emoji"] = op_copy["emoji"].replace("🏦", "")

                    if "idade_marco" in dados:
                        op_copy["idade_marco"] = dados["idade_marco"]

                    eq["saldo"] += op_copy.get("saldo", 0)
                    eq["emojis"] += op_copy.get("emoji", "")
                    eq["qtd_livros"] += op_copy.get("livros", 0)

                    if op_copy.get("corta_mesada") and eq.get("tem_mesada_vo"):
                        eq["renda_extra"] -= 200
                        eq["tem_mesada_vo"] = False
                        eq["emojis"] = eq["emojis"].replace("👵", "")

                    if op_copy.get("flag_mesada"):
                        eq["renda_extra"] += 200
                        eq["tem_mesada_vo"] = True

                    if op_copy.get("flag_promocao"):
                        eq["salario_base"] = eq.get("salario_base", 0) * 2

                    if "novo_salario_base" in op_copy:
                        eq["salario_base"] = op_copy["novo_salario_base"]

                    if "add_salario" in op_copy:
                        eq["salario_base"] += op_copy["add_salario"]

                    if "invest_set" in op_copy:
                        eq["investimento_turno"] = op_copy["invest_set"]

                    if "idade_marco" in op_copy:
                        idade = op_copy["idade_marco"]
                        eq[f"aporte_{idade}"] = eq["investimento_turno"]

                    if "aporte_unico" in op_copy:
                        eq.setdefault("aportes_unicos", []).append(
                            {"casa": eq["posicao"], "valor": op_copy["aporte_unico"]})

                    # REGISTRO HISTORICO DAS ESCOLHAS (Usado na Fase 5 e Final)
                    if "historico_escolhas" not in eq: eq["historico_escolhas"] = []
                    eq["historico_escolhas"].append({
                        "casa": eq["posicao"],
                        "texto": op_copy.get("texto", dados.get("titulo", "Evento da Casa")),
                        "saldo": op_copy.get("saldo", 0),
                        "invest": op_copy.get("invest_set", None)
                    })

                    with res_container:
                        saldo = op_copy.get("saldo", 0)
                        if saldo != 0:
                            cor = "#2E7D32" if saldo >= 0 else "#C62828"
                            ui.html(
                                f"<span style='color:{cor}; font-size:22px; font-weight:900;'>💰 {'+' if saldo > 0 else ''}{fmt_saldo(saldo)}</span>")

                        if "invest_set" in op_copy:
                            ui.html(
                                f"<span style='color:#1976D2; font-size:18px; font-weight:900;'>🏦 Contribuição Definida: R$ {op_copy['invest_set']},00/rod</span>")
                        if op_copy.get("livros"):
                            ui.html(
                                "<span style='color:#F57C00; font-size:18px; font-weight:900;'>📚 Novo Conhecimento!</span>")
                        if "novo_salario_base" in op_copy:
                            ui.html(
                                f"<span style='color:#388E3C; font-size:18px; font-weight:900;'>💼 Nova Renda Base: R$ {op_copy['novo_salario_base']},00/rod</span>")
                        if "add_salario" in op_copy:
                            ui.html(
                                f"<span style='color:#388E3C; font-size:18px; font-weight:900;'>💼 Renda Aumentou! + R$ {op_copy['add_salario']},00/rod</span>")
                        if "renda_extra" in op_copy:
                            ui.html(
                                f"<span style='color:#1976D2; font-size:18px; font-weight:900;'>👵 Vovó te ama! Renda Extra +R$ 200,00/rod</span>")

                        if not any(
                                [saldo, "invest_set" in op_copy, op_copy.get("livros"), "novo_salario_base" in op_copy,
                                 "add_salario" in op_copy, op_copy.get("renda_extra")]):
                            ui.html(
                                "<span style='color:#333; font-size:16px;'>Nenhum impacto financeiro imediato.</span>")

                        # O Respiro Mágico de 0.2s salva o jogo de congelar!
                        ui.button("Avançar →", on_click=lambda: (
                            dialog_enquete.close(),
                            ui.timer(0.2, lambda: (estado_jogo["instancia_painel"].refresh(), processar_proximo_evento()), once=True)
                        )).classes('w-full text-white font-black py-2 rounded-xl mt-4 cursor-pointer').style(
                            'background-color: #333 !important;').props('unelevated')

                with botoes_container:
                    if dados.get("sem_escolha"):
                        resolver_escolha(dados)
                    else:
                        for op in dados.get("opcoes", []):
                            if "template" in op:
                                txt = op["template"].format(val=slider_val["v"])
                                btn = ui.button(txt, on_click=lambda o=op: resolver_escolha(o)).classes(
                                    'w-full text-white font-black text-[13px] p-3 rounded-xl cursor-pointer shadow-md leading-tight min-h-[48px]').style(
                                    'background-color: #1976D2 !important; white-space: normal !important; height: auto;').props(
                                    'unelevated')
                                botoes_dinamicos.append((btn, op["template"]))
                            else:
                                ui.button(op.get("texto", ""), on_click=lambda o=op: resolver_escolha(o)).classes(
                                    'w-full text-white font-black text-[13px] p-3 rounded-xl cursor-pointer shadow-md leading-tight min-h-[48px]').style(
                                    'background-color: #1976D2 !important; white-space: normal !important; height: auto;').props(
                                    'unelevated')

    dialog_enquete.open()


def processar_proximo_evento():
    if not estado_jogo["fila_eventos"]:
        avancar_turno()
        return

    ev = estado_jogo["fila_eventos"].pop(0)
    eq = estado_jogo["equipes"][estado_jogo["turno_atual"]]

    if ev["tipo"] == "chegada":
        if not eq["formado"]:
            eq["formado"] = True
            estado_jogo["formados"].append(eq["nome"])

        pos_chegada = estado_jogo["formados"].index(eq["nome"]) + 1
        idx = min(pos_chegada - 1, len(PREMIOS_CHEGADA) - 1)
        abrir_enquete({
            "sem_escolha": True, "titulo": "CHEGADA / APOSENTADORIA",
            "cenario": f"Você completou 65 anos em {pos_chegada}º lugar! Aproveite a sua aposentadoria.",
            "saldo": PREMIOS_CHEGADA[idx]
        })
    elif ev["tipo"] == "card":
        abrir_enquete(ev["dados"])
    elif ev["tipo"] == "marco":
        abrir_enquete(gerar_card_marco(ev["num"], eq))


async def abrir_giro():
    if estado_jogo["aguardando"] or estado_jogo.get("jogo_finalizado"): return

    estado_jogo["aguardando"] = True

    eq = estado_jogo["equipes"][estado_jogo["turno_atual"]]
    is_turbo = estado_jogo.get("modo_turbo", False)
    passos = random.randint(1, 9) if is_turbo else random.randint(1, 6)
    estado_jogo["passos_atuais"] = passos

    ui_refs['lbl_dado_sub'].text = "SUPER DADO 🚀" if is_turbo else "DADO CLÁSSICO"
    ui_refs['lbl_dado_num'].style('color: #FFCA28 !important;' if is_turbo else 'color: white !important;')
    ui_refs['lbl_dado_eq'].text = eq["nome"]
    ui_refs['lbl_dado_msg'].text = "girando..."

    # Esconde o botão usando a forma nativa do framework
    ui_refs['btn_dado_avancar'].set_visibility(False)

    ui_refs['dialog_dado'].open()

    for _ in range(18):
        await asyncio.sleep(0.065)
        if is_turbo:
            ui_refs['lbl_dado_num'].text = str(random.randint(1, 9))
        else:
            ui_refs['lbl_dado_num'].text = random.choice(["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"])
        ui_refs['lbl_dado_num'].update()

    if is_turbo:
        ui_refs['lbl_dado_num'].text = str(passos)
    else:
        ui_refs['lbl_dado_num'].text = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"][passos - 1]

    ui_refs['lbl_dado_num'].update()
    ui_refs['lbl_dado_msg'].text = f"Tirou {passos} casa(s)!"

    # Exibe o botão de baixo com perfeição
    ui_refs['btn_dado_avancar'].set_visibility(True)


def abrir_status_equipe(idx):
    if estado_jogo.get("aguardando"): return

    eq = estado_jogo["equipes"][idx]
    cor_eq = CORES_EQUIPES[idx % len(CORES_EQUIPES)]
    idade_aprox = calcular_idade_exata(eq['posicao'])

    with ui.dialog() as dialog, ui.card().classes(
            'w-[500px] max-w-[95vw] p-6 bg-[#FAFAFA] rounded-2xl flex flex-col items-center shadow-2xl max-h-[95vh] overflow-y-auto'):
        with ui.column().classes('w-full items-center gap-0'):
            ui.label("📊 STATUS DA EQUIPE").classes('text-[13px] font-black text-[#999] tracking-widest mb-2')

            with ui.row().classes('w-full items-center gap-4 mb-4'):
                ui.element('div').classes('w-12 h-12 rounded-full border-4 shadow-md flex-shrink-0').style(
                    f'background-color: {cor_eq}; border-color: {cor_eq}80;')
                with ui.column().classes('gap-0 flex-grow'):
                    ui.label(eq['nome']).classes('text-2xl font-black text-[#333] leading-none')
                    ui.label(f"Idade aproximada: {idade_aprox} anos | Casa {eq['posicao']}").classes(
                        'text-[14px] font-bold text-[#666]')

            with ui.column().classes('w-full bg-white p-4 rounded-xl border border-[#E0E0E0] gap-2 shadow-sm'):
                ui.label("💰 Relatório Financeiro").classes('font-black text-[#1A237E] mb-1')
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label("Conta Corrente (Saldo Vivo):").classes('font-bold text-[#555]')
                    ui.label(fmt_saldo(eq['saldo'])).classes('font-black text-[18px] text-[#2E7D32]')

                ui.separator().classes('my-1')

                with ui.row().classes('w-full justify-between'):
                    ui.label("Salário Base (Trabalho):").classes('text-[#555]')
                    ui.label(f"R$ {eq['salario_base']},00").classes('font-bold')

                if eq.get('renda_extra', 0) > 0:
                    with ui.row().classes('w-full justify-between'):
                        ui.label("Renda Extra (Vovó):").classes('text-[#555]')
                        ui.label(f"+ R$ {eq['renda_extra']},00").classes('font-bold text-[#1976D2]')

                with ui.row().classes('w-full justify-between'):
                    ui.label("Investimento em Previdência:").classes('text-[#555]')
                    ui.label(f"- R$ {eq['investimento_turno']},00").classes('font-bold text-[#D32F2F]')

                renda_liquida = eq["salario_base"] + eq.get("renda_extra", 0) - eq["investimento_turno"]
                cor_rl = "#1976D2" if renda_liquida > 0 else ("#D32F2F" if renda_liquida < 0 else "#999")
                with ui.row().classes('w-full justify-between mt-2 pt-2 border-t border-[#EEE]'):
                    ui.label("Renda Líquida na Rodada:").classes('font-black text-[#333]')
                    ui.label(f"R$ {renda_liquida},00").classes('font-black text-[16px]').style(f'color: {cor_rl};')

            with ui.column().classes('w-full bg-white p-4 rounded-xl border border-[#E0E0E0] gap-2 mt-3 shadow-sm'):
                ui.label("🎒 Conquistas da Vida").classes('font-black text-[#1A237E] mb-1')

                # 1. Livros (Mudado o nome de "Livros Lidos:" para "Livros:")
                with ui.row().classes('w-full justify-between'):
                    ui.label("Livros:").classes('font-bold text-[#555]')
                    ui.label(f"{eq.get('qtd_livros', 0)} 📚").classes('font-black text-[#F57C00]')

                # 2. Pós-Graduação (Aparece condicionalmente)
                if eq.get('fez_pos_graduacao', False) or '🎓' in eq.get('emojis', ''):
                    with ui.row().classes('w-full justify-between'):
                        ui.label("Pós-Graduação:").classes('font-bold text-[#555]')
                        ui.label("Concluída 🎓").classes('font-black text-[#2E7D32]')

                # 3. Capacitação (Aparece condicionalmente)
                if eq.get('capacitacao_senior', False) or '📈' in eq.get('emojis', ''):
                    with ui.row().classes('w-full justify-between'):
                        ui.label("Capacitação:").classes('font-bold text-[#555]')
                        ui.label("Sênior 📈").classes('font-black text-[#1976D2]')

                # 4. Emojis Acumulados
                with ui.row().classes('w-full justify-between'):
                    ui.label("Emojis Acumulados:").classes('font-bold text-[#555]')
                    ui.label(agrupar_emojis(eq.get("emojis", "")) or "Nenhum").classes('font-black text-[#333]')

            ui.button("Fechar", on_click=dialog.close).classes(
                'w-full mt-6 font-bold py-3 rounded-xl cursor-pointer hover:bg-gray-300 transition-colors').style(
                'background-color: #E0E0E0 !important; color: #333 !important;').props('unelevated')
    dialog.open()


# ==========================================
# 🗔 DIÁLOGOS ESTÁTICOS E SANDBOX
# ==========================================
def abrir_como_comecar():
    with ui.dialog() as dialog, ui.card().classes('w-[500px] p-6 bg-white rounded-2xl border-2 border-[#1A237E]'):
        ui.label("🚀 Como Iniciar?").classes('text-xl font-black text-[#1A237E] w-full text-center mb-2')
        ui.html('''
            <div style='font-size: 15px; color: #333; line-height: 1.6;'>
            <p style="margin-bottom: 15px;">Bem-vindo ao <b>Jogo da Vida: Educação Financeira e Previdenciária</b>! Para iniciar a sua jornada, siga estes passos simples:</p>
            <ul style='margin-top: 5px; margin-bottom: 15px; list-style-type: disc; padding-left: 20px;'>
                <li style='margin-bottom: 8px;'>Digite o nome do jogador ou da equipe no campo de texto! <b>“Defina seu nome…”</b>.</li>
                <li style='margin-bottom: 8px;'>Clique no botão <b>"+"</b> para adicionar o jogador.</li>
                <li style='margin-bottom: 8px;'>Repita o processo até que <b>pelo menos 2 jogadores</b> estejam cadastrados.</li>
                <li style='margin-bottom: 8px;'>Quando todos estiverem na lista, clique no botão azul <b>"🎲 Sortear Ordem do Jogo"</b>.</li>
            </ul>
            <p>Não se preocupe, na próxima tela você terá acesso ao Manual Completo com todas as regras do jogo antes de rolar os dados!</p>
            </div>
        ''')
        ui.button("Entendi!", on_click=dialog.close).classes(
            'text-white font-bold py-2 px-6 rounded-lg mt-4 self-center cursor-pointer').style(
            'background-color: #FF9800 !important;').props('unelevated')
    dialog.open()


def abrir_manual_completo():
    with ui.dialog() as dialog, ui.card().classes(
            'w-[750px] max-w-full h-[85vh] p-8 bg-white rounded-2xl border-2 border-[#1A237E] flex flex-col'):
        ui.label("📖 Manual Completo do Jogo").classes('text-2xl font-black text-[#1A237E] w-full text-center mb-4')
        with ui.scroll_area().classes('flex-grow w-full px-4'):
            ui.html('''
            <div style='font-size: 14px; color: #333; line-height: 1.5;'>
            <div style='color: #1A237E; font-size: 18px; font-weight: 900; margin-bottom: 5px; text-align: center;'>CARDS JOGO DA VIDA: EDUCAÇÃO FINANCEIRA E PREVIDENCIÁRIA</div>
            <p style='text-align: center; font-weight: bold; color: #555;'>“Como funciona o jogo?”</p>
            <p>O jogo simula a vida dos participantes com escolhas financeiras e previdenciárias ao longo dos 16 aos 65 anos. As escolhas feitas vão interferir na qualidade de vida.</p>
            <p>Durante a jornada até a aposentadoria, o jogador passará por marcos fundamentais, em que precisará fazer escolhas que serão determinantes para o futuro. As escolhas estão relacionadas a investimentos, educação e saúde.</p>
            <p>A duração do jogo depende da quantidade de jogadores, mas a estimativa média é de 15 minutos.</p>
            <hr style='border: 1px solid #E0E0E0; margin: 15px 0;'>
            <div style='color: #1A237E; font-size: 17px; font-weight: 900; margin-bottom: 5px;'>Como Começar</div>
            <p>É necessário no mínimo dois jogadores. Cada jogador pode ser uma única pessoa ou uma equipe, como por exemplo, um grupo de amigos.</p>
            <p>Após registrar o jogador ou da equipe na caixinha “Defina seu nome…”, cada jogador deve clicar em <b>+</b>. Assim que todos os jogadores estiverem registrados, deve-se clicar em <b>“sortear a ordem do jogo”</b>. Aparecerá a ordem que os participantes jogarão. Ao clicar em ver regras do jogo, a próxima tela trará informações sobre o funcionamento do jogo. Entendidas as regras, o jogador deve clicar em <b>“vamos para o tabuleiro para começar a jogar”</b>.</p>
            <p style='background: #FFF3E0; padding: 10px; border-radius: 5px; border-left: 4px solid #FF9800;'><b>Lembrete:</b> Os jogadores deverão ser sinceros nas respostas, e escolher as opções que realmente fariam, pois o jogo tende a simular sobre a educação financeira e previdenciária na vida real.</p>
            <hr style='border: 1px solid #E0E0E0; margin: 15px 0;'>
            <div style='color: #1A237E; font-size: 17px; font-weight: 900; margin-bottom: 5px;'>Princípios do Jogo</div>
            <p>Cada jogador inicia com <b>1 salário mínimo</b> vigente em 2026, o que corresponde ao valor de <b>R$ 1.621,00</b>.</p>
            <p>O saldo em conta, renda e emojis conquistados no decorrer do jogo aparecerão no lado direito da tela. Os emojis são:</p>
            <ul style='margin-top: 5px; margin-bottom: 5px; list-style-type: disc; padding-left: 20px;'>
                <li style='margin-bottom: 8px;'>🏦 <b>Investimento na Previdência Complementar:</b> Todo dinheiro investido é um cuidado pessoal e um passo importante em direção ao futuro financeiro mais seguro e tranquilo. Ao fazer a escolha de investir em Previdência Complementar, o dinheiro será aplicado a uma taxa de juros compostos, projetada em <b>1% ao mês</b>.</li>
                <li style='margin-bottom: 8px;'>📚 <b>Investimento em Educação:</b> Cursos, livros e treinamentos geram conhecimento acumulado e contribuem para aumentar o salário quando o jogador entrar para o mercado de trabalho.</li>
                <li style='margin-bottom: 8px;'>👵 <b>Vovó:</b> Se a vovó der mesada para o jogador, ele ganha <b>R$ 200,00 extra por rodada</b>. Mas atenção: a mesada acaba assim que o jogador entrar no mercado de trabalho!</li>
                <li style='margin-bottom: 8px;'><b>Faculdade:</b> Independente da área que o jogador for seguir, o salário inicial terá o mesmo valor. Assim que ele se formar, ganhará um emoji. As áreas que podem ser escolhidas são:
                    <ul style='margin-top: 5px; list-style-type: circle; padding-left: 20px;'>
                        <li>🌾 <b>Agrárias:</b> Focadas no cultivo, agronegócio e produção de alimentos. Inclui Agronomia, Zootecnia e Engenharia Florestal, por exemplo.</li>
                        <li>🧬 <b>Biológicas:</b> Focadas no bem-estar físico, animal e ecossistemas. Inclui Medicina, Enfermagem, Odontologia, Medicina Veterinária, Psicologia e Biomedicina.</li>
                        <li>💻 <b>Exatas:</b> Voltadas para números, lógica, dados e infraestrutura. Abrange Engenharias (Civil, Mecânica, de Produção...), Ciência da Computação, Sistemas de Informação, Matemática e Estatística.</li>
                        <li>🎭 <b>Humanas:</b> Focadas no comportamento, na sociedade, leis e mercados, cultura e comunicação. Inclui Pedagogia, Direito, Jornalismo, História, entre outros.</li>
                    </ul>
                </li>
                <li style='margin-bottom: 8px;'>🎓 <b>Pós-Graduação:</b> É uma especialização que permite a ampliação do conhecimento, o que aumenta o salário do jogador.</li>
                <li style='margin-bottom: 8px;'>📈 <b>Capacitação:</b> É uma capacitação profissional, que também possibilita a ampliação do conhecimento, o que também aumenta o salário do jogador.</li>
                <li style='margin-bottom: 8px;'>💼 <b>Maleta:</b> Indica que o jogador começou a receber seu salário profissional.</li>
            </ul>
            <p style='color: #D32F2F; background: #FFEBEE; padding: 10px; border-radius: 5px; border-left: 4px solid #D32F2F;'><b>🚨 CUIDADO:</b> Quem terminar o jogo com a Conta Corrente no vermelho (negativa) perde todos os investimentos e é DESCLASSIFICADO!</p>
            <p>Ao chegar na última casa do jogo, você também recebe o último salário e uma gratificação, de acordo com sua colocação.</p>
            <hr style='border: 1px solid #E0E0E0; margin: 15px 0;'>
            <div style='color: #1A237E; font-size: 17px; font-weight: 900; margin-bottom: 5px;'>Mecânica do Tabuleiro</div>
            <p>É necessário clicar em <b>“girar o dado”</b> para começar o jogo e a cada nova rodada (o jogador será informado sobre quantas casas andará e deverá clicar em avançar). Aparecerá na tela as opções de escolhas de acordo com a quantidade de casas sorteadas. Após escolher a opção desejada, deve clicar em avançar e será a vez do próximo jogador.</p>
            <p>Durante a jornada pelo tabuleiro, o jogador encontrará casas especiais identificadas com o símbolo de exclamação (<b>!</b>), elas representam alguns marcos de vida. Sempre que o jogador passar por uma dessas casas, ele vai poder escolher investir em Previdência Complementar. Estes marcos acontecem aos <b>16, 20, 30 e 45 anos</b>. Para ajudar no controle dessa escolha, a tela do jogo mostra exatamente o valor que o jogador está investindo na sua Previdência Complementar. Em cada uma dessas paradas, as escolhas feitas impactarão diretamente nas reservas financeiras e no patrimônio acumulado até o final do jogo.</p>
            <p>No canto direito do tabuleiro, o jogador acompanha o placar geral do jogo, os emojis conquistados, a renda e o saldo de sua conta corrente (💰) conforme as jogadas vão acontecendo. O grande diferencial é a interatividade: é possível <b>clicar no cartão de qualquer equipe</b> na lista para abrir o perfil detalhado de <b>Status da Equipe</b>. Você encontrará a exata posição do jogador no tabuleiro e a sua idade aproximada. O painel também traz um relatório da <b>Vida Financeira</b> — mostrando a Renda Bruta, o valor investido na Previdência e a Renda Líquida disponível por rodada — além de detalhar as <b>Conquistas e Educação</b>, que exibe o conhecimento acumulado (livros lidos), a situação profissional no mercado de trabalho e o inventário com todas as conquistas obtidas ao longo da vida.</p>
            <hr style='border: 1px solid #E0E0E0; margin: 15px 0;'>
            <div style='color: #1A237E; font-size: 17px; font-weight: 900; margin-bottom: 5px;'>Informações Importantes</div>
            <p>Ao final da partida, o jogador será direcionado para a tela de resultados, onde o conteúdo exibido dependerá do desempenho financeiro mantido ao longo do tabuleiro. Se o jogador conseguir concluir o jogo sem ser desclassificado, a tela apresentará a posição final na partida. Nessa mesma tela, será exibido um resumo detalhado da jornada financeira do jogador, contendo a quantidade de conquistas e emojis acumulados, além do saldo final que restou na conta corrente do jogo. Além disso, a tela também mostra todo o investimento que o jogador fez em previdência complementar, informando o histórico de contribuições, o total investido e o total de rendimentos (juros compostos) ganhos no período, finalizando com a exibição do patrimônio total do jogador, que é a soma do saldo bruto da previdência com o saldo da conta corrente. Esta mesma tela possui o gráfico de evolução, em que são apresentadas as contribuições realizadas de acordo com as idades e rentabilidades. É possível também clicar na opção “Histórico de escolhas” em que são apresentadas as escolhas feitas pelo jogador e os valores gastos ou ganhos. Ao clicar em avançar, o jogador verá a posição dos outros jogadores. Ele deve clicar em classificação geral para conhecer a ordem de classificação.</p>
            <p style='color: #1976D2; font-size: 16px; margin-top: 15px;'><b>🏆 Resultado da competição:</b></p>
            <p>Quem atingir o maior patrimônio ganha o jogo! Se a estratégia financeira resultou em um saldo negativo, a tela apresentará a informação de que o jogador foi desclassificado por terminar o jogo com a conta corrente no vermelho. Nesse caso, todos os ganhos e investimentos serão usados para o pagamento das dívidas. O gráfico de evolução não terá nenhuma informação, pois todos seus investimentos foram utilizados.</p>
            <hr style='border: 1px solid #E0E0E0; margin: 15px 0;'>
            <div style='color: #1A237E; font-size: 17px; font-weight: 900; margin-bottom: 5px;'>Observações:</div>
            <ul style='margin-top: 5px; list-style-type: disc; padding-left: 20px;'>
                <li>Ao clicar em classificação geral é possível ver a classificação de cada jogador, patrimônio e emojis conquistados.</li>
                <li>Ao clicar em finalizar o jogo, é feito o direcionamento para a tela inicial do jogo.</li>
            </ul>
            </div>
            ''')
        ui.button("Fechar Manual", on_click=dialog.close).classes(
            'text-white font-bold py-3 px-8 rounded-lg mt-6 self-center cursor-pointer').style(
            'background-color: #333333 !important;').props('unelevated')
    dialog.open()


def abrir_sobre_marisele():
    with ui.dialog() as dialog, ui.card().classes(
            'w-[580px] max-w-full h-[85vh] p-6 bg-white rounded-2xl border-4 border-[#FF9800] flex flex-col'):
        ui.label("🌟 Conheça a Marisele Previdente").classes(
            'text-2xl font-black text-[#1A237E] w-full text-center mb-1')
        ui.label("Mascote e Influenciadora Virtual").classes(
            'text-sm font-bold text-[#FF9800] tracking-wider w-full text-center mb-4')
        with ui.scroll_area().classes('flex-grow w-full px-2'):
            ui.html('''
                <div style='font-size: 15px; color: #424242; line-height: 1.6; text-align: justify;'>
                <p style='margin-top: 0;'>Personagem idealizada por <b>Cristiano Verardo</b>, Diretor de Seguridade, Relacionamento e Tecnologia da Vexty e porta-voz da iniciativa “Previdência é Coisa de Jovem”, Marisele Previdente agora faz parte do time da Abrapp.</p>
                <p>Conforme apresentado na palestra do PrevShow, realizada durante o 45º Congresso Brasileiro de Previdência Privada (CBPP), e informado por Verardo, Marisele teve todos os direitos de uso e aproveitamento de sua imagem presenteados integralmente para a Associação em junho deste ano.</p>
                <p>Criada com o intuito de tornar a previdência complementar mais acessível e próxima de todos, Marisele foi apresentada ao público no 44º CBPP, realizado no ano passado, após pesquisas e indagações de Verardo ao longo dos últimos anos.</p>
                <div style='background: #F5F5F5; border-left: 4px solid #3F51B5; padding: 12px; margin: 15px 0; border-radius: 6px;'>
                <h4 style='color: #1A237E; margin: 0 0 5px 0; font-size: 16px;'>A Inspiração do Nome</h4>
                <p style='margin: 0;'>Marisele foi inspirada em <b>Gisele Ayabe</b>, a pessoa que realizou a adesão ao seu primeiro plano de previdência em 2005, e em <b>Marisa Bravi</b>, profissional da Abrapp homenageada no 44º CBPP.</p>
                </div>
                <p>A personagem foi criada com o intuito de engajar diversos públicos, das famílias aos jovens, colocando a previdência complementar como uma atitude.</p>
                </div>
            ''')
        with ui.column().classes('w-full mt-4 gap-2'):
            ui.button("📖 Abrir Cartilha da Marisele",
                      on_click=lambda: ui.run_javascript("window.open('/assets/cartilha.pdf', '_blank');")).classes(
                'w-full text-white font-bold py-3 rounded-xl text-md cursor-pointer').style(
                'background-color: #1A237E !important;').props('unelevated')
            ui.button("🎲 Voltar ao Jogo", on_click=dialog.close).classes(
                'w-full text-white font-bold py-3 rounded-xl text-md cursor-pointer').style(
                'background-color: #FF9800 !important;').props('unelevated')
    dialog.open()


def abrir_sandbox(num):
    """Abre o card de leitura da casa do tabuleiro."""
    if estado_jogo["aguardando"]: return

    with ui.dialog() as dialog, ui.card().classes(
            'w-[500px] max-w-[95vw] p-6 bg-[#F5F5F5] rounded-2xl flex flex-col max-h-[90vh] overflow-y-auto'):
        ui.label(f"🏠 Casa {num}").classes('text-2xl font-black text-[#1A237E] w-full text-center mb-4')

        with ui.column().classes('w-full gap-2 items-center'):
            if num in DILEMAS_FIXOS:
                d = DILEMAS_FIXOS[num]
                ui.label(d['titulo']).classes('text-lg font-black text-[#E65100] w-full text-center')
                ui.label(d['cenario']).classes('text-[15px] text-[#333] mb-2 w-full text-center font-bold')
                for op in d['opcoes']:
                    ui.label(op['texto']).classes(
                        'w-full bg-white p-3 rounded-lg border border-gray-200 text-[#333] font-bold shadow-sm text-center')
            elif num in EVENTOS_FIXOS:
                e = EVENTOS_FIXOS[num]
                ui.label(f"⚡ {e['titulo']}").classes('text-lg font-black text-[#E65100] w-full text-center')

                # === REGRA DE OURO NO SANDBOX DO IR ===
                if e.get("regra_ir"):
                    ui.html("""
                        <div class='bg-white p-4 rounded-xl shadow-sm border border-gray-200 mt-2 text-[14.5px] text-[#333] leading-relaxed text-justify'>
                            <p class='font-black text-center text-[#1A237E] mb-2'>Hora de acertar as contas com a Receita Federal!</p>
                            <p class='mb-2'><b class='text-[#2E7D32]'>✔️ SE CONTRIBUI (Previdência):</b><br>Você não paga imposto e tem <b>devolução de R$ 6.000,00</b>, graças ao benefício fiscal de dedução de até 12%.</p>
                            <p><b class='text-[#D32F2F]'>❌ SE NÃO CONTRIBUI:</b><br>Você NÃO tem o benefício fiscal... Que pena. Você <b>pagará imposto no valor de R$ 6.000,00</b>.</p>
                        </div>
                    """)
                else:
                    ui.label(e['cenario']).classes(
                        'text-[15px] text-[#333] w-full text-center font-bold bg-white p-4 rounded-xl shadow-sm border border-gray-200 mt-2')

            elif num in [3, 10, 13, 20, 24, 30]:
                ui.label("🌟 Marco de Vida").classes('text-lg font-black text-[#1A237E] w-full text-center')
                ui.label(
                    "Nesta casa acontece uma importante decisão para o futuro ou uma virada de chave no jogo.").classes(
                    'text-[15px] text-[#555] w-full text-center bg-white p-4 rounded-xl shadow-sm border border-gray-200 mt-2')
            elif num == TOTAL_CASAS:
                ui.label("🏁 CHEGADA / APOSENTADORIA").classes('text-lg font-black text-[#2E7D32] w-full text-center')
                ui.label(
                    "O jogo encerra aqui e os Juros Compostos são calculados para revelar o Grande Campeão!").classes(
                    'text-[15px] text-[#333] w-full text-center bg-white p-4 rounded-xl shadow-sm border border-gray-200 mt-2')
            else:
                ui.label("Dia tranquilo. Nada de novo no front. Apenas avance!").classes(
                    'text-[16px] text-[#555] w-full text-center bg-white p-4 rounded-xl shadow-sm border border-gray-200')

        ui.button("Entendi", on_click=dialog.close).classes(
            'w-full text-white font-bold py-3 rounded-xl mt-6 cursor-pointer').style(
            'background-color: #1A237E !important;').props('unelevated')
    dialog.open()


def abrir_ajuda_tabuleiro():
    with ui.dialog() as dialog, ui.card().classes('w-[650px] p-6 bg-white rounded-2xl border-2 border-[#1A237E]'):
        ui.label("🧭 Entendendo o Tabuleiro").classes('text-xl font-black text-[#1A237E] w-full text-center mb-4')
        with ui.scroll_area().classes('w-full h-[350px] px-2'):
            ui.html('''
                <div style='font-size: 14px; color: #333; line-height: 1.5;'>
                <p style="margin-bottom: 15px;">A tela do jogo é dividida entre o <b>Tabuleiro</b> (à esquerda) e o <b>Painel de Controle</b> (à direita).</p>
                <p style="margin-bottom: 15px;"><b>🎲 Como Jogar:</b><br>
                Tudo acontece no painel da direita! Basta o jogador da vez clicar no botão verde <b>"🎲 Girar Dado"</b> para sortear e se mover pelo tabuleiro. A cada jogada, os eventos aparecem na tela para o jogador tomar as decisões.</p>
                <p style="margin-bottom: 15px;"><b>👤 De quem é a vez?</b><br>
                O topo do painel lateral sempre mostra em destaque o nome do jogador da vez. Além disso, na lista de jogadores logo abaixo, o cartão de quem é a vez fica destacado com fundo cinza e borda colorida.</p>
                <p style="margin-bottom: 15px;"><b>📊 Placar das Equipes (Perfil do Jogador):</b><br>
                Você pode <b>clicar em cima do cartão de qualquer equipe</b> na lista lateral a qualquer momento! Isso abrirá um perfil detalhado mostrando a idade aproximada no jogo, o resumo financeiro (renda e contribuições) e todas as conquistas acumuladas.</p>
                <p style="margin-bottom: 15px;"><b>💰 Saldo (A sua Conta Corrente):</b><br>
                Do lado direito do nome de cada jogador, será exibido o símbolo 💰. Ele mostra exatamente o dinheiro vivo que o jogador ou a equipe têm no momento para gastar nos dilemas ou pagar contas.</p>
                <p style="margin-bottom: 15px;"><b>🔄 Renda (+0,00/rod):</b><br>
                Essa é a sua <b>Renda</b>! Mostra quanto dinheiro "cai" na sua conta a cada rodada (giro do dado). Esse valor é calculado assim: <br>
                <i>(Salário Base + Rendas Extras) - (O que você investe na Previdência) = Renda Disponível</i>.<br>
                Atenção: Se você investir muito sem ter salário, essa renda pode ficar negativa!</p>
                <p><b>🏠 A Casa 0:</b><br>
                Todo jogador começa na Casa 0! Ela não existe fisicamente no desenho do tabuleiro. Significa apenas que você está na "Linha de Partida" aguardando o seu primeiro giro de dado.</p>
                </div>
            ''')
        with ui.row().classes('w-full justify-center gap-4 mt-4'):
            ui.button("📖 Manual Completo", on_click=abrir_manual_completo).classes(
                'text-white font-bold py-3 px-6 rounded-lg cursor-pointer').style(
                'background-color: #1976D2 !important;').props('unelevated')
            ui.button("Entendi!", on_click=dialog.close).classes(
                'text-white font-bold py-3 px-6 rounded-lg cursor-pointer').style(
                'background-color: #FF9800 !important;').props('unelevated')
    dialog.open()


# ==========================================
# 🎨 TELAS (COMPONENTES UI GERAIS)
# ==========================================
def renderizar_menu():
    with ui.element('div').classes('w-full min-h-screen bg-[#F5F5F5] relative overflow-hidden'):
        ui.button("Como Começar?", on_click=abrir_como_comecar).classes(
            'absolute top-6 left-6 text-white font-bold rounded-2xl py-2 px-5 z-20 shadow-md cursor-pointer').style(
            'background-color: #1A237E !important;').props('unelevated')

        with ui.column().classes(
                'absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full max-w-[500px] min-h-[620px] items-center p-10 bg-white rounded-3xl shadow-lg border border-gray-200 z-10 mx-4'):

            with ui.row().classes('gap-4 justify-center items-center w-full mb-2'):
                ui.image('/assets/logo_agros.png').classes('h-10 w-24').props('fit="contain"')
                ui.image('/assets/logo_ENEF.png').classes('h-12 w-16').props('fit="contain"')
                ui.image('/assets/logo_abrapp.png').classes('h-8 w-24').props('fit="contain"')
                ui.image('/assets/logo_UniAbrapp.png').classes('h-12 w-12').props('fit="contain"')

            ui.label("O Jogo da Vida").classes('text-3xl font-black text-[#1A237E] mt-2 font-serif')
            ui.label("EDUCAÇÃO FINANCEIRA E PREVIDENCIÁRIA").classes(
                'text-[12px] font-bold text-[#3F51B5] tracking-[0.2em] mb-6 text-center')

            with ui.row().classes('w-full gap-2 items-stretch h-12'):
                inp_nome = ui.input(placeholder="Defina seu nome...").classes(
                    'flex-grow text-lg bg-[#1A237E] text-white font-bold rounded-xl px-4').style(
                    'border: 2px solid #C5CAE9;').props('dark borderless')

                def adicionar_equipe():
                    nome = inp_nome.value.strip()
                    if nome and nome not in estado_jogo["equipes_nomes"]:
                        estado_jogo["equipes_nomes"].append(nome)
                        inp_nome.value = ''
                        atualizar_interface_menu()  # ATUALIZA SÓ A LISTA!

                inp_nome.on('keydown.enter', adicionar_equipe)
                ui.button('+', on_click=adicionar_equipe).classes(
                    'text-white font-black text-2xl rounded-xl w-12 h-full shadow-none cursor-pointer').style(
                    'background-color: #3F51B5 !important;').props('unelevated')

            with ui.scroll_area().classes('w-full flex-grow min-h-[150px] mt-4'):
                # CRIAMOS UM CONTÊINER VAZIO PARA A LISTA
                container_lista = ui.column().classes('w-full gap-3')

            def sortear_ordem():
                nomes = estado_jogo["equipes_nomes"]
                sorteado = sorted([(n, random.randint(1, 6)) for n in nomes], key=lambda x: -x[1])
                estado_jogo["ordem_final"] = [s[0] for s in sorteado]
                estado_jogo["tela_atual"] = "sorteio"
                estado_jogo["instancia_telas"].refresh()

            btn_sortear = ui.button("🎲 Sortear Ordem do Jogo", on_click=sortear_ordem).classes(
                'w-full text-white font-black text-lg py-4 rounded-2xl mt-4 cursor-pointer').style(
                'background-color: #1A237E !important;').props('unelevated')

            # === FUNÇÃO CIRÚRGICA DE ATUALIZAÇÃO ===
            def atualizar_interface_menu():
                container_lista.clear()  # Limpa apenas os nomes
                with container_lista:
                    for i, nome in enumerate(estado_jogo["equipes_nomes"]):
                        cor = CORES_EQUIPES[i % len(CORES_EQUIPES)]
                        with ui.row().classes(
                                'w-full bg-[#FAFAFA] p-3 rounded-xl items-center justify-between shadow-sm border-l-4').style(
                            f'border-color: {cor}'):
                            ui.label(nome).classes('font-bold text-[#1A237E] text-lg font-serif')

                            def remover_equipe(n=nome):
                                estado_jogo["equipes_nomes"].remove(n)
                                atualizar_interface_menu()  # ATUALIZA SÓ A LISTA!

                            ui.button('✕', on_click=remover_equipe).props('flat dense').classes(
                                'text-[#BDBDBD] font-bold text-sm hover:text-red-500 cursor-pointer')

                # Ajusta a cor e bloqueio do botão Sorteio dependendo de quantos nomes tem
                if len(estado_jogo["equipes_nomes"]) < 2:
                    btn_sortear.disable()
                    btn_sortear.style('background-color: #9E9E9E !important; opacity: 0.7;')
                else:
                    btn_sortear.enable()
                    btn_sortear.style('background-color: #1A237E !important; opacity: 1.0;')

            # Roda a função uma primeira vez para desenhar a lista vazia corretamente
            atualizar_interface_menu()

        # A Marisele fica solta no layout da página, sem NUNCA ser recarregada
        ui.image('/assets/Marisela_olho.png').classes(
            'absolute right-0 bottom-0 h-[85vh] w-[450px] z-0 cursor-pointer hover:scale-105 transition-transform duration-300').props(
            'fit="contain" position="100% 100%"').on('click', abrir_sobre_marisele)


def renderizar_sorteio():
    with ui.row().classes('w-full min-h-screen bg-[#F5F5F5] items-center justify-center p-4 m-0'):
        with ui.column().classes(
                'w-full max-w-[500px] max-h-[90vh] items-center p-6 bg-white rounded-3xl shadow-lg border border-gray-200'):
            ui.label("Ordem definida!").classes('text-[26px] font-black text-[#1A237E] font-serif mb-2')
            with ui.scroll_area().classes('w-full max-h-[220px] pr-2'):
                with ui.column().classes('w-full gap-2'):
                    medalhas = ["🥇", "🥈", "🥉"] + [f"{i + 1}º" for i in range(3, len(estado_jogo["ordem_final"]))]
                    for i, nome in enumerate(estado_jogo["ordem_final"]):
                        cor = CORES_EQUIPES[i % len(CORES_EQUIPES)]
                        fundo = '#F5F5F5' if i == 0 else '#FAFAFA'
                        with ui.row().classes('w-full p-3 rounded-xl items-center gap-4 border-l-4').style(
                                f'background-color: {fundo}; border-color: {cor}'):
                            ui.label(medalhas[i]).classes('text-2xl font-bold text-[#555]')
                            ui.label(nome).classes('font-bold text-[#555] text-[15px]')

            ui.label("⚙️ Escolha a Dinâmica do Jogo:").classes('font-black text-[#555] text-[14px] mt-4 mb-2')
            with ui.row().classes('w-full justify-center gap-3'):
                def set_modo(turbo):
                    estado_jogo["modo_turbo"] = turbo
                    estado_jogo["instancia_telas"].refresh()

                turbo_ativo = estado_jogo["modo_turbo"]
                cor_c_bg = '#1976D2' if not turbo_ativo else '#EEEEEE'
                cor_c_txt = 'white' if not turbo_ativo else '#9E9E9E'
                cor_t_bg = '#FF8F00' if turbo_ativo else '#EEEEEE'
                cor_t_txt = 'white' if turbo_ativo else '#9E9E9E'
                ui.button("🎲 MODO CLÁSSICO\n(DADO 1 A 6)", on_click=lambda: set_modo(False)).classes(
                    'rounded-xl font-black text-center py-2 flex-1 cursor-pointer').style(
                    f'background-color: {cor_c_bg} !important; color: {cor_c_txt} !important;').props('unelevated')
                ui.button("🚀 MODO TURBO\n(DADO 1 A 9)", on_click=lambda: set_modo(True)).classes(
                    'rounded-xl font-black text-center py-2 flex-1 cursor-pointer').style(
                    f'background-color: {cor_t_bg} !important; color: {cor_t_txt} !important;').props('unelevated')

            desc_texto = "O tempo voa! Partidas mais curtas, pulos longos e uma jornada bem mais rápida!" if turbo_ativo else "Um jogo cadenciado. Caminhe passo a passo e viva mais eventos do tabuleiro."
            ui.label(desc_texto).classes('text-[#757575] text-[12px] text-center italic mt-2')

            def iniciar_jogo_real():
                estado_jogo["equipes"] = [{
                    "nome": n, "saldo": SALDO_INICIAL, "posicao": 0, "formado": False,
                    "salario_base": 0, "renda_extra": 0, "investimento_turno": 0, "qtd_livros": 0,
                    "tem_mesada_vo": False, "emojis": "", "marcos_passados": [], "historico_escolhas": []
                } for n in estado_jogo["ordem_final"]]
                estado_jogo["turno_atual"] = 0
                estado_jogo["fila_eventos"] = []
                estado_jogo["formados"] = []
                estado_jogo["aguardando"] = False

                estado_jogo["tela_atual"] = "regras"
                estado_jogo["instancia_telas"].refresh()

            ui.button("🚀 VER REGRAS DO JOGO!", on_click=iniciar_jogo_real).classes(
                'w-full text-white font-black text-[16px] py-4 rounded-2xl mt-4 cursor-pointer').style(
                'background-color: #1A237E !important;').props('unelevated')


def renderizar_regras():
    with ui.element('div').classes('w-full min-h-screen bg-[#F5F5F5] relative overflow-hidden'):
        ui.image('/assets/Marisela_pensar.png').classes(
            'absolute left-0 bottom-0 h-[85vh] w-[400px] z-0 cursor-pointer hover:scale-105 transition-transform duration-300').props(
            'fit="contain" position="0% 100%"').on('click', abrir_sobre_marisele)
        with ui.column().classes(
                'absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full max-w-[850px] p-10 bg-white rounded-3xl shadow-lg border border-gray-200 z-10 mx-4'):
            with ui.row().classes('w-full items-center justify-between mb-6'):
                ui.label("📜 Como Funciona o Jogo?").classes('text-[28px] font-black text-[#1A237E] font-serif')
                ui.button("Manual Completo", on_click=abrir_manual_completo).classes(
                    'text-white font-bold py-2 px-5 rounded-xl cursor-pointer').style(
                    'background-color: #FF9800 !important;').props('unelevated')

            with ui.scroll_area().classes('w-full h-[40vh] pr-4'):
                ui.html('''
                    <div style='font-size: 16px; color: #333; line-height: 1.6;'>
                        <p>O <b>Jogo da Vida</b> simula a jornada financeira dos 16 aos 65 anos. O objetivo é simular escolhas no decorrer da vida e pensar em atitudes na vida real que possam contribuir para chegar à aposentadoria com o maior patrimônio possível!</p>
                        <p class="mt-4"><b>🧭 O Básico para Começar:</b></p>
                        <ul style='margin-top: 0; margin-bottom: 15px;'>
                            <li style='margin-bottom: 8px;'>Cada jogador inicia a partida com <b>R$ 1.621,00</b>.</li>
                            <li style='margin-bottom: 8px;'>Ao longo do tabuleiro, enfrentará dilemas financeiros. Seja sincero: <b>o que você faria na vida real?</b></li>
                            <li style='margin-bottom: 8px;'>Fique atento às <b>Casas Especiais (!)</b>: Elas representam <b>Marcos de Vida</b> aos 16, 20, 30 e 45 anos, momentos fundamentais para investir na Previdência Complementar e na Educação.</li>
                        </ul>
                        <div style='background: #E3F2FD; border-left: 5px solid #1976D2; padding: 12px; margin-bottom: 15px; border-radius: 5px;'>
                        <p style='color: #1A237E; margin: 0;'><b>📊 Acompanhe seu Progresso:</b></p>
                        <p style='color: #333; margin: 5px 0 0 0;'>
                        A qualquer momento, <b>clique no cartão da sua equipe</b> no painel à direita! Isso abrirá o seu Perfil detalhado, onde você pode acompanhar exatamente a sua Renda Bruta, quanto está contribuindo para a Previdência por rodada, sua situação profissional e todas as suas conquistas.
                        </p>
                        </div>
                        <p><b>⭐ Os Emojis e as Regras:</b><br>
                        Suas escolhas rendem Emojis no seu placar. Eles representam a evolução da sua vida financeira e trazem benefícios reais para a sua partida:
                        </p>
                        <ul style='margin-top: 0; margin-bottom: 15px;'>
                            <li style='margin-bottom: 5px;'>🏦 <b>Previdência:</b> Faz seu dinheiro render juros compostos de 1% ao mês até o fim do jogo.</li>
                            <li style='margin-bottom: 5px;'>📚 <b>Educação:</b> Quanto mais livros juntar na juventude, maior será o seu salário inicial ao se formar!</li>
                            <li style='margin-bottom: 5px;'>👵 <b>Vovó:</b> Garante uma mesada extra de <b>R$ 200,00/rodada</b> (mas acaba quando você conseguir um emprego).</li>
                            <li style='margin-bottom: 5px;'>🌾🧬💻🎭 <b>Faculdade:</b> O caminho que você escolher na faculdade não vai afetar seu salário e não altera nada. Serve apenas para personalizar sua jornada!</li>
                            <li style='margin-bottom: 5px;'>💼 <b>Mercado de Trabalho:</b> Você se formou! Agora sua renda aumenta e você ganha seu salário a cada rodada.</li>
                            <li style='margin-bottom: 5px;'>📈/🎓 <b>Capacitação e Pós-Graduação:</b> Aumentam o seu salário base permanentemente!</li>
                        </ul>
                        <div style='background: #FFEBEE; border-left: 5px solid #D32F2F; padding: 12px; margin-top: 15px; border-radius: 5px;'>
                        <p style='color: #C62828; font-weight: bold; margin: 0;'>🚨 REGRA DE OURO:</p>
                        <p style='color: #D32F2F; margin: 5px 0 0 0;'>
                        Cuidado com os excessos! Quem terminar o jogo com a Conta Corrente no vermelho <b>perde todos os investimentos</b> para pagar as dívidas e é desclassificado da partida.
                        </p>
                        </div>
                    </div>
                ''')

            def iniciar_tabuleiro():
                estado_jogo["tela_atual"] = "jogo"
                estado_jogo["instancia_telas"].refresh()

            ui.button("Entendi, vamos para o Tabuleiro! 🚀", on_click=iniciar_tabuleiro).classes(
                'text-white font-black text-[18px] py-4 px-8 rounded-xl mt-6 self-center cursor-pointer').style(
                'background-color: #43A047 !important;').props('unelevated')


@ui.refreshable
def ui_tabuleiro():
    with ui.element('div').classes('flex-grow relative bg-[#ECEFF1] overflow-hidden h-full z-0'):
        ui.html(gerar_svg_caminho()).classes('absolute top-0 left-0 w-full h-full pointer-events-none z-0')

        for num in range(1, 41):
            x_pct, y_pct = obter_pos_pct(num)
            cor = cor_da_casa(num)
            texto = obter_texto_casa(num)
            with ui.element('div').classes(
                    'absolute flex items-center justify-center text-center text-white font-black cursor-pointer') \
                    .style(
                f'left: {x_pct}%; top: {y_pct}%; transform: translate(-50%, -50%); width: 52px; height: 52px; background-color: {cor}; border: 3px solid white; border-radius: 11px; box-shadow: 2px 3px 6px rgba(0,0,0,0.3); z-index: 10; transition: transform 0.2s;') \
                    .on('click', lambda _, n=num: abrir_sandbox(n)):
                ui.html(texto.replace('\n', '<br>')).style(
                    f"font-size: {'13px' if '\n' in texto else '18px'}; line-height: 1.1;")

        grupos = {}
        for i, eq in enumerate(estado_jogo["equipes"]):
            if eq["posicao"] > 0:
                grupos.setdefault(eq["posicao"], []).append(i)

        for pos, indices in grupos.items():
            x_pct, y_pct = obter_pos_pct(pos)
            n = len(indices)
            for j, eq_idx in enumerate(indices):
                eq = estado_jogo["equipes"][eq_idx]
                offset_x = (j - (n - 1) / 2) * 20
                cor_eq = CORES_EQUIPES[eq_idx % len(CORES_EQUIPES)]
                with ui.element('div').classes(
                        'absolute flex flex-col items-center pointer-events-none z-20 transition-all duration-700 ease-out') \
                        .style(
                    f'left: calc({x_pct}% + {offset_x}px); top: calc({y_pct}% - 40px); transform: translate(-50%, -50%);'):
                    ui.label(eq['nome']).classes(
                        'bg-white/90 px-2 py-0.5 rounded text-[10px] font-bold text-gray-800 mb-1 shadow-sm whitespace-nowrap')
                    ui.element('div').classes('w-4 h-4 rounded-full border-2 border-white shadow-md').style(
                        f'background-color: {cor_eq};')

        # A FUNÇÃO ACABA AQUI! Nenhuma ui.image ou logo deve existir abaixo desta linha nesta função.
@ui.refreshable
def ui_painel_lateral():
    with ui.column().classes(
            'w-[280px] min-w-[280px] h-full bg-[#FAFAFA] border-l-2 border-[#E0E0E0] flex flex-col flex-shrink-0 m-0 p-0'):

        with ui.column().classes('w-full p-4 pb-0'):
            eq_vez = estado_jogo["equipes"][estado_jogo["turno_atual"]]
            cor_vez = CORES_EQUIPES[estado_jogo["turno_atual"] % len(CORES_EQUIPES)]

            with ui.column().classes('w-full bg-[#212121] rounded-2xl p-3 items-center shadow-md'):
                ui.label("VEZ DE JOGAR").classes('text-[10px] font-black text-[#616161] tracking-widest')
                ui.label(eq_vez["nome"]).classes('text-[18px] font-black text-white text-center truncate w-full')
                ui.element('div').classes('w-full h-1 mt-1 rounded-sm').style(f'background-color: {cor_vez};')

            ui.label("PLACAR DAS EQUIPES").classes('text-[11px] font-black text-[#999] tracking-wider mt-4')

        with ui.scroll_area().classes('w-full flex-grow px-4 mt-2'):
            with ui.column().classes('w-full gap-2 pb-4'):
                for i, eq in enumerate(estado_jogo["equipes"]):
                    cor_eq = CORES_EQUIPES[i % len(CORES_EQUIPES)]
                    is_ativo = (i == estado_jogo["turno_atual"])
                    bg_card = '#F5F5F5' if is_ativo else 'white'
                    border_card = '#E0E0E0' if is_ativo else '#F0F0F0'

                    renda_liquida = eq["salario_base"] + eq.get("renda_extra", 0) - eq["investimento_turno"]
                    sinal_r = "+" if renda_liquida > 0 else ("-" if renda_liquida < 0 else "")
                    cor_r = "#1976D2" if renda_liquida > 0 else ("#D32F2F" if renda_liquida < 0 else "#999999")
                    cor_s = "#2E7D32" if eq["saldo"] >= 0 else "#C62828"

                    with ui.column().classes(
                            'w-full p-3 rounded-xl cursor-pointer transition-colors hover:bg-[#FFF3E0] border-l-[5px]').style(
                            f'background-color: {bg_card}; border-color: {cor_eq}; border-top: 1px solid {border_card}; border-right: 1px solid {border_card}; border-bottom: 1px solid {border_card};') \
                            .on('click', lambda idx=i: abrir_status_equipe(idx)):
                        with ui.row().classes('w-full justify-between items-center'):
                            ui.label(f"{eq['nome']} {agrupar_emojis(eq.get('emojis', ''))}").classes(
                                f'text-[14px] {"font-black" if is_ativo else "font-bold"} truncate').style(
                                f'color: {cor_eq}; max-width: 140px;')
                            ui.label(f"Casa {eq['posicao']}").classes('text-[11px] text-[#999]')

                        with ui.row().classes('w-full justify-between items-end mt-1'):
                            ui.label(f"💰 {fmt_saldo(eq['saldo'])}").classes(
                                'text-[14px] font-black leading-none').style(f'color: {cor_s};')
                            ui.label(f"(Renda: {sinal_r}{abs(renda_liquida)},00/rod)").classes(
                                'text-[11px] font-bold leading-none mb-[2px]').style(f'color: {cor_r};')

        with ui.column().classes('w-full p-4 bg-[#FAFAFA] border-t border-[#E0E0E0] mt-auto gap-2'):
            btn_dado_ui = ui.button("🎲 Girar Dado", on_click=abrir_giro).classes(
                'w-full text-white font-black text-lg rounded-xl shadow-md cursor-pointer min-h-[50px]').style(
                'background-color: #43A047 !important;').props('unelevated')

            if estado_jogo["aguardando"] or eq_vez.get("formado"):
                btn_dado_ui.disable()
                btn_dado_ui.style('background-color: #9E9E9E !important; opacity: 0.7;')
                btn_dado_ui.text = "⏳ Aguardando..."

            # Este é o ÚNICO botão de reiniciar que deve existir aqui:
            ui.button("↩ Reiniciar Jogo", on_click=confirmar_reinicio).classes(
                'w-full bg-white text-[#BDBDBD] font-bold border-2 border-[#E0E0E0] py-2 rounded-lg cursor-pointer hover:bg-red-50 hover:text-red-500 hover:border-red-200 transition-colors').props(
                'unelevated flat')

            def resetar():
                reiniciar_jogo_completo()


def confirmar_reinicio():
    with ui.dialog() as dialog, ui.card().classes(
            'w-[360px] p-6 bg-white rounded-2xl flex flex-col items-center shadow-2xl border border-gray-200'):
        ui.label("⚠️ Reiniciar Jogo").classes('text-xl font-black text-[#1A237E] mb-2')
        ui.label("Tem certeza que deseja reiniciar?").classes('text-[15px] font-bold text-[#333] text-center mb-6')

        with ui.row().classes('w-full gap-3 justify-center'):
            ui.button("Não", on_click=dialog.close).classes(
                'flex-1 bg-gray-200 text-gray-700 font-bold py-3 rounded-xl cursor-pointer hover:bg-gray-300 transition-colors').props(
                'unelevated')

            def sim_reiniciar():
                dialog.close()
                # 1. Executa a limpeza completa que você já tem
                reiniciar_jogo_completo()

                # 2. Fecha eventuais diálogos abertos na tela (como o de status ou modal de casa)
                # (Se você tiver uma variável global para diálogos, pode fechar aqui, senão o estado 'menu' já resolve)

                # 3. Força o redesenho global das telas para cair na tela "menu"
                estado_jogo["instancia_telas"].refresh()

            ui.button("Sim", on_click=sim_reiniciar).classes(
                'flex-1 bg-[#D32F2F] text-white font-bold py-3 rounded-xl cursor-pointer hover:bg-red-700 transition-colors').props(
                'unelevated')

    dialog.open()

def renderizar_jogo():
    """Tela 4: Layout Principal"""
    with ui.column().classes('w-full min-h-screen bg-[#ECEFF1] p-0 m-0 flex-nowrap overflow-hidden'):
        # DIALOG DADO GLOBAL E SEGURO (Alinhamento corrigido)
        with ui.dialog().props('persistent') as dialog_dado:
            with ui.card().classes(
                    'w-[340px] min-h-[330px] rounded-[24px] border-4 border-[#3F51B5] items-center justify-center p-6 flex flex-col gap-2').style(
                    'background-color: #1A237E !important;'):
                ui_refs['lbl_dado_sub'] = ui.label("DADO").classes(
                    'text-[11px] font-black text-[#7986CB] tracking-widest text-center w-full')
                ui_refs['lbl_dado_eq'] = ui.label("").classes(
                    'text-[18px] font-bold text-[#C5CAE9] text-center w-full mt-1')

                # Forçamos o dado a ficar sozinho no meio ocupando toda a linha
                ui_refs['lbl_dado_num'] = ui.label("?").classes(
                    'text-[100px] font-black my-4 font-serif leading-none text-center w-full')

                ui_refs['lbl_dado_msg'] = ui.label("girando...").classes(
                    'text-[16px] font-bold text-[#9FA8DA] text-center w-full')

                # Botão com visibilidade controlada nativamente (evita bugar o layout)
                ui_refs['btn_dado_avancar'] = ui.button("Avançar →").classes(
                    'text-white font-black py-3 px-8 rounded-xl mt-4 cursor-pointer').style(
                    'background-color: #3F51B5 !important;').props('unelevated')
                ui_refs['btn_dado_avancar'].set_visibility(False)

                ui_refs['dialog_dado'] = dialog_dado

                def ao_avancar(e=None):
                    dialog_dado.close()
                    ui_refs['btn_dado_avancar'].set_visibility(False)

                    passos = estado_jogo.get("passos_atuais", 1)
                    ui.timer(0.2, lambda p=passos: aplicar_movimento(p), once=True)

                ui_refs['btn_dado_avancar'].on_click(ao_avancar)

        with ui.row().classes(
                'w-full h-[50px] bg-[#212121] items-center justify-between px-6 shadow-md z-30 flex-shrink-0 m-0'):
            ui.label("O JOGO DA VIDA  ·  EDUCAÇÃO FINANCEIRA E PREVIDENCIÁRIA").classes(
                'text-white font-black text-[13px] tracking-widest')
            ui.button("Como Funciona o Tabuleiro?", on_click=abrir_ajuda_tabuleiro).classes(
                'text-white font-bold px-4 py-1 rounded-lg text-[13px] cursor-pointer').style(
                'background-color: #FF9800 !important;').props('unelevated')

        with ui.row().classes('w-full flex-grow flex-nowrap p-0 m-0 overflow-hidden relative').style(
                'height: calc(100vh - 50px);'):
            # Guarda a instância única do tabuleiro desta aba
            estado_jogo["instancia_tabuleiro"] = ui_tabuleiro()

            ui.image('/assets/Marisela_binoculo.png').classes(
                'absolute left-0 bottom-0 h-[26vh] max-w-[220px] z-40 cursor-pointer hover:scale-105 transition-transform duration-300').props(
                'fit="contain" position="0% 100%"').on('click', abrir_sobre_marisele)

            with ui.row().classes('absolute bottom-8 gap-4 z-10 pointer-events-none items-center').style(
                    'right: calc(280px + 2rem);'):
                ui.image('/assets/logo_agros.png').classes('h-10 w-24').props('fit="contain"')
                ui.image('/assets/logo_ENEF.png').classes('h-10 w-16').props('fit="contain"')
                ui.image('/assets/logo_abrapp.png').classes('h-8 w-24').props('fit="contain"')
                ui.image('/assets/logo_UniAbrapp.png').classes('h-10 w-10').props('fit="contain"')

            ui_painel_lateral()


# ==========================================
# 🏆 FASE FINAL: RANKING E JUROS COMPOSTOS
# ==========================================
def calcular_ranking_final():
    """Reproduz a matemática exata de juros compostos do PyQt6 para todas as equipes."""
    for e in estado_jogo["equipes"]:
        a16 = e.get("aporte_16", 0)
        a20 = e.get("aporte_20", a16)
        a30 = e.get("aporte_30", a20)
        a45 = e.get("aporte_45", a30)

        saldo_prev = 0
        hist = [0]
        bolso = 0

        # Verifica os aportes únicos e mapeia para o mês exato
        aportes_extras = {}
        for au in e.get("aportes_unicos", []):
            if au["casa"] == 30:
                mes_exato = 348  # (30 anos -> 45 anos reais = 348 meses)
            else:
                mes_exato = int((au["casa"] / 40.0) * 588)

            if mes_exato >= 588: mes_exato = 587
            aportes_extras[mes_exato] = aportes_extras.get(mes_exato, 0) + au["valor"]

        # Loop de 588 meses (dos 16 aos 65 anos) a 1% ao mês
        for mes in range(588):
            if mes < 48:
                pmt = a16  # 16 aos 20
            elif mes < 168:
                pmt = a20  # 20 aos 30
            elif mes < 348:
                pmt = a30  # 30 aos 45
            else:
                pmt = a45  # 45 aos 65

            saldo_prev = saldo_prev * 1.01 + pmt
            bolso += pmt

            if mes in aportes_extras:
                valor_extra = aportes_extras[mes]
                saldo_prev += valor_extra
                bolso += valor_extra

            hist.append(saldo_prev)

        e["prev_hist"] = hist
        e["prev_bolso"] = bolso
        e["prev_juros"] = saldo_prev - bolso

        # Relatório de contribuições para a UI
        txt_hist = f"&nbsp;&nbsp;• <b>Dos 16 aos 20 anos:</b> R$ {a16},00/mês<br>&nbsp;&nbsp;• <b>Dos 20 aos 30 anos:</b> R$ {a20},00/mês<br>&nbsp;&nbsp;• <b>Dos 30 aos 45 anos:</b> R$ {a30},00/mês<br>&nbsp;&nbsp;• <b>Dos 45 aos 65 anos:</b> R$ {a45},00/mês"
        if e.get("aportes_unicos"):
            txt_hist += "<br>&nbsp;&nbsp;• <b style='color:#1976D2;'>Aportes Únicos Extras:</b> "
            txt_hist += ", ".join([f"{fmt_saldo(au['valor'])} (Casa {au['casa']})" for au in e["aportes_unicos"]])
        e["historico_aportes_txt"] = txt_hist

        # A regra de Ouro: Se fechar negativo, perde TUDO!
        if e["saldo"] < 0:
            e["patrimonio_total"] = e["saldo"]
        else:
            e["patrimonio_total"] = e["saldo"] + saldo_prev

    # Separando os ganhadores dos desclassificados
    positivos = [e for e in estado_jogo["equipes"] if e["saldo"] >= 0]
    negativados = [e for e in estado_jogo["equipes"] if e["saldo"] < 0]

    positivos.sort(key=lambda e: -e["patrimonio_total"])
    negativados.sort(key=lambda e: -e["patrimonio_total"])
    estado_jogo["ranking"] = positivos + negativados


def mudar_view_ranking(novo_idx):
    estado_jogo["ranking_view_idx"] = novo_idx
    estado_jogo["instancia_telas"].refresh()


def ir_para_classificacao_geral():
    estado_jogo["tela_atual"] = "resumo"
    estado_jogo["instancia_telas"].refresh()


def renderizar_ranking():
    ranking = estado_jogo["ranking"]
    idx = estado_jogo.get("ranking_view_idx", len(ranking) - 1)
    eq = ranking[idx]
    pos = idx + 1

    with ui.element('div').classes('w-full min-h-screen bg-[#F5F5F5] flex items-center justify-center p-4 m-0'):

        with ui.card().classes(
                'w-full max-w-[1300px] bg-[#FAFAFA] rounded-[24px] p-0 flex flex-row shadow-2xl h-[90vh] max-h-[720px] min-h-[550px] border-4 border-white overflow-hidden'):

            # ==========================================
            # PAINEL DA ESQUERDA (DADOS DA EQUIPE)
            # ==========================================
            with ui.column().classes('w-[420px] bg-white h-full p-6 flex flex-col border-r-2 border-gray-200'):

                with ui.column().classes('w-full flex-grow gap-1 overflow-hidden'):
                    if eq["saldo"] < 0:
                        ui.label("❌ FORA DO RANKING").classes('text-[18px] font-black text-[#D32F2F]')
                    elif pos == 1:
                        ui.label("🏆 1º LUGAR - GRANDE CAMPEÃO!").classes('text-[20px] font-black text-[#FBC02D]')
                    else:
                        ui.label(f"{pos}º LUGAR").classes('text-[18px] font-black text-[#757575]')

                    with ui.row().classes('w-full items-center gap-2 flex-wrap mt-1'):
                        ui.label(eq['nome']).classes('text-[30px] font-black text-[#1A237E] font-serif leading-none')
                        ui.html(
                            f"<div style='font-size: 22px; display: inline-flex; align-items: center; gap: 4px;'>{agrupar_emojis_html(eq.get('emojis', ''), '14px')}</div>")

                    with ui.scroll_area().classes('w-full h-full mt-2 pr-2'):
                        if eq["saldo"] < 0:
                            ui.html(f"""
                                <span style='color: #D32F2F; font-size: 20px; font-weight: bold;'>🚨 DESCLASSIFICADO!</span><br><br>
                                <span style='font-size: 14px; color: #333;'>A equipe terminou com a <b>Conta Corrente no Vermelho</b>.<br>
                                Todos os investimentos precisaram ser liquidados para pagar dívidas!</span><br><br>
                                <b style='font-size: 15px; color: #333;'>Saldo da Conta:</b> <span style='font-size: 15px; color: #D32F2F;'>{fmt_saldo(eq['saldo'])}</span><br>
                                <b style='font-size: 15px; color: #333;'>Patrimônio Bruto:</b> <span style='font-size: 15px; color: #333;'>R$ 0,00</span>
                            """)
                        else:
                            ui.html(f"""
                                <div style='font-size: 14px; color: #333; line-height: 1.5;'>
                                <b>💰 Saldo Conta Corrente:</b> {fmt_saldo(eq['saldo'])}<br><br>
                                <b>📊 Histórico de Contribuições:</b><br>
                                <span style='color: #555; font-size: 13px;'>{eq['historico_aportes_txt']}</span><br><br>
                                <b>📥 Total Tirado do Bolso:</b> {fmt_saldo(eq['prev_bolso'])}<br>
                                <b>📈 Juros Compostos Ganhos:</b> <span style='color:#43A047; font-weight: 900;'>{fmt_saldo(eq['prev_juros'])}</span><br><br>
                                <div style='background: #E8F5E9; padding: 10px; border-radius: 8px; border-left: 4px solid #43A047; margin-top: 5px;'>
                                    <span style='font-size: 13px; color: #2E7D32; font-weight: bold;'>👑 PATRIMÔNIO BRUTO:</span><br>
                                    <span style='font-size: 20px; color: #1A237E; font-weight: 950;'>{fmt_saldo(eq['patrimonio_total'])}</span>
                                </div>
                                </div>
                            """)

                # BOTÕES DE NAVEGAÇÃO
                with ui.column().classes('w-full pt-4 mt-2 border-t border-gray-200 shrink-0'):
                    with ui.row().classes('w-full justify-between items-center gap-2'):
                        btn_voltar = ui.button("⬅️ VOLTAR", on_click=lambda: mudar_view_ranking(idx + 1)).classes(
                            'flex-1 h-[50px] rounded-xl bg-gray-200 text-gray-700 font-black text-[12px] md:text-[13px] leading-tight p-0 m-0 shadow-sm').props(
                            'unelevated')
                        if idx >= len(ranking) - 1: btn_voltar.disable()

                        if pos == 1 or idx == 0:
                            ui.button("CLASSIFICAÇÃO GERAL 🏆", on_click=lambda: ir_para_classificacao_geral()).classes(
                                'flex-1 h-[50px] rounded-xl bg-[#2E7D32] text-white font-black text-[12px] md:text-[13px] leading-tight p-0 m-0 shadow-md').props(
                                'unelevated')
                        else:
                            ui.button("AVANÇAR ➡️", on_click=lambda: mudar_view_ranking(idx - 1)).classes(
                                'flex-1 h-[50px] rounded-xl bg-[#1976D2] text-white font-black text-[12px] md:text-[13px] leading-tight p-0 m-0 shadow-md').props(
                                'unelevated')

            # ==========================================
            # PAINEL DA DIREITA (GRÁFICO E HISTÓRICO)
            # ==========================================
            with ui.column().classes('flex-grow h-full p-0 m-0 bg-white'):
                with ui.tabs().classes('w-full bg-[#3F51B5] text-white font-bold m-0 p-0 shadow-sm shrink-0') as tabs:
                    tab_grafico = ui.tab('📊 Gráfico de Evolução').classes('py-3 text-[14px]')
                    tab_historico = ui.tab('📜 Histórico de Escolhas').classes('py-3 text-[14px]')

                with ui.tab_panels(tabs, value=tab_grafico).classes('w-full flex-grow bg-white p-4 relative'):

                    with ui.tab_panel(tab_grafico).classes(
                            'p-0 m-0 absolute inset-0 w-full h-full flex flex-col justify-center items-center bg-white'):
                        if eq["saldo"] < 0:
                            ui.image('/assets/Marisela_triste.png').classes(
                                'w-full h-full max-h-[80%] max-w-[80%] opacity-90').props('fit="contain"')
                        else:
                            # === GRÁFICO COM FUNDO BRANCO FORÇADO ===
                            ui.echart({
                                'backgroundColor': '#FFFFFF',  # <--- ISSO GARANTE O FUNDO BRANCO NO GRÁFICO
                                'tooltip': {
                                    'trigger': 'axis',
                                    'formatter': 'Idade: {b} anos<br/><b>Patrimônio: R$ {c}</b>'
                                },
                                'grid': {'top': 30, 'bottom': 40, 'left': 100, 'right': 30},
                                'xAxis': {
                                    'type': 'category',
                                    'data': [str(16 + (m // 12)) for m in range(588)],
                                    'name': 'Anos de Vida',
                                    'axisLabel': {'interval': 59}
                                },
                                'yAxis': {
                                    'type': 'value',
                                    'name': 'Montante (R$)',
                                    'axisLabel': {
                                        'formatter': 'R$ {value}'
                                    }
                                },
                                'series': [{
                                    'data': [round(v, 2) for v in eq.get('prev_hist', [])],
                                    'type': 'line',
                                    'color': '#4CAF50',
                                    'showSymbol': False,
                                    'smooth': True,
                                    'areaStyle': {'color': 'rgba(76, 175, 80, 0.2)'}
                                }]
                            }).classes('w-full h-full min-h-[400px] bg-white')  # <-- Adicionei bg-white aqui também

                    with ui.tab_panel(tab_historico).classes('p-0 m-0 absolute inset-0 w-full h-full bg-white'):
                        with ui.scroll_area().classes('w-full h-full bg-white rounded-xl p-4 border border-gray-200'):
                            hist_html = "<div style='font-family: Arial; font-size: 14px; color: #333; line-height: 1.5;'>"
                            for item in eq.get("historico_escolhas", []):
                                casa = item["casa"]
                                texto_escolha = item["texto"].replace("\n", " ")
                                saldo_impacto = item["saldo"]
                                invest_set = item.get("invest")

                                impacto_str = ""
                                if saldo_impacto < 0:
                                    impacto_str += f"<span style='color: #C62828; font-weight: bold;'> (Gastou {fmt_saldo(abs(saldo_impacto))})</span>"
                                elif saldo_impacto > 0:
                                    impacto_str += f"<span style='color: #2E7D32; font-weight: bold;'> (Ganhou {fmt_saldo(saldo_impacto)})</span>"

                                if invest_set is not None:
                                    impacto_str += f"<br><span style='color: #1976D2; font-size: 13px;'> ↳ Contribuição Mensal Reajustada: {fmt_saldo(invest_set)}</span>"

                                hist_html += f"<p style='margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #EEE;'><b style='color:#1A237E;'>🏠 Casa {casa}:</b> {texto_escolha}{impacto_str}</p>"
                            hist_html += "</div>"
                            ui.html(hist_html)


def renderizar_resumo():
    with ui.element('div').classes('w-full min-h-screen bg-[#F5F5F5] flex items-center justify-center p-8'):
        # Ajustei o max-w para 700px para acomodar bem os dois botões lado a lado
        with ui.card().classes('w-full max-w-[700px] bg-white rounded-[20px] p-10 shadow-lg border border-gray-200'):
            ui.label("🏆 Classificação Geral Final").classes(
                'text-[28px] font-black text-[#1A237E] font-serif w-full text-center mb-6')

            with ui.column().classes('w-full gap-3'):
                medalhas = ["🥇", "🥈", "🥉"] + [f"{i + 1}º" for i in range(3, len(estado_jogo["ranking"]))]
                for i, eq in enumerate(estado_jogo["ranking"]):
                    cor = CORES_EQUIPES[estado_jogo["equipes_nomes"].index(eq["nome"]) % len(CORES_EQUIPES)]

                    with ui.row().classes(
                            f'w-full bg-[#FAFAFA] p-4 rounded-xl border-l-[5px] items-center justify-between shadow-sm').style(
                            f'border-color: {cor};'):
                        with ui.row().classes('items-center gap-4'):
                            ui.label(medalhas[i]).classes('text-[22px] font-bold')
                            ui.label(f"{eq['nome']} {agrupar_emojis(eq.get('emojis', ''))}").classes(
                                'text-[16px] font-bold text-[#1A237E]')

                        if eq["saldo"] < 0:
                            ui.html("<span style='color: #D32F2F; font-weight: bold;'>🚨 DESCLASSIFICADO</span>")
                        else:
                            ui.html(
                                f"<span style='color: #2E7D32; font-weight: 900; font-size: 18px;'>{fmt_saldo(eq['patrimonio_total'])}</span>")

            # ==========================================
            # NOVOS BOTÕES DIVIDIDOS LADO A LADO
            # ==========================================
            with ui.row().classes('w-full mt-8 gap-4 flex-nowrap'):
                def voltar_para_ranking():
                    estado_jogo["tela_atual"] = "ranking"
                    estado_jogo["instancia_telas"].refresh()

                ui.button("⬅️ Voltar aos Gráficos", on_click=voltar_para_ranking).classes(
                    'flex-1 bg-[#E0E0E0] text-[#424242] font-black py-4 rounded-xl cursor-pointer hover:bg-[#D6D6D6] transition-colors shadow-sm').props(
                    'unelevated')

                ui.button("Finalizar Jogo 🏠", on_click=lambda: reiniciar_jogo_completo()).classes(
                    'flex-1 bg-[#1A237E] text-white font-black py-4 rounded-xl cursor-pointer hover:bg-[#283593] transition-colors shadow-md').props(
                    'unelevated')


# ==========================================
# 🔄 MOTOR DE RENDERIZAÇÃO SPA E ROTAS
# ==========================================
@ui.refreshable
def renderizar_telas():
    tela = estado_jogo["tela_atual"]
    if tela == "menu":
        renderizar_menu()
    elif tela == "sorteio":
        renderizar_sorteio()
    elif tela == "regras":
        renderizar_regras()
    elif tela == "jogo":
        renderizar_jogo()
    elif tela == "ranking":
        renderizar_ranking()
    elif tela == "resumo":
        renderizar_resumo()


@ui.page('/')
def index():
    ui.add_head_html('''
        <style>
            body, html { margin: 0; padding: 0; background-color: #F5F5F5; overflow-x: hidden; height: 100vh; }
            .nicegui-content { padding: 0 !important; margin: 0 !important; max-width: 100% !important; height: 100vh !important; display: flex; flex-direction: column; }
        </style>
    ''')
    estado_jogo["instancia_telas"] = renderizar_telas()


ui.run(
    title="Jogo da Vida",
    favicon="🎲",
    port=int(os.environ.get('PORT', 8080)),
    host='0.0.0.0',
    storage_secret='agros_segredo_super_secreto_2026',
    dark=False
)