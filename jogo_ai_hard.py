import numpy as np
import pygame
import sys
import os

import math
import random

os.environ['SDL_VIDEO_CENTERES'] = '1'
pygame.init() #iniciar o jogo

cor_tabuleiro = (255,244,97)
cor_fundo = (4,44,29)
verde = (115, 255, 204)
rosa = (243,129,199)

cont_linha = 6
cont_coluna = 7

secc_tabuleiro = 100 #tamanho de cada "círculo" do tabuleiro
width = cont_coluna * secc_tabuleiro
height = (cont_linha+1) * secc_tabuleiro

tamanho = (width, height)

screen = pygame.display.set_mode(tamanho)

esp_vazio = 0
peça_humano = 1
peça_maquina = 2
jogada_vencedora = 4

def font(size):
    #Devolve a font no tamanho que eu quiser
    return pygame.font.Font("assets/font.ttf", size)


def criar_tabuleiro():
    #Cria tabuleiro
    tabuleiro = np.zeros ((cont_linha,cont_coluna)) #np.zeros - devolve uma nova array com 6 linhas por 7 colunas preenchida com 0s
    return tabuleiro


def ins_peça(tabuleiro, linha, coluna, peça):
    #Inserir a peça no tabuleiro
    tabuleiro[linha][coluna] = peça


def val_local(tabuleiro,coluna):
    #Validar a localização onde o Jogador quer inserir a peça - Pode ou não?
    return tabuleiro[cont_linha-1][coluna] == 0 #se for true é ok inserir peça, se não significa que a coluna já foi "cheia" até ao de cima


def verificar_prox_linha(tabuleiro,coluna): 
    #verificar que row a peça vai/pode ser inserida; se o slot é 0, significa que ainda está vazio, por isso retorna o 1º index que está vazio
    for l in range(cont_linha):
        if tabuleiro[l][coluna] == 0:
            return l


def orientação_tabuleiro(tabuleiro):
    #Inverte/Flip o tabuleiro para as peças começarem a entrar no "fundo" do mesmo
    
    print(np.flip(tabuleiro, 0)) #flip "vira" o tabuleiro consoante o x axis


def vencedor (tabuleiro, peça):
    #Verifica quais a jogadas vencedoras

    #Verificar horizontais:
    for c in range(cont_coluna-3):
        for l in range(cont_linha):
            if tabuleiro[l][c] == peça and tabuleiro[l][c+1] == peça and tabuleiro[l][c+2] == peça and tabuleiro[l][c+3] == peça:
                return True

    #Verificar Verticais
    for c in range(cont_coluna):
        for l in range(cont_linha-3):
            if tabuleiro[l][c] == peça and tabuleiro[l+1][c] == peça and tabuleiro[l+2][c] == peça and tabuleiro[l+3][c] == peça:
                return True

    #Verificar Diagonais +
    for c in range(cont_coluna-3):
        for l in range(cont_linha-3):
            if tabuleiro[l][c] == peça and tabuleiro[l+1][c+1] == peça and tabuleiro[l+2][c+2] == peça and tabuleiro[l+3][c+3] == peça:
                return True

    #Verificar Diagonais -
    for c in range(cont_coluna-3):
        for l in range(3, cont_linha):
            if tabuleiro[l][c] == peça and tabuleiro[l-1][c+1] == peça and tabuleiro[l-2][c+2] == peça and tabuleiro[l-3][c+3] == peça:
                return True


def avaliar_jog_venc(quatro_em_linha, peça):
    #Avalia as jogadas mais importantes - torna a função pontuar_tabuleiro menos abstrata/+ simples
    pontos = 0
    peça_adv = peça_humano
    if peça == peça_humano:
        peça_adv = peça_maquina

    if quatro_em_linha.count(peça) == 4:
        pontos += 200
    elif quatro_em_linha.count(peça) == 3 and quatro_em_linha.count(esp_vazio) == 1:
        pontos += 10
    elif quatro_em_linha.count(peça) == 2 and quatro_em_linha.count(esp_vazio) == 2:
        pontos += 2

    if quatro_em_linha.count(peça_adv) == 3 and quatro_em_linha.count(esp_vazio) == 1:
        pontos -= 10
    elif quatro_em_linha.count(peça_adv) == 2 and quatro_em_linha.count(esp_vazio) == 2:
        pontos -= 2
            

    return pontos


