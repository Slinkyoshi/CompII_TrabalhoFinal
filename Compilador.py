import sys

from AbrirArquivo import carregarArquivo
from AnalisadorLexico import AnalisadorLexico
from AnalisadorSintatico import AnalisadorSintatico
from AnalisadorSemantico import AnalisadorSemantico
from TabelaDeSimbolos import TabelaDeSimbolos
from GrafoSintatico import grafoSintatico

import Instrucao

def main():

    lista = carregarArquivo()
    token, string = AnalisadorLexico().analisar(lista)
    tabelaDeSimbolos = TabelaDeSimbolos()

    C = []
    D = []
    AnalisadorSintatico(token, string, tabelaDeSimbolos, C, D).analisar()
    AnalisadorSemantico(token, string, tabelaDeSimbolos.getTabela()).analisar()
    tabelaDeSimbolos.mostrarTabela()
    print ("\nCODIGO COMPILADO SEM ERROS")

    print("Instruções")
    print(C)

    Instrucao(C).executar()

    grafoSintatico()





main()



