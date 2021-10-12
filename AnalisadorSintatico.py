
import sys

class AnalisadorSintatico:

    def __init__ (self, token, string, tabela, C, D):

        self.token = []
        self.string = []
        self.tabelaDeSimbolos = tabela
        self.carga = ''

        self.C = C
        self.D = D

        self.i = 0
        self.s = -1


        print ("\n ANALISANDO SINTATICAMENTE... \n")

        print ("\n EXECUTANDO OPERAÇÕES COM A TABELA DE SIMBOLOS... \n")

        for i in range(len(token)):

            for j in range(len(token[i])):
                self.token.append(token[i][j])
                self.string.append(string[i][j])

        #print(self.token)
        #print()

    def erro(self, funcao, elemento):
        print ("ERRO SINTATICO NA FUNÇÃO ", funcao, " -> ESPERAVA O TOKEN ", elemento)
        sys.exit()

    def remove(self):
        #print(self.token[0])
        #print()
        self.token.pop(0)
        self.string.pop(0)


    def analisar(self):

        def programa():

            if (self.token[0] == 'program'):
                self.remove()

                if (self.token[0] == 'ident'):
                    self.tabelaDeSimbolos.addTabela('ident', self.string[0], '', 'program', 'global', '')
                    self.C.append("INPP")
                    self.s = -1
                    self.remove()  
                    corpo()

                    if (self.token[0] == '.'):
                        self.C.append("PARA")
                        self.remove()

                    else:
                        self.erro("programa", '.')

                else:
                    self.erro("programa", "ident")
            else:
                self.erro("programa", "program")

        def corpo():

            dc()

            if (self.token[0] == 'begin'):
                self.remove()
                comandos()

                if (self.token[0] == 'end'):
                    self.remove()

                else:
                    self.erro("corpo", "end")

            else:
                self.erro("corpo", "begin")
        
        def dc():

            if (self.token[0] == 'real' or self.token[0] == 'integer'):
                dc_v()
                mais_dc()

            else:
                return ''

        def mais_dc():

            if (self.token[0] == ';'):
                self.remove()
                dc()

            else:
                return ''

        def dc_v():

            tipo_var()

            if (self.token[0] == ':'):
                self.remove()
                variaveis()

            else:
                self.erro("dc_v", ':')

        def tipo_var():
            
            if (self.token[0] == "real" or self.token[0] == "integer"):
                self.carga = self.token[0]
                self.tabelaDeSimbolos.inserirTipo(self.token[0])
                self.tabelaDeSimbolos.addTabela(self.token[0], '', '', '', '', '')
                self.remove()

            else:
                self.erro("tipo_var", "real ou integer")

        def variaveis():

            if (self.token[0] == "ident"):
                self.tabelaDeSimbolos.inserirTipo(self.token[0])
                self.tabelaDeSimbolos.addTabela(self.token[0], self.string[0], self.carga, "declaracao", 'global', '')
                self.C.append("ALME 1")
                self.s += 1
                self.remove()
                mais_var()

            else:
                self.erro("variaveis", "integer")

        def mais_var():

            if (self.token[0] == ','):
                self.remove()
                variaveis()

            else:
                return ''

        def comandos():

            comando()
            mais_comandos()

        def mais_comandos():

            if (self.token[0] == ';'):
                self.tabelaDeSimbolos.addTabela(self.token[0], self.string[0], "", "", "", "")
                self.remove()
                comandos()

            else:
                return ''

        def comando():

            if (self.token[0] == "read" or self.token[0] == "write"):
                self.carga = self.token[0]
                self.remove()

                if (self.token[0] == '('):
                    self.remove()

                    if (self.token[0] == "ident"):
                        self.tabelaDeSimbolos.addTabela('ident', self.string[0], '', self.carga, 'global', '')

                        if (self.carga == "read"):
                            self.C.append("LEIT")
                            self.s += 1
                            self.C.append("ARMZ 0")

                        elif (self.carga == "write"):
                            self.C.append("CRVL 0")
                            self.s += 1
                            self.C.append("IMPR")

                        self.remove()

                        if (self.token[0] == ')'):
                            self.remove()

                        else:
                            self.erro("comando", ')')

                    else:
                        self.erro("comando", "ident")

                else:
                    self.erro("comando", ')')
            
            elif (self.token[0] == "ident"):
                self.carga = 'atribuicao'
                self.tabelaDeSimbolos.addTabela('ident', self.string[0], '', self.carga, 'global', '')
                self.remove()

                if (self.token[0] == ":="):
                    self.remove()
                    expressao()

                else:
                    self.erro("comando", ":=")

            elif (self.token[0] == "if"):
                self.carga = self.token[0]
                self.remove()
                condicao()

                if (self.token[0] == "then"):
                    self.C.append("DSVF")  # adicionar linha p depois
                    linhaDSVF = len(self.C) - 1
                    self.remove()
                    comandos()
                    self.C.append("DSVI")  # adicionar linha p depois
                    linhaDSVI = len(self.C) - 1

                    linhaElse = len(self.C)
                    pfalsa()

                    if len(self.C) == linhaElse:
                        # nao tem else
                        self.C.pop()  # remove o comando DSVI, pois eh desnecessario
                        self.C[linhaDSVF] += f" {len(self.C)}"
                    else:
                        # tem else
                        self.C[linhaDSVF] += f" {linhaElse}"
                        self.C[linhaDSVI] += f" {len(self.C)}"

                    if (self.token[0] == '$'):
                        self.remove()

                    else:
                        self.erro("comando", '$')

                else:
                    self.erro("comando", "then")

            elif (self.token[0] == "while"):
                linhaCondicao = len(self.C)
                self.carga = self.token[0]
                self.remove()
                condicao()
                self.C.append("DSVF")  # adicionar linha p depois
                linhaDSVF = len(self.C) - 1


                if (self.token[0] == "do"):
                    self.remove()
                    comandos()
                    self.C.append(f"DSVI {linhaCondicao}")

                    linhaAposWhile = len(self.C)
                    self.C[linhaDSVF] += f" {linhaAposWhile}"

                    if (self.token[0] == "$"):
                        self.remove()

                    else:
                        self.erro("comando", '$')

                else:
                    self.erro("comando", 'do')

            else:
                self.erro("comando", "read ou write / ident / if / while")

        def condicao():

            expressao()
            relacao()
            expressao()

        def relacao():

            if (self.token[0] == '=' or self.token[0] == "<>" or self.token[0] == ">=" or self.token[0] == "<=" or self.token[0] == '>' or self.token[0] == '<'):

                if (self.token[0] == '='):
                    self.C.append("CPIG")

                if (self.token[0] == '<>'):
                    self.C.append("CDES")

                if (self.token[0] == '>='):
                    self.C.append("CMAI")

                if (self.token[0] == '<='):
                    self.C.append("CPMI")

                if (self.token[0] == '>'):
                    self.C.append("CPMA")

                if (self.token[0] == '<'):
                    self.C.append("CPME")

                self.remove()

            else:
                self.erro("relacao", "= ou <> ou >= ou <= ou > ou <")

        def expressao():

            termo()
            outros_termos()

        def termo():

            op_un()
            fator()
            mais_fatores()

        def op_un():

            if (self.token[0] == '-'):
                self.remove()

            else:
                return ''

        def fator():

            if (self.token[0] == "ident" or self.token[0] == "numero_inteiro" or self.token[0] == "numero_real"):

                if (self.token[0] == 'ident'):
                    self.tabelaDeSimbolos.addTabela('ident', self.string[0], '', self.carga, 'global', '')

                if (self.token[0] == 'numero_inteiro'):
                    self.tabelaDeSimbolos.addTabela('numero_inteiro', self.string[0], 'integer', '', '', self.string[0])

                if (self.token[0] == 'numero_real'):
                    self.tabelaDeSimbolos.addTabela('numero_real', self.string[0], 'real', '', '', self.string[0])

                self.C.append("CRVL 2")
                self.C.append("INVE")

                self.remove()

            elif (self.token[0] == '('):
                self.remove()
                expressao()

                if (self.token[0] == ')'):
                    self.remove()

                else:
                    self.erro("fator", ')')

            else:
                self.erro("fator", "ident ou numero_inteiro ou numero_real / (")

        def outros_termos():

            if (self.token[0] == '+' or self.token[0] == '-'):
                op_ad()
                termo()
                outros_termos()

            else:
                return ''

        def op_ad():

            if (self.token[0] == '+' or self.token[0] == '-'):

                if (self.token[0] == '-'):

                    if (self.token[0] == '-'):
                        self.C.append("SUBT")

                    else:
                        self.C.append("SOMA")


                self.remove()

            else:
                self.erro("op_ad", "+ ou -")

        def mais_fatores():

            if (self.token[0] == '*' or self.token[0] == '/'):
                op_mul()
                fator()
                mais_fatores()

            else:
                return ''

        def op_mul():

            if (self.token[0] == '*' or self.token[0] == '/'):

                if (self.token[0] == "*"):
                    self.C.append("MULT")

                else:
                    self.C.append("DIVI")

                self.remove()

            else:
                self.erro("op_mul", "* ou /")

        def pfalsa():

            if (self.token[0] == "else"):
                self.remove()
                comandos()

            else:
                return ''

        programa()

        self.tabelaDeSimbolos.complementaTabela()

























