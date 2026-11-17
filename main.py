import random
import pygame

TELA_LARGURA = 1280
TELA_ALTURA = 720
COMPRIMENTO_PISTA = 100
QTD_RETANGULO = [5, 10, 25, 50, 100, 250, 500]
METODOS = [('Esquerda', 0), ('Ponto médio', 0.5), ('Direita', 1)]

FUNDO = (30, 30, 30)
PAINEL = (45, 45, 45)
BORDA = (100, 100, 100)
CLARO = (255, 255, 255)
CINZA_CLARO = (200, 200, 200)
CIANO = (0, 200, 255)
AMARELO = "#F5B427"
VERDE = "#63914A"
MAPA = pygame.Rect(20, 76, 820, 474)


def f(x):
    return 8 + x ** 2 / 500


def F(x):
    return 8 * x + x ** 3 / 1500


def calcular_area_exata(a, b):
    return F(b) - F(a)


def calcular_retangulos(a, b, quantidade, metodo):
    largura = (b - a) / quantidade
    retangulos = []

    for i in range(quantidade):
        inicio = a + i * largura
        ponto = inicio + metodo * largura
        altura = f(ponto)
        area = largura * altura

        retangulos.append((inicio, ponto, altura, area))

    return largura, retangulos


def numero(valor):
    return f'{valor:.3f}'.replace('.', ',')


def projetar(x, y, z=0):
    distancia_x = x - 50
    distancia_y = y - 14
    profundidade = 155 + 0.48 * distancia_x + 0.68 * distancia_y
    escala = 1060 / profundidade

    pixel_x = 450 + escala * (0.88 * distancia_x - 0.47 * distancia_y)
    pixel_y = 320 - escala * (0.24 * distancia_x + 0.45 * distancia_y + z)
    return round(pixel_x), round(pixel_y)


def poligono(superficie, cor, pontos):
    pontos_tela = [projetar(*ponto) for ponto in pontos]
    pygame.draw.polygon(superficie, cor, pontos_tela)


def linha(superficie, cor, inicio, fim, espessura=1):
    pygame.draw.line(
        superficie, cor, projetar(*inicio), projetar(*fim), espessura
    )


def faixa(superficie, cor, x0, x1, y0, y1, z=0):
    pontos = [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)]
    poligono(superficie, cor, pontos)


