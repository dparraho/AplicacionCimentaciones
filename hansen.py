# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 17:50:02 2018

@author: Daniel Parra
"""
from tkinter import *
from tkinter import ttk
from math import tan, pi, exp, atan, sin, radians
from ponderado import Ponderado as pond
from suelo import Suelo as sl
from costos import Costos


# creando la ventana
ventana = Tk()
ventana.title("Cimentaciones")
ventana.geometry("1110x500")

# Creando las pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand='yes')
pes0 = ttk.Frame(notebook)  # pestaña 1
notebook.add(pes0, text='Hansen')

nombre_archivo = StringVar()
nombre_archivo.set("Hansen")
caso = StringVar()
caso.set("u")

e1 = DoubleVar()
e1.set(1.4)
Gs1 = DoubleVar()
Gs1.set(2.7)
S1 = DoubleVar()
S1.set(0.7)
w1 = DoubleVar()
gama1 = DoubleVar()
gama1.set(0)
c1 = DoubleVar()
c1.set(5)
fi_1 = DoubleVar()
fi_1.set(20)
check_e1 = IntVar()
check_e1.set(1)
check_Gs1 = IntVar()
check_Gs1.set(1)
check_S1 = IntVar()
check_S1.set(1)
check_w1 = IntVar()
espesor1 = DoubleVar()
espesor1.set(2)

e2 = DoubleVar()
e2.set(0.7)
Gs2 = DoubleVar()
Gs2.set(2.64)
S2 = DoubleVar()
w2 = DoubleVar()
gama2 = DoubleVar()
c2 = DoubleVar()
c2.set(7)
fi_2 = DoubleVar()
fi_2.set(28)
check_e2 = IntVar()
check_e2.set(1)
check_Gs2 = IntVar()
check_Gs2.set(1)
check_S2 = IntVar()
check_w2 = IntVar()
espesor2 = DoubleVar()
espesor2.set(4)

e3 = DoubleVar()
e3.set(0.6)
Gs3 = DoubleVar()
Gs3.set(2.64)
S3 = DoubleVar()
w3 = DoubleVar()
gama3 = DoubleVar()
c3 = DoubleVar()
c3.set(0)
fi_3 = DoubleVar()
fi_3.set(32)
check_e3 = IntVar()
check_e3.set(1)
check_Gs3 = IntVar()
check_Gs3.set(1)
check_S3 = IntVar()
check_w3 = IntVar()

B = DoubleVar()
B.set(2)
DF = DoubleVar()
DF.set(2)
l = DoubleVar()
l.set(23.28)

opcion = IntVar()
opcion.set(1)
conteliminar = StringVar()
datos = []

FM = DoubleVar()
FM.set(1.5)
fi_R = DoubleVar()
fi_R.set(0.5)
# FS_c=DoubleVar()
# FS_fi=DoubleVar()
Global = DoubleVar()

Mx = DoubleVar()
Mx.set(3500)
My = DoubleVar()
My.set(2800)
carga = DoubleVar()
carga.set(4200)
Beta = DoubleVar()

def hansen_Ngama(Nq, fi):
    '''Es una verificación propia de Hansen. Solo si el fi es cero'''
    if fi == 0:
        return -2 * sin(Beta.get())
    else:
        return 1.5 * (Nq - 1) * tan(radians(fi))

def hansen_Sc(Nq, Nc, B_prima, L_prima, fi):
    '''Es una verificación propia de Hansen. Solo si el fi es cero'''
    if fi == 0:
        Sc = 0.2 * B_prima / L_prima
    else:
        Sc = 1 + Nq * B_prima / (L_prima * Nc)
    return Sc

def hansen_Dc(fi, k):
    '''Es una verificación propia de Hansen. Solo si el fi es cero'''
    if fi == 0:
        return 0.4 * k
    else:
        return 1 + 0.4 * k

def k(Bi, df):
    '''Factor requerido en los coeficientes de Hansen, sus unidades son
    radianes'''
    if df / Bi <= 1:
        return df / Bi
    else:
        if 1 < df / Bi:
            return atan(df / Bi)

def verifica_Sq(Kp, fi):
    '''... más parámetros'''
    if fi == 0:
        Sq = 1
    elif fi > 10:
        Sq = round(1 + 0.1 * Kp * B.get() / L, 3)
    return Sq

def verifica_Dq(Kp, fi):
    '''...más parámetros'''
    if fi == 0:
        Dq = 1
    elif fi > 10:
        Dq = round((1 + 0.1 * (Kp ** 0.5) * DF.get() / B.get()), 3)
    return Dq

def gama_ponderado(df, Hmax):
    ''' Dada la poca practicidad de incluir los checking para las relaciones
     gravimétricas, que calculan el gamma, en una clase, decidí dejar esta función.
     Completamente insatisfecho '''
    a = sl(e1.get(), Gs1.get(), S1.get(), w1.get(), gama1.get())
    a = a.calcular_gamma(check_e1.get(), check_Gs1.get(), check_S1.get(), check_w1.get())

    b = sl(e2.get(), Gs2.get(), S2.get(), w2.get(), gama2.get())
    b = b.calcular_gamma(check_e2.get(), check_Gs2.get(), check_S2.get(), check_w2.get())

    c = sl(e3.get(), Gs3.get(), S3.get(), w3.get(), gama3.get())
    c = c.calcular_gamma(check_e3.get(), check_Gs3.get(), check_S3.get(), check_w3.get())

    gama1.set(a)
    gama2.set(b)
    gama3.set(c)
    return pond(espesor1.get(), espesor2.get(), df, B.get()).gamma(Hmax, a, b, c)

class crear:
    '''Esta clase es con el propósito de facilitar la edición de los parámetros en cajas,
    labels, etc.'''
    def __init__(self, pes):
        self.pes = pes

    def caja(self, TextV, Width, x, y):  # (Variable, espesor, posición x, posición y)
        caja = Entry(self.pes, textvariable=TextV, width=Width).place(x=x, y=y)

    def label(self, Text, x, y):
        label = Label(self.pes, text=Text).place(x=x, y=y)

    def boton(self, Text, comando, x, y, bg="#9ACD32", fg="black"):
        boton = Button(self.pes, text=Text, command=comando, bg=bg, fg=fg).place(x=x, y=y)

    def botonC(self, Text, TextV, x, y):
        botonC = ttk.Checkbutton(self.pes, text=Text, variable=TextV).place(x=x, y=y)

def iniciarArchivo():
    if nombre_archivo == "":
        nombre_archivo == "Nuevo"
    archivo = open(nombre_archivo.get() + ".txt", "a")
    archivo.close()

def cargar():
    archivo = open(nombre_archivo.get() + ".txt", "r")
    linea = archivo.readline()
    if linea:
        while linea:
            if linea[-1] == "\n":
                linea = linea[:-1]
            datos.append(linea)
            linea = archivo.readline()  # Readline have memory
    archivo.close()

def escribirContacto():
    archivo = open(nombre_archivo.get() + ".txt", "w")
    datos.sort()
    for elemento in datos:
        archivo.write(elemento + "\n")
    archivo.close()

def consultar():
    r = Text(pes0, width=135, height=10, relief="sunken", borderwidth=2)
    datos.sort()
    valores = []
    r.insert(INSERT, "DF\tHmax\t\u03A6\t\u03b3\tCohe\tB\tL\tB'\tL'\tsolicitacion\t\t"
                     "Admisible\t\tCosto\t\tExcentricidad\n")
    scrollb = ttk.Scrollbar(pes0, command=r.yview)
    scrollb.place(x=1080, y=300)
    r['yscrollcommand'] = scrollb.set
    for elemento in datos:
        arreglo = elemento.split("$")
        valores.append(arreglo[0])
        r.insert(INSERT, arreglo[0] + "\t" + arreglo[1] + "\t" + arreglo[2] + "\t"
                 + arreglo[3] + "\t" + arreglo[4] + "\t" + arreglo[5] + "\t"
                 + arreglo[6] + "\t" + arreglo[7] + "\t" + arreglo[8] + "\t"
                 + arreglo[12] + "\t\t" + arreglo[13] + "\t\t" + arreglo[14] + "\t\t"
                 + arreglo[15] + "\n")
        # "\t"+arreglo[12]+"\t"+arreglo[13]+"\t"+arreglo[14]+"\t"+arreglo[15]+"\t"+arreglo[16]+"\t"+arreglo[17]+"\n")
    r.place(x=10, y=300)
    spinTelefono = Spinbox(pes0, value=valores, textvariable=conteliminar).place(x=920, y=50)
    if not datos:
        spinTelefono = Spinbox(pes0, value=valores, textvariable=conteliminar).place(x=920, y=50)
    r.config(state=DISABLED)
    return valores

def guardar():  # SI TENGO B
    ponderar = pond(espesor1.get(), espesor2.get(), DF.get(), B.get())
    fi, Hmax = ponderar.angulo(fi_1.get(), fi_2.get(), fi_3.get())
    Coh = ponderar.cohesion(c1.get(), c2.get(), c3.get())
    gam = gama_ponderado(DF.get(), Hmax)
    q = ponderar.sobrecarga(gama1.get(), gama2.get(), gama3.get())
    Nq = exp(pi * tan(radians(fi))) * tan(radians(45 + (fi / 2))) ** 2
    Nc = (Nq - 1) / tan(radians(fi))
    Ngama = hansen_Ngama(Nq, fi)
    Dgama = 1  # for all fi
    Bi = B.get()
    ki = k(Bi, DF.get())
    Dq = 1 + 2 * tan(radians(fi)) * (1 - sin(radians(fi))) ** 2 * ki
    Dc = hansen_Dc(fi, ki)
    eyi = Mx.get() / carga.get()
    exi = My.get() / carga.get()
    fi_i = fi_R.get()
    B_prima = Bi - 2 * exi
    L_prima = (-1) * (Coh * Dc * B_prima * Nq + q * Nq * Dq * sin(radians(fi)) * B_prima - 0.2 * gam * (
                B_prima ** 2) * Ngama * Dgama - FM.get() * carga.get() / (B_prima * fi_R.get())) / (
                Coh * Dc * Nc + q * Nq * Dq + 0.5 * gam * B_prima * Ngama * Dgama)  # Despejado
    Sc = hansen_Sc(Nq, Nc, B_prima, L_prima, fi)
    Sq = 1 + (B_prima / L_prima * sin(radians(fi)))
    Sgama = 1 - 0.4 * B_prima / L_prima
    total1 = Coh * Nc * Sc * Dc
    total2 = 0.5 * B_prima * gam * Ngama * Sgama * Dgama
    total3 = q * Nq * Sq * Dq
    ultima = total1 + total2 + total3
    admisible = ultima * fi_i / FM.get()
    L = L_prima + 2 * eyi
    solicitacion = carga.get()/(L_prima*B_prima)
    precios = Costos()
    exc, con, lle, costo = precios.calcular(L, Bi, DF.get())
    if Bi / 6 >= exi and L / 6 >= eyi:
        restriccion = "Cumple"
    else:
        restriccion = "No cumple"
    datos.append(str(round(DF.get(), 3)) + "$" + str(round(Hmax, 3)) + "$" + str(round(fi, 3)) + "$"
                 + str(round(gam, 3)) + "$" + str(round(Coh, 3)) + "$" + str(round(Bi, 3)) + "$"
                 + str(round(abs(L), 3)) + "$" + str(round(B_prima, 3)) + "$" + str(round(L_prima, 3)) + "$"
                 + str(precios.multiplo(exc)) + "$" + str(precios.multiplo(con)) + "$" + str(precios.multiplo(lle))
                 + "$" + str(round(solicitacion, 3)) + "$" + str(round(admisible, 3)) + "$" + str(precios.multiplo(costo))
                 + "$" + restriccion)
    escribirContacto()
    caso.set("")
    consultar()

def bisection(f, a, b, tol):
    c = (a+b)/2.0
    while (b-a)/2.0 > tol:
        if f(c) == 0:
            return c
        elif f(a)*f(c) < 0:
            b = c
        else:
            a = c
        c = (a+b)/2.0
    return c

def guardar2():  # SI TENGO L
    # c=10
    # L=25
    carg, df, fi_i, L, fm = carga.get(), DF.get(), fi_R.get(), l.get(), FM.get()
    esp1, esp2 = espesor1.get(), espesor2.get()
    eyi = Mx.get() / carga.get()
    exi = My.get() / carga.get()
    L_prima = l.get() - 2 * eyi
    Bi = 2 * exi
    solicitacion = 1
    admisible = 0
    while round(solicitacion, 1) != round(admisible, 1):
        Bi += 0.0001
        B_prima = Bi - 2 * exi
        ponderar = pond(esp1, esp2, df, Bi)
        fi, Hmax = ponderar.angulo(fi_1.get(), fi_2.get(), fi_3.get())
        gam = gama_ponderado(df, Hmax)
        Coh = ponderar.cohesion(c1.get(), c2.get(), c3.get())
        q = ponderar.sobrecarga(gama1.get(), gama2.get(), gama3.get())
        ki = k(Bi, df)
        Dc = hansen_Dc(fi, ki)
        Dq = 1 + 2 * tan(radians(fi)) * (1 - sin(radians(fi))) ** 2 * ki
        Nq = exp(pi * tan(radians(fi))) * tan(radians(45 + (fi / 2))) ** 2
        Nc = (Nq - 1) / tan(radians(fi))
        Ngama = hansen_Ngama(Nq, fi)
        Dgama = 1  # for all fi
        Sc = hansen_Sc(Nq, Nc, B_prima, L_prima, fi)
        Sq = 1 + (B_prima / L_prima * sin(radians(fi)))
        Sgama = 1 - 0.4 * B_prima / L_prima
        total1 = Coh * Nc * Sc * Dc
        total2 = 0.5 * B_prima * gam * Ngama * Sgama * Dgama
        total3 = q * Nq * Sq * Dq
        ultima = total1 + total2 + total3
        admisible = ultima * fi_i / fm
        solicitacion = carg / (B_prima * L_prima)
        if Bi > 20:
            break
    precios = Costos()
    exc, con, lle, costo = precios.calcular(L, Bi, DF.get())
    if Bi / 6 >= exi and L / 6 >= eyi:
        restriccion = "Cumple"
    else:
        restriccion = "No cumple"
    datos.append(str(round(DF.get(), 3)) + "$" + str(round(Hmax, 3)) + "$" + str(round(fi, 3)) + "$"
                 + str(round(gam, 3)) + "$" + str(round(Coh, 3)) + "$" + str(round(Bi, 3)) + "$"
                 + str(round(abs(L), 3)) + "$" + str(round(B_prima, 3)) + "$" + str(round(L_prima, 3)) + "$"
                 + str(precios.multiplo(exc)) + "$" + str(precios.multiplo(con)) + "$" + str(precios.multiplo(lle)) + "$"
                 + str(round(solicitacion, 3)) + "$" + str(round(admisible, 3)) + "$" + str(precios.multiplo(costo)) + "$"
                 + restriccion)
    escribirContacto()
    caso.set("")
    consultar()

def guardar3():# No tengo DF
    carg, Bi, L, fi_i, fm = carga.get(), B.get(), l.get(), fi_R.get(), FM.get()
    esp1, esp2 = espesor1.get(), espesor2.get()
    fi1, fi2, fi3 = fi_1.get(), fi_2.get(), fi_3.get()
    c_1, c_2, c_3 = c1.get(), c2.get(), c3.get()
    eyi = Mx.get() / carga.get()
    exi = My.get() / carga.get()
    L_prima = l.get() - 2 * eyi
    B_prima = Bi - 2 * exi
    solicitacion = 1
    admisible = 0
    df = 0.0001
    while round(solicitacion, 2) != round(admisible, 2):
        df += 0.0001
        ponderar = pond(esp1, esp2, df, Bi)
        fi, Hmax = ponderar.angulo(fi1, fi2, fi3)
        Coh = ponderar.cohesion(c_1, c_2, c_3)
        gam = gama_ponderado(df, Hmax)
        q = ponderar.sobrecarga(gama1.get(), gama2.get(), gama3.get())
        ki = k(Bi, df)
        Dc = hansen_Dc(fi, ki)
        Dq = 1 + 2 * tan(radians(fi)) * (1 - sin(radians(fi))) ** 2 * ki
        Nq = exp(pi * tan(radians(fi))) * tan(radians(45 + (fi / 2))) ** 2
        Nc = (Nq - 1) / tan(radians(fi))
        Ngama = hansen_Ngama(Nq, fi)
        Dgama = 1  # for all fi
        # L_prima=(-1)*(Coh*Dc*B_prima*Nq+q*Nq*Dq*sin(radianes(fi))*B_prima-0.2*gam*(B_prima**2)*Ngama*Dgama-FM.get()*carga.get()/(B_prima*fi_R.get()))/(Coh*Dc*Nc+q*Nq*Dq+0.5*gam*B_prima*Ngama*Dgama)
        Sc = hansen_Sc(Nq, Nc, B_prima, L_prima, fi)
        Sq = 1 + (B_prima / L_prima * sin(radians(fi)))
        Sgama = 1 - 0.4 * B_prima / L_prima
        total1 = Coh * Nc * Sc * Dc
        total2 = 0.5 * B_prima * gam * Ngama * Sgama * Dgama
        total3 = q * Nq * Sq * Dq
        ultima = total1 + total2 + total3
        admisible = ultima * fi_i / fm
        solicitacion = carg / (B_prima * L_prima)
        if df > 20:
            break
    precios = Costos()
    exc, con, lle, costo = precios.calcular(L, Bi, DF.get())
    if Bi / 6 >= exi and L / 6 >= eyi:
        restriccion = "Cumple"
    else:
        restriccion = "No cumple"
    datos.append(str(round(df, 3)) + "$" + str(round(Hmax, 3)) + "$" + str(round(fi, 3)) + "$"
                 + str(round(gam, 3)) + "$" + str(round(Coh, 3)) + "$" + str(round(Bi, 3)) + "$"
                 + str(round(abs(L), 3)) + "$" + str(round(B_prima, 3)) + "$" + str(round(L_prima, 3)) + "$"
                 + str(precios.multiplo(exc)) + "$" + str(precios.multiplo(con)) + "$" + str(precios.multiplo(lle)) + "$"
                 + str(round(solicitacion, 3)) + "$" + str(round(admisible, 3)) + "$" + str(precios.multiplo(costo)) + "$"
                 + restriccion)
    escribirContacto()
    caso.set("")
    consultar()

def mostrar():
    consultar()

def eliminar():
    eliminado = conteliminar.get()
    for elemento in datos[:]:
        arreglo = elemento.split("$")
        if eliminado == arreglo[0]:
            datos.remove(elemento)
    escribirContacto()
    consultar()


def nuevo_archivo():
    iniciarArchivo()
    cargar()
    consultar()

########################################### PRIMER ESTRATO ###############################
titulo = Label(pes0, text="Estrato 1").place(x=320, y=30)
para_e = crear(pes0)
para_e.label("e :", 320, 60)
para_e.caja(e1, 7, 345, 60)
para_e.botonC("", check_e1, 300, 60)

para_Gs = crear(pes0)
para_Gs.label("Gs:", 320, 85)
para_Gs.caja(Gs1, 7, 345, 85)
para_Gs.botonC("", check_Gs1, 300, 85)

para_S = crear(pes0)
para_S.label("S:", 320, 110)
para_S.caja(S1, 7, 345, 110)
para_S.botonC("", check_S1, 300, 110)

para_w = crear(pes0)
para_w.label("w:", 320, 135)
para_w.caja(w1, 7, 345, 135)
para_w.botonC("", check_w1, 300, 135)

para_gama = crear(pes0)
para_gama.label("\u03b3:", 320, 160)
for_gama = Entry(pes0, textvariable=gama1, width=7).place(x=345, y=160)

para_cohesion = crear(pes0)
para_cohesion.label("C:", 320, 185)
para_cohesion.caja(c1, 7, 345, 185)

para_fi = crear(pes0)
para_fi.label("\u03d5:", 320, 210)
para_fi.caja(fi_1, 7, 345, 210)

para_D1 = crear(pes0)
para_D1.label("D :", 320, 235)
para_D1.caja(espesor1, 7, 345, 235)

######################################### SEGUNDO ESTRATO ############################################
titulo = Label(pes0, text="Estrato 2").place(x=450, y=30)
para_e = crear(pes0)
para_e.label("e :", 450, 60)
para_e.caja(e2, 7, 475, 60)
para_e.botonC("", check_e2, 430, 60)

para_Gs = crear(pes0)
para_Gs.label("Gs:", 450, 85)
para_Gs.caja(Gs2, 7, 475, 85)
para_Gs.botonC("", check_Gs2, 430, 85)

para_S = crear(pes0)
para_S.label("S:", 450, 110)
para_S.caja(S2, 7, 475, 110)
para_S.botonC("", check_S2, 430, 110)

para_w = crear(pes0)
para_w.label("w:", 450, 135)
para_w.caja(w2, 7, 475, 135)
para_w.botonC("", check_w2, 430, 135)

para_gama = crear(pes0)
para_gama.label("\u03b3:", 450, 160)
for_gama = Entry(pes0, textvariable=gama2, width=7).place(x=475, y=160)

para_cohesion = crear(pes0)
para_cohesion.label("C:", 450, 185)
para_cohesion.caja(c2, 7, 475, 185)

para_fi = crear(pes0)
para_fi.label("\u03d5:", 450, 210)
para_fi.caja(fi_2, 7, 475, 210)

para_D2 = crear(pes0)
para_D2.label("D :", 450, 235)
para_D2.caja(espesor2, 7, 475, 235)

######################################### TERCER ESTRATO ############################################
titulo = Label(pes0, text="Estrato 3").place(x=580, y=30)
para_e = crear(pes0)
para_e.label("e :", 580, 60)
para_e.caja(e3, 7, 605, 60)
para_e.botonC("", check_e3, 560, 60)

para_Gs = crear(pes0)
para_Gs.label("Gs:", 580, 85)
para_Gs.caja(Gs3, 7, 605, 85)
para_Gs.botonC("", check_Gs3, 560, 85)

para_S = crear(pes0)
para_S.label("S:", 580, 110)
para_S.caja(S3, 7, 605, 110)
para_S.botonC("", check_S3, 560, 110)

para_w = crear(pes0)
para_w.label("w:", 580, 135)
para_w.caja(w3, 7, 605, 135)
para_w.botonC("", check_w3, 560, 135)

para_gama = crear(pes0)
para_gama.label("\u03b3:", 580, 160)
for_gama = Entry(pes0, textvariable=gama3, width=7).place(x=605, y=160)

para_cohesion = crear(pes0)
para_cohesion.label("C:", 580, 185)
para_cohesion.caja(c3, 7, 605, 185)

para_fi = crear(pes0)
para_fi.label("\u03d5:", 580, 210)
para_fi.caja(fi_3, 7, 605, 210)

para_carga = crear(pes0)
para_carga.label("Carga (kN): ", 30, 60)
para_carga.caja(carga, 8, 100, 60)

para_L = crear(pes0)
para_L.label("L : ", 30, 90)
para_L.caja(l, 8, 100, 90)

para_B = crear(pes0)
para_B.label("B : ", 30, 120)
para_B.caja(B, 8, 100, 120)

para_DF = crear(pes0)
para_DF.label("DF : ", 30, 150)
para_DF.caja(DF, 8, 100, 150)

para_Mx = crear(pes0)
para_Mx.label("Mx (kN) : ", 30, 180)
para_Mx.caja(Mx, 8, 100, 180)

para_My = crear(pes0)
para_My.label("My (kN) : ", 30, 210)
para_My.caja(My, 8, 100, 210)
consultar()

para_nombre_archivo = crear(pes0)
para_nombre_archivo.caja(nombre_archivo, 8, 30, 30)
para_nombre_archivo.boton("Cargar/abrir", nuevo_archivo, 100, 25, bg="#bebebe")

para_calcular = crear(pes0)
para_calcular.boton("Calcular DF", guardar3, 1005, 180, bg="#009", fg="white")

para_calcular = crear(pes0)
para_calcular.boton("Calcular B", guardar2, 1005, 210, bg="#009", fg="white")

para_calcular = crear(pes0)
para_calcular.boton("Calcular L", guardar, 1005, 240, bg="#009", fg="white")

para_mostrar = crear(pes0)
para_mostrar.boton("Mostrar resultados", mostrar, 950, 270, bg="gray", fg="white")

spinTelefono = Spinbox(pes0, textvariable=conteliminar).place(x=920, y=50)
botonEliminar = Button(pes0, text="Eliminar", command=eliminar, bg="#009", fg="white").place(x=1000, y=80)

Radio_LRFD = Radiobutton(pes0, text="LRFD", value=1,
                         variable=opcion, activebackground="#009").place(x=30, y=260)
para_LRFD1 = crear(pes0)
para_LRFD1.label("F.M.", 110, 243)
para_LRFD1.caja(FM, 8, 100, 260)
para_LRFD2 = crear(pes0)
para_LRFD2.label("\u03d5", 185, 243)
para_LRFD2.caja(fi_R, 8, 170, 260)

para_creditos = crear(pes0)
para_creditos.label("Desarrollado por: Daniel Parra H.", 900, 0)

ventana.mainloop()
