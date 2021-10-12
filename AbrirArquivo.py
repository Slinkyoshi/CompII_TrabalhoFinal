from tkinter import Tk
from tkinter.filedialog import askopenfilename

import nltk

#FUNÇÃO QUER CARREGA O DIRETÓRIO DO ARQUIVO TEXTO
def carregarArquivo():

    Tk().withdraw()
    diretorio = askopenfilename(title = "SELECIONE O ARQUIVO A SER LIDO")
    arquivo = open(diretorio, 'r')
    return lerEOrganizarArquivo(arquivo)

#FUNÇÃO QUE FAZ A LEITURA E ORGANIZAÇÃO DO ARQUIVO TEXTO
def lerEOrganizarArquivo(arquivo):

    lista = arquivo.readlines()
    
    tkn = nltk.WordPunctTokenizer()

    for i in range(len(lista)):
        lista[i] = tkn.tokenize(lista[i])

    return lista