def construcaoCenario():
    cenario = pygame.Surface((TELA_LARGURA, TELA_ALTURA))
    cenario.fill(FUNDO)
    cenario.set_clip(MAPA)

    for y in range(MAPA.top, MAPA.bottom):
        proporcao = (y - MAPA.top) / MAPA.height
        cor = (int(89 + 47 * proporcao), int(126 + 40 * proporcao),
               int(145 + 24 * proporcao))
        pygame.draw.line(cenario, cor, (MAPA.left, y), (MAPA.right, y))

    poligono(cenario, (49, 66, 38), [
        (-8, -13, 0), (108, -13, 0), (108, -13, -4), (-8, -13, -4)
    ])
    poligono(cenario, (61, 78, 44), [
        (-8, -13, 0), (-8, 43, 0), (-8, 43, -4), (-8, -13, -4)
    ])
    for x in range(-8, 108, 4):
        for y in range(-13, 43, 4):
            cor = (91, 120, 63) if (x // 4 + y // 4) % 2 else (95, 125, 65)
            faixa(cenario, cor, x, x + 4, y, min(y + 4, 43))

    for x in range(COMPRIMENTO_PISTA):
        poligono(cenario, (68, 73, 78), [
            (x, 0, 0), (x + 1, 0, 0),
            (x + 1, f(x + 1), 0), (x, f(x), 0),
        ])

    for x in range(0, COMPRIMENTO_PISTA, 2):
        cor = (223, 218, 199) if (x // 2) % 2 else (165, 54, 49)
        faixa(cenario, cor, x, x + 2, -0.65, 0)
        poligono(cenario, cor, [
            (x, f(x), 0), (x + 2, f(x + 2), 0),
            (x + 2, f(x + 2) + 0.65, 0), (x, f(x) + 0.65, 0),
        ])

    for x in range(0, COMPRIMENTO_PISTA, 5):
        linha(cenario, (191, 194, 188),
              (x, f(x) / 2, 0), (x + 2, f(x + 2) / 2, 0), 2)

    for i in range(8):
        for j in range(2):
            cor = (232, 234, 225) if (i + j) % 2 else (34, 38, 40)
            faixa(cenario, cor, 0.7 + j * 0.7, 1.4 + j * 0.7, i, i + 1)

    cenario.set_clip(None)
    return cenario


def desenharPlano(tela, fontes, largura, retangulos, exibidos, a, b):
    camada = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
    camada.set_clip(MAPA)

    for x in range(0, 101, 10):
        linha(camada, (255, 255, 255, 85), (x, -2, 0), (x, 32, 0))
    for y in range(0, 33, 4):
        linha(camada, (255, 255, 255, 85), (0, y, 0), (100, y, 0))

    for i, retangulo in enumerate(retangulos[:exibidos]):
        inicio, ponto, altura, area = retangulo
        atual = i == exibidos - 1
        cor = (255, 255, 0, 145) if atual else (0, 200, 255, 100)
        faixa(camada, cor, inicio, inicio + largura, 0, altura)

        pontos = [
            (inicio, 0), (inicio + largura, 0),
            (inicio + largura, altura), (inicio, altura),
        ]
        pygame.draw.lines(
            camada, AMARELO if atual else CIANO, True,
            [projetar(*p) for p in pontos], 2 if atual else 1,
        )

    for x in range(COMPRIMENTO_PISTA):
        linha(camada, AMARELO, (x, f(x), 0), (x + 1, f(x + 1), 0), 2)
    linha(camada, CLARO, (0, 0, 0), (105, 0, 0), 2)
    linha(camada, CLARO, (0, 0, 0), (0, 34, 0), 2)

    for limite in (a, b):
        linha(camada, AMARELO, (limite, 0, 0), (limite, f(limite), 0), 3)

    if exibidos:
        _, ponto, altura, _ = retangulos[exibidos - 1]
        pygame.draw.circle(camada, AMARELO, projetar(ponto, altura), 5)

    tela.blit(camada, (0, 0))
    tela.set_clip(MAPA)
    for x in range(0, 101, 20):
        px, py = projetar(x, -1)
        texto(tela, fontes, x, px - 7, py + 3, tamanho=14)
    for y in (8, 16, 24, 32):
        px, py = projetar(0, y)
        texto(tela, fontes, y, px - 25, py - 8, tamanho=14)
    px, py = projetar(104, 0)
    texto(tela, fontes, 'x (m)', px, py, tamanho=14)
    px, py = projetar(0, 34)
    texto(tela, fontes, 'y (m)', px - 24, py - 18, tamanho=14)
    tela.set_clip(None)


def texto(tela, fontes, conteudo, x, y, cor=CLARO, tamanho=18):
    imagem = fontes[tamanho].render(str(conteudo), True, cor)
    tela.blit(imagem, (x, y))


def painel(tela, retangulo):
    pygame.draw.rect(tela, PAINEL, retangulo)
    pygame.draw.rect(tela, BORDA, retangulo, 1)


def botao(tela, fontes, botoes, rotulo, x, y, largura, acao, ativo=False):
    retangulo = pygame.Rect(x, y, largura, 34)
    botoes.append((retangulo, acao))

    cor = (70, 70, 70)
    if ativo:
        cor = (0, 90, 150)
    elif retangulo.collidepoint(pygame.mouse.get_pos()):
        cor = (100, 100, 100)

    pygame.draw.rect(tela, cor, retangulo)
    pygame.draw.rect(tela, CIANO if ativo else BORDA, retangulo, 1)
    imagem = fontes[16].render(rotulo, True, CLARO)
    tela.blit(imagem, imagem.get_rect(center=retangulo.center))


def painelMatematica(tela, fontes, largura, retangulos, exibidos, a, b, modo):
    painel(tela, pygame.Rect(856, 76, 404, 624))
    x = 876
    quantidade = len(retangulos)
    exata = calcular_area_exata(a, b)
    soma = sum(retangulo[3] for retangulo in retangulos[:exibidos])

    texto(tela, fontes, 'Função da pista', x, 94, CINZA_CLARO, 16)
    texto(tela, fontes, 'f(x) = 8 + x²/500', x, 120, tamanho=24)

    texto(tela, fontes, '1. Integral definida', x, 160, VERDE, 20)
    texto(tela, fontes, f'∫ [{a}, {b}] (8 + x²/500) dx', x, 190, tamanho=20)
    texto(tela, fontes, 'F(x) = 8x + x³/1500', x, 220, tamanho=20)
    texto(tela, fontes, f'F({b}) − F({a})', x, 250, tamanho=20)
    texto(tela, fontes, 'Área exata', x, 280, CINZA_CLARO, 16)
    texto(tela, fontes, numero(exata) + ' m²', x, 303, VERDE, 30)

    texto(tela, fontes, '2. Soma de Riemann', x, 360, VERDE, 20)
    texto(tela, fontes, f'Δx = ({b} − {a}) / {quantidade} = {numero(largura)} m',
          x, 392, tamanho=18)
    texto(tela, fontes, f'Retângulos: {exibidos}/{quantidade}', x, 420)

    if exibidos:
        _, ponto, altura, area = retangulos[exibidos - 1]
        texto(tela, fontes, f'x* = {numero(ponto)} m', x, 450)
        texto(tela, fontes, f'f(x*) = {numero(altura)} m', x, 477)
        texto(tela, fontes, f'ΔA = {numero(largura)} × {numero(altura)}', x, 504)
        texto(tela, fontes, f'ΔA = {numero(area)} m²', x, 531, VERDE)
    else:
        texto(tela, fontes, '', x, 477, CINZA_CLARO, 16)

    texto(tela, fontes, 'Resultado', x, 570, CINZA_CLARO, 16)
    resultado = numero(soma) + ' m²' if modo else ''
    texto(tela, fontes, resultado, x, 603, AMARELO, 30)

    erro = 'Aguardando conclusão'
    if modo and exibidos == quantidade:
        erro = numero(abs(exata - soma)) + ' m²'
    texto(tela, fontes, 'Erro absoluto: ' + erro, x, 640, AMARELO, 16)


def painelControles(tela, fontes, a, b, quantidade, indice_metodo, animando):
    botoes = []

    texto(tela, fontes, f'Início: {a} m', 36, 570, CINZA_CLARO, 16)
    texto(tela, fontes, f'Fim: {b} m', 168, 570, CINZA_CLARO, 16)
    texto(tela, fontes, f'Retângulos: {quantidade}', 300, 570, CINZA_CLARO, 16)
    texto(tela, fontes, 'Método de aproximação', 492, 570, CINZA_CLARO, 16)

    for x, acao in [(36, 'a'), (168, 'b'), (300, 'n')]:
        botao(tela, fontes, botoes, '−', x, 595, 54, acao + '-')
        botao(tela, fontes, botoes, '+', x + 60, 595, 54, acao + '+')

    for i, (nome, valor) in enumerate(METODOS):
        botao(tela, fontes, botoes, nome, 492 + i * 110, 595, 104,
              'metodo' + str(i), i == indice_metodo)

    controles = [
        ('Pausar' if animando else 'Calcular', 36, 150, 'calcular'),
        ('Próximo retângulo', 200, 150, 'proximo'),
        ('Mostrar todos', 366, 148, 'todos'),
        ('Limpar', 524, 134, 'reiniciar'),
        ('Ver mapa', 668, 156, 'mapa'),
    ]
    for rotulo, x, largura, acao in controles:
        botao(tela, fontes, botoes, rotulo, x, 650, largura, acao,
              acao == 'calcular')

    return botoes


def main():
    pygame.init()
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption('Projeto Computacional - Soma de Riemann')
    fontes = {
        tamanho: pygame.font.SysFont('arial', tamanho)
        for tamanho in (14, 16, 18, 20, 24, 30)
    }
    cenario = construcaoCenario()
    relogio = pygame.time.Clock()

    a = 0
    b = COMPRIMENTO_PISTA
    indice_quantidade = 0
    indice_metodo = 2
    exibir_plano = False
    animando = False
    exibidos = 0
    tempo_acumulado = 0.0
    botoes = []
    executando = True

    while executando:
        dt = relogio.tick(60) / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
                break

            if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
                continue

            acao = None
            for retangulo, nome_acao in botoes:
                if retangulo.collidepoint(evento.pos):
                    acao = nome_acao
                    break

            if acao is None:
                continue

            configuracao_anterior = (a, b, indice_quantidade, indice_metodo)
            quantidade = QTD_RETANGULO[indice_quantidade]

            if acao == 'a-':
                a = max(0, a - 10)
            elif acao == 'a+':
                a = min(b - 10, a + 10)
            elif acao == 'b-':
                b = max(a + 10, b - 10)
            elif acao == 'b+':
                b = min(COMPRIMENTO_PISTA, b + 10)
            elif acao == 'n-':
                indice_quantidade = max(0, indice_quantidade - 1)
            elif acao == 'n+':
                indice_quantidade = min(len(QTD_RETANGULO) - 1, indice_quantidade + 1)
            elif acao.startswith('metodo'):
                indice_metodo = int(acao[-1])

            elif acao == 'calcular':
                if not exibir_plano or exibidos == quantidade:
                    exibidos = 0
                    tempo_acumulado = 0.0
                    exibir_plano = True
                    animando = True
                else:
                    animando = not animando
            elif acao == 'proximo':
                exibir_plano = True
                animando = False
                exibidos = min(exibidos + 1, quantidade)
                tempo_acumulado = 0.0
            elif acao == 'todos':
                exibir_plano = True
                animando = False
                exibidos = quantidade
            elif acao == 'reiniciar':
                exibir_plano = True
                animando = False
                exibidos = 0
                tempo_acumulado = 0.0
            elif acao == 'mapa':
                exibir_plano = False
                animando = False
                exibidos = 0
                tempo_acumulado = 0.0

            if configuracao_anterior != (a, b, indice_quantidade, indice_metodo):
                exibidos = 0
                animando = False
                tempo_acumulado = 0.0

        if not executando:
            break

        quantidade = QTD_RETANGULO[indice_quantidade]
        metodo = METODOS[indice_metodo][1]
        largura, retangulos = calcular_retangulos(a, b, quantidade, metodo)

        if animando:
            tempo_acumulado += dt
            intervalo = min(0.55, 8 / quantidade)
            while tempo_acumulado >= intervalo and exibidos < quantidade:
                tempo_acumulado -= intervalo
                exibidos += 1
            if exibidos == quantidade:
                animando = False

        tela.fill(FUNDO)
        tela.blit(cenario, MAPA, MAPA)

        if exibir_plano:
            desenharPlano(tela, fontes, largura, retangulos, exibidos, a, b)

        pygame.draw.rect(tela, BORDA, MAPA, 1)
        pygame.draw.rect(tela, FUNDO, (32, 88, 224, 33))
        titulo_mapa = 'Análise matemática' if exibir_plano else 'Mapa da pista'
        texto(tela, fontes, titulo_mapa, 44, 94, CLARO, 16)

        painelMatematica(tela, fontes, largura, retangulos, exibidos, a, b, exibir_plano)
        botoes = painelControles(tela, fontes, a, b, quantidade, indice_metodo, animando)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
