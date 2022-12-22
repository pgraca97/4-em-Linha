import numpy as np
import pygame
import sys
import math


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

def font(size):
    #Devolve a font no tamanho que eu quiser
    return pygame.font.Font("assets/font.ttf", size)

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


def desenhar_tabuleiro(tabuleiro):
    for c in range (cont_coluna):
        for l in range (cont_linha):
            pygame.draw.rect(screen, cor_tabuleiro,(c*secc_tabuleiro, l*secc_tabuleiro+secc_tabuleiro, secc_tabuleiro, secc_tabuleiro))
            pygame.draw.circle(screen, cor_fundo, (int(c*secc_tabuleiro+secc_tabuleiro/2), int(l*secc_tabuleiro+secc_tabuleiro+secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))

    for c in range(cont_coluna):
        for l in range(cont_linha):
            if tabuleiro[l][c] == 1:
                pygame.draw.circle(screen, verde, (int(c*secc_tabuleiro+secc_tabuleiro/2), height - int(l*secc_tabuleiro+secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))
            elif tabuleiro[l][c] == 2:
                pygame.draw.circle(screen, rosa, (int(c*secc_tabuleiro+secc_tabuleiro/2), height - int(l*secc_tabuleiro+secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))

    pygame.display.update()



pygame.init() #iniciar o jogo

def inicio_jogo():
    tabuleiro = criar_tabuleiro()
    print(1)
    fim_de_jogo = False
    vez = 0

    desenhar_tabuleiro(tabuleiro)
    pygame.draw.rect(screen, cor_fundo, (0,0, width, secc_tabuleiro))
    pygame.display.update()


    print("Fim do jogo:"+str(fim_de_jogo))
    while fim_de_jogo is not True:
        
        for event in pygame.event.get():
            pygame.draw.rect(screen, cor_fundo, (0,0, width, secc_tabuleiro))
            if event.type == pygame.QUIT: #fecha o jogo como deve ser, se se fechar a janela
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                posx = event.pos[0]
                if vez == 0:
                    pygame.draw.circle(screen, verde, (posx, int(secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))
                else: 
                    pygame.draw.circle(screen, rosa, (posx, int(secc_tabuleiro/2)), radius=int(secc_tabuleiro/2-5))
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN: #todos os eventos do jogo, acontecem quando se clica "down" no rato
                pygame.draw.rect(screen, cor_fundo, (0,0, width, secc_tabuleiro))
                
                #Jogador 1 joga:
                if vez == 0: 
                    posx = event.pos[0]
                    coluna = int(math.floor(posx/secc_tabuleiro)) #vê onde o mouse está e escolhe essa coluna com base nisso

                    if val_local(tabuleiro, coluna):
                        linha = verificar_prox_linha(tabuleiro, coluna)
                        ins_peça(tabuleiro, linha, coluna, 1)

                        if vencedor(tabuleiro, 1):
                            text_vencedor = font(35).render("Jogador 1 ganha!", True, verde)
                            rect_menu = text_vencedor.get_rect(center=(350, 75))
                            screen.blit(text_vencedor,rect_menu)
                            fim_de_jogo = True

                #Pedir o input do Jogador 2:
                else:
                    posx = event.pos[0]
                    coluna = int(math.floor(posx/secc_tabuleiro)) #vê onde o mouse está e escolhe essa coluna com base nisso

                    if val_local(tabuleiro, coluna):
                        linha = verificar_prox_linha(tabuleiro, coluna)
                        ins_peça(tabuleiro, linha, coluna, 2)

                        if vencedor(tabuleiro, 2):
                            text_vencedor = font(35).render("Jogador 2 ganha!", True, rosa)
                            rect_menu = text_vencedor.get_rect(center=(350, 75))
                            screen.blit(text_vencedor,rect_menu)
                            fim_de_jogo = True

                orientação_tabuleiro(tabuleiro)
                desenhar_tabuleiro(tabuleiro)
                    
                vez +=1
                vez = vez % 2 #alternar a vez apenas entre 0 e 1
    return fim_de_jogo