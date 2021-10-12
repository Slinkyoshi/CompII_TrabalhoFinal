class Instrucao:

    def __init__(self, C):
        self.C = C
        self.D = []
        self.i = 0
        self.s = -1

    def executar(self):

        while self.i < len(self.C):
            palavras = self.C[self.i].split()
            comando = ""
            parametro = ""
            if len(palavras) == 2:
                comando, parametro = palavras[0], int(palavras[1])
                funcao = getattr(Instrucao, comando)
                funcao(self, parametro)
            else:
                comando = palavras[0]
                funcao = getattr(Instrucao, comando)
                funcao(self)

            self.i += 1

    def CRVL(self, n):
        self.s += 1
        self.D.append(self.D[n])

    def CRCT(self, k):
        self.s += 1
        self.D.append(k)

    def SOMA(self):
        self.D[self.s-1] = self.D[self.s-1] + self.D[self.s]
        self.D.pop()
        self.s -= 1

    def SUBT(self):
        self.D[self.s-1] = self.D[self.s-1] - self.D[self.s]
        self.D.pop()
        self.s -= 1

    def MULT(self):
        self.D[self.s-1] = self.D[self.s-1] * self.D[self.s]
        self.D.pop()
        self.s -= 1

    def DIVI(self):
        self.D[self.s-1] = self.D[self.s-1] / self.D[self.s]
        self.D.pop()
        self.s -= 1

    def INVE(self):
        self.D[self.s] = -self.D[self.s]

    def CONJ(self):
        if self.D[self.s-1] == 1 and self.D[self.s] == 1:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def DISJ(self):
        if self.D[self.s-1] == 1 or  self.D[self.s] == 1:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def NEGA(self):
        self.D[self.s] = 1 - self.D[self.s]

    def CPME(self):
        if self.D[self.s-1] < self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def CPMA(self):
        if self.D[self.s-1] > self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def CPIG(self):
        if self.D[self.s-1] == self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def CDES(self):
        if self.D[self.s-1] != self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def CPMI(self):
        if self.D[self.s-1] <= self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def CMAI(self):
        if self.D[self.s-1] >= self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.D.pop()
        self.s -= 1

    def ARMZ(self, n):
        self.D[n] = self.D[self.s]
        self.D.pop()
        self.s -= 1

    def DSVI(self, p):
        self.i = p - 1

    def DSVF(self, p):
        if self.D[self.s] == 0:
            self.i = p - 1

        self.s -= 1
        self.D.pop()

    def LEIT(self):
        self.s += 1
        entrada = float(input())
        self.D.append(entrada)

    def IMPR(self):
        print(f"{self.D[self.s]}")
        self.D.pop()
        self.s -= 1

    def ALME(self, m):
        for _ in range(m):
            self.s += 1
            self.D.append(None)

    def INPP(self):
        return

    def PARA(self):
        return