
import sys

class AnalisadorSemantico:

    def __init__(self, token, string, tabela):

        self.tabela = tabela
        self.token = token
        self.string = string
        self.listaVariaveis = []
        self.listaTipos = []
        print ("\n ANALISANDO SEMANTICAMENTE... \n")
    
    def erroDeclaracao(self, cadeia):
        print ("ERRO SEMANTICO: A VARIAVEL", cadeia, "JÁ FOI USADA EM OUTRA DECLARAÇÃO")
        sys.exit()

    def erroAtribuicao(self, cadeia1, tipo1, cadeia2, tipo2):
        print ("ERRO SEMANTICO: A VARIAVEL", cadeia1, "COM O TIPO", tipo1, "ESTA SENDO ATRIBUIDA COM A VARIAVEL", cadeia2, "E TIPO", tipo2)
        sys.exit()

    def erroExistencia(self, cadeia, escopo):
        print ("ERRO SEMANTICO: A VARIAVEL", cadeia, "NÃO FOI DECLARADA NO ESCOPO", escopo)
        sys.exit()

    def verificaDeclaracao(self):

        for i in range(len(self.tabela["categoria"])):

            if (self.tabela["categoria"][i] == "declaracao"):

                if (self.tabela["cadeia"][i] in self.listaVariaveis):
                    self.erroDeclaracao(self.tabela["cadeia"][i])

                self.listaVariaveis.append(self.tabela["cadeia"][i])
                self.listaTipos.append(self.tabela["tipo"][i])

        for i in range(len(self.tabela["categoria"])):

            if (self.tabela["categoria"][i] == "atribuicao" and self.tabela["token"][i] == "ident" and self.tabela["cadeia"][i] not in self.listaVariaveis):
                self.erroExistencia(self.tabela["cadeia"][i], "global")


    def verificaAtribuicao(self):

        cont = 0
        variavel = ''
        tipo = ''

        for i in range(len(self.tabela["categoria"])):

            if (self.tabela["token"][i] == ';'):
                cont = 0
                continue

            if (self.tabela["categoria"][i] == "atribuicao" and cont == 0):
                variavel = self.tabela["cadeia"][i]
                tipo = self.listaTipos[self.buscaVariavel(variavel)]
                cont = 1
                continue

            if (cont == 1):

                if (self.tabela["categoria"][i] == "atribuicao"):

                    for j in range(len(self.listaVariaveis)):

                        if (self.listaVariaveis[j] == self.tabela["cadeia"][i]):

                            if (self.listaTipos[j] != tipo):
                                self.erroAtribuicao(variavel, tipo, self.listaVariaveis[j], self.listaTipos[j])

    def buscaVariavel(self, cadeia):

        for i in range(len(self.listaVariaveis)):

            if (self.listaVariaveis[i] == cadeia):
                return i

        self.erroExistencia(cadeia, "global")

    def analisar(self):

        self.verificaDeclaracao()
        self.verificaAtribuicao()


        





                

    



                

                



                