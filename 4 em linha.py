import numpy as np
import pygame
import sys
import math

azul = (0,0,255)
black = (0,0,0)
vermelho = (255, 0, 0)
amarelo = (255,255,0)
cont_linha = 6
cont_coluna = 7


def criar_tabuleiro():
    tabuleiro = np.zeros ((cont_linha,cont_coluna)) #6 linhas por 7 colunas
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
    print(np.flip(tabuleiro, 0)) #flip "vira" o tabuleiro consoante o x axis


def vencedor (tabuleiro, peça):
    #Verificar horizontais:
    for c in range(cont_coluna-3):
        for l in range(cont_linha):
            if tabuleiro[l][c] == peça and tabuleiro[l][c+1] == peça and tabuleiro[l][c] == peça and tabuleiro[l][c+3] == peça:
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


def desenhar_tabuleiro(tabuleiro):
    for c in range (cont_coluna):
        for l in range (cont_linha):
            pygame.draw.rect(screen, azul,(c*secc_tabuleiro, l*secc_tabuleiro+secc_tabuleiro, secc_tabuleiro, secc_tabuleiro))
            pygame.draw.circle(screen, black, (int(c*secc_tabuleiro+secc_tabuleiro/2), int(l*secc_tabuleiro+secc_tabuleiro+secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))

    for c in range(cont_coluna):
        for l in range(cont_linha):
            if tabuleiro[l][c] == 1:
                pygame.draw.circle(screen, vermelho, (int(c*secc_tabuleiro+secc_tabuleiro/2), height - int(l*secc_tabuleiro+secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))
            elif tabuleiro[l][c] == 2:
                pygame.draw.circle(screen, amarelo, (int(c*secc_tabuleiro+secc_tabuleiro/2), height - int(l*secc_tabuleiro+secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))

    pygame.display.update()

tabuleiro = criar_tabuleiro()
fim_de_jogo = False
vez = 0

pygame.init() #iniciar o jogo

secc_tabuleiro = 100 #tamanho de cada círculo do tabuleiro
width = cont_coluna * secc_tabuleiro
height = (cont_linha+1) * secc_tabuleiro

tamanho = (width, height)


screen = pygame.display.set_mode(tamanho)
desenhar_tabuleiro(tabuleiro)
pygame.display.update()

anuncio = pygame.font.SysFont("monospace", 65)

while fim_de_jogo is not True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #fecha o jogo como deve ser, se se fechar a janela
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0,0, width, secc_tabuleiro))
            posx = event.pos[0]
            if vez == 0:
                pygame.draw.circle(screen, vermelho, (posx, int(secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))
            else: 
                pygame.draw.circle(screen, amarelo, (posx, int(secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN: #todos os eventos do jogo, acontecem quando se clica "down" no rato
            pygame.draw.rect(screen, black, (0,0, width, secc_tabuleiro))
            
            #Jogador 1 joga:
            if vez == 0: #inserir range de entrada de input
                posx = event.pos[0]
                coluna = int(math.floor(posx/secc_tabuleiro))

                if val_local(tabuleiro, coluna):
                    linha = verificar_prox_linha(tabuleiro, coluna)
                    ins_peça(tabuleiro, linha, coluna, 1)

                    if vencedor(tabuleiro, 1):
                        label = anuncio.render("Jogador 1 ganha!", 1, vermelho)
                        screen.blit(label, (40,10))
                        fim_de_jogo = True

            #Pedir o input do Jogador 2:
            else:
                posx = event.pos[0]
                coluna = int(math.floor(posx/secc_tabuleiro))

                if val_local(tabuleiro, coluna):
                    linha = verificar_prox_linha(tabuleiro, coluna)
                    ins_peça(tabuleiro, linha, coluna, 2)

                    if vencedor(tabuleiro, 2):
                        label = anuncio.render("Jogador 2 ganha!", 1, amarelo)
                        screen.blit(label, (40,10))
                        fim_de_jogo = True

            orientação_tabuleiro(tabuleiro)
            desenhar_tabuleiro(tabuleiro)
                
            vez +=1
            vez = vez % 2 #alternar a vez apenas entre 0 e 1

            if fim_de_jogo:
                pygame.time.wait(3000)