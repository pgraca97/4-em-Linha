import pygame, sys
from jogo import *
from button import Button


pygame.init() #iniciar o jogo/janela

#Variáveis Globais
WINDOW = pygame.display.set_mode((700, 700))
pygame.display.set_caption("4 em Linha")
BG = pygame.image.load("assets\Background.png")

BG_PLAY_BUTTON = pygame.image.load("assets\Play Rect.png")
BG_AI_BUTTON = pygame.image.load("assets\Ai Rect.png")
BG_EXIT_BUTTON = pygame.image.load("assets\Exit Rect.png")

def play():
    while True:
        
        fim_de_jogo=inicio_jogo()

        if fim_de_jogo:
            pygame.time.wait(1000)
            menu_princ()

        pygame.display.update()


def menu_princ(): 
    #Menu Principal
    while True:
        WINDOW.blit(BG, (0,0)) #blit - Block Transfer - copia os conteúdos de uma surface/window para outra

        pos_mouse = pygame.mouse.get_pos() #get a posição do cursos do mouse
        text_menu = font(75).render("MENU", True, "#f873a2")
        rect_menu = text_menu.get_rect(center=(350, 75))

        play_button = Button(image=pygame.transform.scale(BG_PLAY_BUTTON,(570,109) ), pos=(350, 250), text_input="JOGAR MULTIPLAYER", font=font(30), base_color="#d7fcd4", hovering_color="White")
        ai_button = Button(image=pygame.transform.scale(BG_AI_BUTTON,(550,109) ), pos=(350, 400), text_input="JOGAR CONTRA AI", font=font(30), base_color="#d7fcd4", hovering_color="White")
        exit_button = Button(image=pygame.transform.scale(BG_EXIT_BUTTON,(195,109) ), pos=(350, 550), text_input="SAIR", font=font(30), base_color="#d7fcd4", hovering_color="White")

        WINDOW.blit(text_menu,rect_menu)

        for button in [play_button, ai_button, exit_button]:
            button.changeColor(pos_mouse)
            button.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(pos_mouse): #se o input for no botão do "JOGAR" - começa o jogo multiplayer
                    play()
                #if ai_button.checkForInput(pos_mouse): #se o input for no botão do "JOGAR CONTRA AI" - começa o jogo contra AI
                    #play_ai()
                if exit_button.checkForInput(pos_mouse): #se o input for no botão do "SAIR" - a janela fecha-se/jogo encerra
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

menu_princ()
