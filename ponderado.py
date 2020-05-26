from math import cos, exp, radians, tan

class Ponderado:
    def __init__(self, espesor1, espesor2, DF, B):
        self.espesor1 = espesor1
        self.espesor2 = espesor2
        self.DF = DF
        self.B = B

    def angulo(self, fi1, fi2, fi3):
        '''Con los ángulos proporcionados por el usuario se calcula el ponderado y a su vez el Hmax
        que depende del mismo'''
        f1 = 1  # Pequeña asunción de fi para la convergencia del método
        d = 1  # Tolerancia del WHILE
        while d > 0.001:
            Hmax = self.B / 2 / cos(radians(45 + f1 / 2)) * exp(radians(45 + f1 / 2) * tan(radians(f1))) * cos(
                radians(f1))
            if self.DF < self.espesor1:
                if Hmax <= (self.espesor1 - self.DF):
                    f2 = fi1
                elif self.espesor1 < Hmax + self.DF <= self.espesor1 + self.espesor2:
                    f2 = ((self.espesor1 - self.DF) * fi1 + (Hmax - (self.espesor1 - self.DF)) * fi2) / Hmax
                else:
                    f2 = ((self.espesor1 - self.DF) * fi1 + self.espesor2 * fi2 + (Hmax - (self.espesor1 - self.DF) - self.espesor2) * fi3) / Hmax
            elif self.espesor1 <= self.DF < self.espesor2 + self.espesor1:
                if Hmax <= (self.espesor1 + self.espesor2 - self.DF):
                    f2 = fi2
                else:
                    f2 = ((self.espesor1 + self.espesor2 - self.DF) * fi2 + (Hmax - (self.espesor1 + self.espesor2 - self.DF)) * fi3) / Hmax
            else:
                f2 = fi3
            d = abs(f1 - f2)
            f1 = f2
        self.Hmax = Hmax
        return f2, Hmax

    def cohesion(self, cohesion1, cohesion2, cohesion3):
        ''' Con las cohesiones dadas para cada estrato se calcula la ponderada.
        ***REGLA*** antes de correr este método, es necesario correr el del ángulo, ya que hiciste una
        deprendencia con el Hmax'''
        if self.DF < self.espesor1:
            if self.Hmax <= (self.espesor1 - self.DF):
                co = cohesion1
            elif self.espesor1 < self.Hmax + self.DF <= self.espesor1 + self.espesor2:
                co = ((self.espesor1 - self.DF) * cohesion1 + (self.Hmax - (self.espesor1 - self.DF)) * cohesion2) / self.Hmax
            else:
                co = ((self.espesor1 - self.DF) * cohesion1 + self.espesor2 * cohesion2 + (
                        self.Hmax - (self.espesor1 - self.DF) - self.espesor2) * cohesion3) / self.Hmax
        elif self.espesor1 <= self.DF < self.espesor1 + self.espesor2:
            if self.Hmax <= (self.espesor1 + self.espesor2 - self.DF):
                co = cohesion2
            else:
                co = ((self.espesor2 + self.espesor1 - self.DF) * cohesion2 + (self.Hmax - (self.espesor1 + self.espesor2 - self.DF)) * cohesion3) / (
                    self.Hmax)
        else:
            co = cohesion3
        return co

    def sobrecarga(self, gama1, gama2, gama3):
        '''La sobrecarga debe ponderarse. No tiene dependencia con Hmax'''
        if self.DF <= self.espesor1:
            return gama1*self.DF
        elif self.espesor1 < self.DF <= self.espesor1 + self.espesor2:
            return gama1 * self.espesor1 + gama2 * (self.DF - self.espesor1)
        else:
            return (gama1 * self.espesor1 + gama2 * self.espesor2 + gama3 * (
                        self.DF - (self.espesor1 + self.espesor2)))

    def gamma(self, Hmax, gama1, gama2, gama3):
        ''' Este método viene conjunto con el de gamma de la librería peso_específico.
        TENER CUIDADO CON LOS GAMMAS. Se deja el Hmax porque en la práctica este método se ejecuta
        individualmente del método ángulo'''
        if self.DF < self.espesor1:
            if Hmax <= (self.espesor1 - self.DF):
                gama = gama1
            elif self.espesor1 < Hmax + self.DF <= self.espesor1 + self.espesor2:
                gama = ((self.espesor1 - self.DF) * gama1 + (Hmax - (self.espesor1 - self.DF)) * gama2) / Hmax
            else:
                gama = ((self.espesor1 - self.DF) * gama1 + self.espesor2 * gama2 + (
                            Hmax - (self.espesor1 - self.DF) - self.espesor2) * gama3) / Hmax
        elif self.espesor1 <= self.DF < self.espesor1 + self.espesor2:
            if Hmax <= (self.espesor1 + self.espesor2 - self.DF):
                gama = gama2
            else:
                gama = (((self.espesor1 + self.espesor2) - self.DF) * gama2 + (
                            Hmax - (self.espesor1 + self.espesor2 - self.DF)) * gama3) / Hmax
        else:
            gama = gama3
        return gama