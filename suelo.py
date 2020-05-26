class Suelo:

    def __init__(self, e, Gs, S, w, gama):
        self.e = e
        self.Gs = Gs
        self.S = S
        self.w = w
        self.gama = gama

    def calcular_gamma(self, e_c, Gs_c, S_c, w_c):
        '''Aquí se calcula el gama de acuerdo con cada estrato y parámetros dados'''
        if e_c == 1 and S_c == 1 and Gs_c == 1:
            Y = humedo1(self.e, self.Gs, self.S)  # humedo
        elif e_c == 1 and Gs_c == 1 and w_c == 0:
            Y = saturado(self.e, self.Gs) - 9.81  # sumergido
        elif e_c == 1 and Gs_c == 1 and w_c == 1:
            Y = humedo2(self.e, self.Gs, self.w)  # humedo
        else:
                Y = self.gama
            # info=crear(pes0)
            # info.label("No existe la combinación", 210,10)
        return Y

def humedo2(e, Gs, w):
    Vt = 1 + e
    Vs = 1
    Gama_w = 9.8  # kN/m^3
    Ws = (Gs * Gama_w) / Vs
    Gama_dry = Ws / Vt
    Gama_wet = Gama_dry + Gama_dry * w
    return Gama_wet

def humedo1(e, Gs, S):
    Vv = e
    Vt = 1 + e
    Vs = 1
    Vw = S * Vv
    Va = Vv - Vw
    gama_w = 9.8  # kN/m^3
    Ww = Vw * gama_w
    Ws = (Gs * gama_w) / Vs
    Wt = Ww + Ws
    gama_dry = Ws / Vt
    w = Ww / Ws
    gama_wet = gama_dry + gama_dry * w
    return gama_wet

def saturado(e, Gs):
    Vv = e
    Vt = 1 + e
    Vs = 1
    Vw = 1 * Vv
    Va = Vv - Vw
    Gama_w = 9.8  # kN/m^3
    Ww = Vw * Gama_w
    Ws = (Gs * Gama_w) / Vs
    Wt = Ww + Ws
    Gama_dry = Ws / Vt
    w = Ww / Ws
    Gama_saturated = Gama_dry + Gama_dry * w
    return Gama_saturated



