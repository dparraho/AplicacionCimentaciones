
class Costos:
    def __init__(self, exc_NF = 200000, exc = 100000, concret = 1200000, llen = 150000):
        self.exc_NF = exc_NF
        self.exc = exc
        self.concret = concret
        self.llen = llen

    def calcular(self, L, B, DF):  # $/m^3
        concreto = ((DF - 1) * 1 * 1 + B * L * 1) * self.concret
        if DF > 2:
            excavacion = (((DF - 2) - 1) * B * L + ((DF - 2) ** 2) * (0.5) * L + ((DF - 2) ** 2) * (
                0.5) * B + (DF - 2) ** 3 / 3) * self.exc +((DF - 1) * B * L + (DF ** 2) * (0.5) * L + (DF ** 2) * (
                0.5) * B + DF ** 3 / 3 - (((DF - 2) - 1) * B * L + ((DF - 2) ** 2) * (0.5) * L + ((DF - 2) ** 2) * (
                0.5) * B + (DF - 2) ** 3 / 3)) * self.exc
        else:
            excavacion = ((DF - 1) * B * L + (DF ** 2) * (0.5) * L + (DF ** 2) * (
                0.5) * B + DF ** 3 / 3) * self.exc
        lleno = ((DF - 1) * B * L + (DF ** 2) * (0.5) * L + (DF ** 2) * (0.5) * B + DF ** 3 / 3
                 - ((DF - 1) * 1 * 1 + B * L * 1)) * self.llen
        costo = concreto + excavacion + lleno
        return excavacion, concreto, lleno, costo
    def multiplo(self, num):
        return multiplo_100mil(num)

def multiplo_100mil(num): # Múltiplo de $100.000 COP para redondear los costos
    residuo = num % 100000
    cociente = num//100000
    if residuo > 40000:
        return round(100000*cociente+100000)
    else:
        return round(100000*cociente)