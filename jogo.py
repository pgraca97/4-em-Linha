import numpy as np
import pygame
import sys
import os
import math
from tkinter import *


os.environ['SDL_VIDEO_CENTERES'] = '1'

pygame.init()

#Variáveis Globais
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

btn_font = ("Press Start 2P", 10)

player1 = "Zé Ninguém"
player2= "Jane Doe"

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

def append_loc_validas(tabuleiro):
    #Agrupar todas as colunas em que se pode inserir a peça para ver quando será o empate em MULTIPLAYER
    loc_validas = []
    for coluna in range (cont_coluna):
        if val_local(tabuleiro,coluna):
            loc_validas.append(coluna)
    return loc_validas

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


def desenhar_tabuleiro(tabuleiro):
    #Desenha o tabuleiro - tabuleiro, circulos que criam o "vazio" em cima da cor do tabuleiro, por serem da mesma cor do fundo + preenche com os respetivos circulos
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


def nomes_players(msg):
    #Pede o Input do nomes dos jogadores quando MULTIPLAYER
    janela_popup = Tk()
    janela_popup.wm_attributes("-toolwindow", True)
    janela_popup.title("Get ready!")
    janela_popup.option_add(btn_font, '10')
    janela_popup.config(bg="#F381C7")

    def center(win):
        #centra a window dos nomes
        win.update_idletasks()
        width_janela = win.winfo_width()
        height_janela = win.winfo_height()
        x = (win.winfo_screenwidth() // 2 ) - (width_janela // 2)
        y = (win.winfo_screenheight() // 2) - (height_janela // 2)
        win.geometry("+%d+%d" % (x,y))

    center(janela_popup)

    def nomes(event = None): #get nomes do input
        global player1, player2
        player1 = entry.get().strip()
        player2 = entry1.get().strip()
        
        janela_popup.destroy() 


    label= Label(janela_popup, text=msg, font=btn_font, bg="#F381C7")
    label.pack(side = "top", fill="x", pady=10)
    
    entry = Entry(janela_popup, width=15, font= btn_font)
    entry.pack(padx=5)
    entry.insert(0, "Zé Ninguém")
    entry.bind("<Return>", nomes)
    entry.focus_set()

    entry1 = Entry(janela_popup, width=15, font= btn_font)
    entry1.pack(pady=5)
    entry1.insert(0, "Jane Doe")
    entry1.bind("<Return>", nomes)
    entry1.focus_set()

    b1 = Button(janela_popup, text = "OK",font=btn_font, command=nomes)
    b1.pack()


    janela_popup.mainloop()


def inicio_jogo():
    #Faz aparecer o jogo em si na janela main - quando se clica em JOGAR MULTIPLAYER.
    nomes_players("Nomes:")

    pygame.display.update()
    tabuleiro = criar_tabuleiro()
    fim_de_jogo = False
    vez = 0

    desenhar_tabuleiro(tabuleiro)
    pygame.draw.rect(screen, cor_fundo, (0,0, width, secc_tabuleiro))
    pygame.display.update()


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
                            text_vencedor = font(35).render("{0} ganha!".format(player1), True, verde)
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
                            text_vencedor = font(35).render("{0} ganha!".format(player2), True, rosa)
                            rect_menu = text_vencedor.get_rect(center=(350, 75))
                            screen.blit(text_vencedor,rect_menu)
                            fim_de_jogo = True

                if len(append_loc_validas(tabuleiro)) == 0:
                    text_vencedor = font(35).render("EMPATE!", True, cor_tabuleiro)
                    rect_menu = text_vencedor.get_rect(center=(350, 75))
                    screen.blit(text_vencedor,rect_menu)
                    fim_de_jogo = True

                orientação_tabuleiro(tabuleiro)
                desenhar_tabuleiro(tabuleiro)
                    
                vez +=1
                vez = vez % 2 #alternar a vez apenas entre 0 e 1


    return fim_de_jogo