import numpy as np

cont_linha = 6
cont_coluna = 7
def criar_tabuleiro():
    tabuleiro = np.zeros ((6,7)) #6 linhas por 7 colunas
    return tabuleiro

def ins_peça():
    #Inserir a peça no tabuleiro
    pass

def val_local(tabuleiro,jogada):
    #Validar a localização onde o Jogador quer inserir a peça - Pode ou não?
    return tabuleiro[5][jogada] == 0

def get_next_open_row(tabuleiro,jogada):
    pass

tabuleiro = criar_tabuleiro()
fim_de_jogo = False
vez = 0
while not fim_de_jogo:
    #Pedir o input do Jogado 1:
        if vez == 0: #inserir range de entrada de input
            jogada = int(input("Jogador 1, faça a sua jogada (entre 0-6): ")) #0-6 são as colunas
    #Pedir o input do Jogador 2:
        else:
            jogada = int(input("Jogador 2, faça a sua jogada (entre 0-6): ")) #0-6 são as colunas

        vez +=1
        vez = vez % 2 #alternar a vez apenas entre 0 e 1