def pontuar_tabuleiro(tabuleiro, peça):
    #Pontuar o tabuleiro por inteiro
    pontos = 0
    #Centrais
    centro_lista = [int(i) for i in list(tabuleiro[:, cont_coluna//2])] #a coluna do centro pois é a que dá + possibilidades de ganhar
    centro_cont = centro_lista.count(peça)
    pontos += centro_cont * 3

    # Na Horizontal
    for l in range(cont_linha):
        linha_lista = [int(i) for i in list(tabuleiro[l,:])] #a linha em que estamos + todas as colunas para essa linha
        for c in range(cont_coluna-3):
            quatro_em_linha = linha_lista[c:c+jogada_vencedora]
            pontos += avaliar_jog_venc(quatro_em_linha,peça)
    
    #Na Vertical
    for c in range(cont_coluna):
        coluna_lista = [int(i) for i in list(tabuleiro[:,c])] #a coluna em que estamos + todas as linhas para essa coluna
        for l in range(cont_linha-3):
            quatro_em_linha = coluna_lista[l:l+jogada_vencedora]
            pontos += avaliar_jog_venc(quatro_em_linha,peça)


    #Na Diagonal +
    for l in range(cont_linha-3):
        for c in range(cont_coluna-3):
            quatro_em_linha = [tabuleiro[l+i][c+i] for i in range(jogada_vencedora)]
            pontos += avaliar_jog_venc(quatro_em_linha,peça)
    
    #Na Diagonal - 
    for l in range(cont_linha-3):
        for c in range(cont_coluna-3):
            quatro_em_linha = [tabuleiro[l+3-i][c+i] for i in range(jogada_vencedora)]
            pontos += avaliar_jog_venc(quatro_em_linha,peça)

    return pontos


def append_loc_validas(tabuleiro):
    #Agrupar todas as colunas em que se pode inserir a peça para serem avaliadas consuante pontuação na função escolhe_melhor_pont
    loc_validas = []
    for coluna in range (cont_coluna):
        if val_local(tabuleiro,coluna):
            loc_validas.append(coluna)
    return loc_validas


def escolhe_melhor_pont(tabuleiro,peça):
    #Recorrendo a append_loc_validas e a pontuar_tabuleiro escolhe as posições que fornecem a melhor pontuação
    loc_validas = append_loc_validas(tabuleiro)
    melhor_pont = -2000
    melhor_col = random.choice(loc_validas)

    for col in loc_validas:
        linha = verificar_prox_linha(tabuleiro, col)
        tabuleiro_temp = tabuleiro.copy() #para não modificar o tabuleiro principal
        ins_peça(tabuleiro_temp, linha, col, peça)
        pontos = pontuar_tabuleiro(tabuleiro_temp, peça)
        if pontos > melhor_pont:
            melhor_pont = pontos
            melhor_col = col

    return melhor_col

def possibilidades (tabuleiro):

    return vencedor(tabuleiro, peça_humano) or vencedor(tabuleiro, peça_maquina) or len(append_loc_validas(tabuleiro)) == 0

#ALGORITMO MINIMAX + ALPHA-BETA PRUNING
def minimax_alg(tabuleiro, depth, alpha, beta, jogador_max): #depth =  o quão longe queremos ir nas possibilidades de procurar a melhor jogada #jogador_max é true para a AI e falso para o HUMANO
    loc_validas = append_loc_validas(tabuleiro)
    poss_de_jogo = possibilidades(tabuleiro)
    
    if depth == 0 or poss_de_jogo:
        if poss_de_jogo:
            if vencedor(tabuleiro, peça_maquina):
                return (None, 500000000000000)
            elif vencedor(tabuleiro,peça_humano):
                return (None, -500000000000000)
            else: #Empate
                return (None, 0)
        else: #depth é 0
            return (None, pontuar_tabuleiro(tabuleiro, peça_maquina))
    
    if jogador_max:
        pontos = -math.inf
        coluna = random.choice(loc_validas)
        for col in loc_validas:
            linha = verificar_prox_linha(tabuleiro, col)
            tab_copy = tabuleiro.copy()
            ins_peça(tab_copy, linha, col, peça_maquina)
            new_pontos = minimax_alg(tab_copy, depth-1, alpha, beta, False)[1]
            if new_pontos > pontos: #saber que coluna produz os pontos max
                pontos = new_pontos
                coluna = col
            alpha = max(alpha, pontos)
            if alpha >= beta:
                break

        return coluna, pontos
    else: #jogador_min = HUMANO
        pontos = math.inf
        coluna = random.choice(loc_validas)
        for col in loc_validas:
            linha = verificar_prox_linha(tabuleiro,col)
            tab_copy = tabuleiro.copy()
            ins_peça(tab_copy, linha, col, peça_humano)
            new_pontos = minimax_alg(tab_copy, depth-1, alpha, beta, True)[1]
            if new_pontos < pontos:
                pontos = new_pontos
                coluna = col
            beta = min(beta, pontos)
            if alpha >= beta:
                break 

        return coluna, pontos


def desenhar_tabuleiro(tabuleiro):
    #Desenha o tabuleiro - tabuleiro, circulos que criam o "vazio" em cima da cor do tabuleiro, por serem da mesma cor do fundo + preenche com os respetivos circulos
    for c in range (cont_coluna):
        for l in range (cont_linha):
            pygame.draw.rect(screen, cor_tabuleiro,(c*secc_tabuleiro, l*secc_tabuleiro+secc_tabuleiro, secc_tabuleiro, secc_tabuleiro))
            pygame.draw.circle(screen, cor_fundo, (int(c*secc_tabuleiro+secc_tabuleiro/2), int(l*secc_tabuleiro+secc_tabuleiro+secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))

    for c in range(cont_coluna):
        for l in range(cont_linha):
            if tabuleiro[l][c] == peça_humano:
                pygame.draw.circle(screen, verde, (int(c*secc_tabuleiro+secc_tabuleiro/2), height - int(l*secc_tabuleiro+secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))
            elif tabuleiro[l][c] == peça_maquina:
                pygame.draw.circle(screen, rosa, (int(c*secc_tabuleiro+secc_tabuleiro/2), height - int(l*secc_tabuleiro+secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))

    pygame.display.update()


def iniciar_jogo():
    #Faz aparecer o jogo em si na janela main - quando se clica em JOGAR CONTRA AI.
    tabuleiro = criar_tabuleiro()
    desenhar_tabuleiro(tabuleiro)
    pygame.draw.rect(screen, cor_fundo, (0,0, width, secc_tabuleiro))
    pygame.display.update()

    humano = 0
    maquina = 1
    vez = random.randint(humano,maquina) #escolher à sorte quem começa a jogar

    fim = False
    while fim is not True:
        
        for event in pygame.event.get():
            pygame.draw.rect(screen, cor_fundo, (0,0, width, secc_tabuleiro))
            if event.type == pygame.QUIT: #fecha o jogo como deve ser, se se fechar a janela
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                posx = event.pos[0]
                if vez == humano:
                    pygame.draw.circle(screen, verde, (posx, int(secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN: #todos os eventos do jogo, acontecem quando se clica "down" no rato
                pygame.draw.rect(screen, cor_fundo, (0,0, width, secc_tabuleiro))
                
                #Jogador 1 joga:
                if vez == humano: #inserir range de entrada de input
                    posx = event.pos[0]
                    coluna = int(math.floor(posx/secc_tabuleiro)) #vê onde o mouse está e escolhe essa coluna com base nisso

                    if val_local(tabuleiro, coluna):
                        linha = verificar_prox_linha(tabuleiro, coluna)
                        ins_peça(tabuleiro, linha, coluna, peça_humano)

                        if vencedor(tabuleiro, peça_humano):
                            text_vencedor = font(35).render("Jogador 1 ganha!", True, verde)
                            rect_menu = text_vencedor.get_rect(center=(350, 75))
                            screen.blit(text_vencedor,rect_menu)
                            fim = True
                        
                        vez +=1
                        vez = vez % 2 #alternar a vez apenas entre 0 e 1

                    orientação_tabuleiro(tabuleiro)
                    desenhar_tabuleiro(tabuleiro)

        #Vez da máquina - vai inserir a peça quando o jogador 1 finaliza a jogada:
        if vez == maquina and not fim:
            #coluna = random.randint(0, cont_coluna-1) #escolhe uma coluna random no range dos indexes existentes
            #coluna = escolhe_melhor_pont(tabuleiro,peça_maquina)
            coluna, pont_minimax = minimax_alg(tabuleiro, 5, -math.inf, math.inf, True)

            if val_local(tabuleiro, coluna):
                #pygame.time.wait(500)
                linha = verificar_prox_linha(tabuleiro, coluna)
                ins_peça(tabuleiro, linha, coluna, peça_maquina)

                if vencedor(tabuleiro, peça_maquina):
                    text_vencedor = font(35).render("AI ganha!", True, rosa)
                    rect_menu = text_vencedor.get_rect(center=(350, 75))
                    screen.blit(text_vencedor,rect_menu)
                    fim = True

                orientação_tabuleiro(tabuleiro)
                desenhar_tabuleiro(tabuleiro)
                    
                vez +=1
                vez = vez % 2 #alternar a vez apenas entre 0 e 1
    return fim