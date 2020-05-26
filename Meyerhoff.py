# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 20:59:14 2018

@author: Daniel Parra
"""

from tkinter import *
from tkinter import ttk
from math import sqrt
from math import tan, pi, exp, radians
from ponderado import Ponderado as Pond
from suelo import Suelo as Soil
from costos import Costos

# Creando la ventana
ventana = Tk()
ventana.title("Cimentaciones")
ventana.geometry("1110x500")

# Creando las pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand='yes')
pes_cero = ttk.Frame(notebook)  # pestaña 1
# pes1=ttk.Frame(notebook)#pestaña 1
notebook.add(pes_cero, text='Meyerhoff')
# notebook.add(pes1, text='Cargas')

nombre_archivo = StringVar()
caso = StringVar()
e_one = DoubleVar()
e_one.set(1.4)
Gs_one = DoubleVar()
Gs_one.set(2.7)
S_one = DoubleVar()
S_one.set(0.7)
w_one = DoubleVar()
gama_one = DoubleVar()
gama_one.set(18)
c_one = DoubleVar()
c_one.set(10)
fi_one = DoubleVar()
fi_one.set(26)
check_e1 = IntVar()
check_e1.set(0)
check_Gs1 = IntVar()
check_Gs1.set(0)
check_S1 = IntVar()
check_S1.set(0)
check_w1 = IntVar()
espesor_one = DoubleVar()
espesor_one.set(1.5)

e_two = DoubleVar()
e_two.set(0.7)
Gs_two = DoubleVar()
Gs_two.set(2.64)
S_two = DoubleVar()
w_two = DoubleVar()
gama_two = DoubleVar()
gama_two.set(20 - 9.81)
c_two = DoubleVar()
c_two.set(10)
fi_two = DoubleVar()
fi_two.set(26)
check_e2 = IntVar()
check_e2.set(0)
check_Gs2 = IntVar()
check_Gs2.set(0)
check_S2 = IntVar()
check_w2 = IntVar()
espesor_two = DoubleVar()
espesor_two.set(100)

e_three = DoubleVar()
e_three.set(0.6)
Gs_three = DoubleVar()
Gs_three.set(2.64)
S_three = DoubleVar()
w_three = DoubleVar()
gama_three = DoubleVar()
c_three = DoubleVar()
c_three.set(0)
fi_three = DoubleVar()
fi_three.set(32)
check_e3 = IntVar()
check_e3.set(0)
check_Gs3 = IntVar()
check_Gs3.set(0)
check_S3 = IntVar()
check_w3 = IntVar()

# caso=StringVar()
B = DoubleVar()
B.set(3.2)
DF = DoubleVar()
DF.set(0.5)
l = DoubleVar()
l.set(9.02)

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
Mx.set(0)
My = DoubleVar()
My.set(0)
carga = DoubleVar()
carga.set(2800)
Beta = DoubleVar()

nombre_archivo.set("Meyerhoff")
caso.set("u")

def gama_ponderado(df, Hmax):
    '''Dada la poca practicidad de incluir los checking para las relaciones
     gravimétricas, que calculan el gamma, en una clase, decidí dejar esta función.
     Completamente insatisfecho'''
    a = Soil(e_one.get(), Gs_one.get(), S_one.get(), w_one.get(), gama_one.get())
    a = a.calcular_gamma(check_e1.get(), check_Gs1.get(), check_S1.get(), check_w1.get())

    b = Soil(e_two.get(), Gs_two.get(), S_two.get(), w_two.get(), gama_two.get())
    b = b.calcular_gamma(check_e2.get(), check_Gs2.get(), check_S2.get(), check_w2.get())

    c = Soil(e_three.get(), Gs_three.get(), S_three.get(), w_three.get(), gama_three.get())
    c = c.calcular_gamma(check_e3.get(), check_Gs3.get(), check_S3.get(), check_w3.get())
    gama_one.set(a)
    gama_two.set(b)
    gama_three.set(c)
    return Pond(espesor_one.get(), espesor_two.get(), df, B.get()).gamma(Hmax, a, b, c)

def multiplo100_mil(num):#Múltiplo de $100.000 COP para redondear los costos
    residuo = num % 100000
    cociente = num // 100000
    if residuo > 40000:
        return round(100000*cociente+100000)
    else:
        return round(100000*cociente)

def verifica_dq(Kp, fi, b):
    if fi == 0:
        dq = 1
        return dq
    elif fi > 10:
        dq = 1 + 0.1 * (sqrt(Kp)) * DF.get() / b
        return dq
    return None

class crear:#Esta clase es con el propósito de facilitar la edición de los parámetros en cajas,labels, etc.
    def __init__(self, pes):
        self.pes = pes
    def caja(self,TextV, Width, x, y):#(Variable, espesor, posición x, posición y)
        caja = Entry(self.pes, textvariable=TextV, width=Width).place(x=x, y=y)
    def label(self, Text, x, y):
        label = Label(self.pes,text=Text).place (x=x, y=y)
    def boton(self, Text, comando, x, y, bg="#9ACD32", fg="black"):
        boton = Button(self.pes, text=Text, command=comando,bg=bg,fg=fg).place(x=x, y=y)
    def botonC(self, Text, TextV, x, y):
        botonC = ttk.Checkbutton(self.pes,text=Text,variable=TextV).place(x=x,y=y)
        
def iniciar_archivo():
    if nombre_archivo == "":
        nombre_archivo == "Nuevo"
    archivo = open(nombre_archivo.get()+".txt", "a")
    archivo.close()

def cargar():
    if nombre_archivo == False:
        nombre_archivo == ""
    archivo = open(nombre_archivo.get()+".txt","r")
    linea = archivo.readline()
    if linea:
        while linea:
            if linea[-1] == "\n":
                linea = linea[:-1]
            datos.append(linea)
            linea = archivo.readline()
    archivo.close()

def escribir_contacto():
    if nombre_archivo=="":
        nombre_archivo=="Nuevo"
    archivo=open(nombre_archivo.get()+".txt","w")
    datos.sort()
    for elemento in datos:
        archivo.write(elemento+"\n")
    archivo.close()
  
def consultar():
    r = Text(pes_cero, width=135, height=10, relief="sunken", borderwidth=2)
    datos.sort()
    valores = []
    # r.insert(INSERT,"Caso\tC\tNc\tSc\tDc\tTotal\t\u03b3\tN\u03b3\tS\u03b3\tD\u03b3\tTotal\tq\tNq\tSq\tDq\tTotal\tÚltima\tAdmisible\n")
    r.insert(INSERT, "DF\t\u03b3\tfi\tHmax\tCohe\tB\tL\tUltima\t\tAdmisible\n")
    scrollb = ttk.Scrollbar(pes_cero, command=r.yview)
    scrollb.place(x=1080, y=300)
    r['yscrollcommand'] = scrollb.set
    for elemento in datos:
        arreglo = elemento.split("$")
        valores.append(arreglo[0])
        r.insert(INSERT, arreglo[0] + "\t" + arreglo[1] + "\t" + arreglo[2] + "\t"
                        + arreglo[3] + "\t" + arreglo[4] + "\t" + arreglo[5] + "\t"
                        + arreglo[6] + "\t" + arreglo[7] + "\t\t" + arreglo[8] + "\t"
                        + arreglo[9] + "\n")
                 #"\t"+arreglo[12]+"\t"+arreglo[13]+"\t"+arreglo[14]+"\t"+arreglo[15]+"\t"+arreglo[16]+"\t"+arreglo[17]+"\n")
    r.place(x=10, y=300)
    spinTelefono = Spinbox(pes_cero, value=valores, textvariable=conteliminar).place(x=920, y=50)
    if not datos:
        spinTelefono = Spinbox(pes_cero, value=valores, textvariable=conteliminar).place(x=920, y=50)
    r.config(state=DISABLED)
    return valores

#def costos(L,B):  # $/m^3
#    concreto = ((DF.get()-1)*1*1+B*L*1)*1200000
#    if DF.get() > 2:
#        excavacion = (((DF.get()-2)-1)*B*L + (DF.get() - 2)**2*0.5*L+((DF.get() - 2)**2)*0.5*B
#                      + (DF.get()-2)**3/3)*200000 + ((DF.get()-1)*B*L+DF.get()**2*0.5*L
#                      + DF.get()**2*0.5*B + DF.get()**3/3 - (((DF.get()-2)-1)*B*L
#                      + ((DF.get()-2)**2)*0.5*L+((DF.get()-2)**2)*0.5*B+(DF.get()-2)**3/3))*100000
#    else:
#        excavacion = ((DF.get()-1)*B*L+(DF.get()**2)*(0.5)*L+(DF.get()**2)*(0.5)*B+DF.get()**3/3)*100000
#    lleno = ((DF.get()-1)*B*L+(DF.get()**2)*(0.5)*L+(DF.get()**2)*(0.5)*B+DF.get()**3/3-((DF.get()
#              -1)*1*1+B*L*1))*150000
#    costo = concreto + excavacion + lleno
#    return excavacion, concreto, lleno, costo

def guardar():  # hallar L
    ponderar = Pond(espesor_one.get(), espesor_two.get(), DF.get(), B.get())
    fi, Hmax = ponderar.angulo(fi_one.get(), fi_two.get(), fi_three.get())
    Coh = ponderar.cohesion(c_one.get(), c_two.get(), c_three.get())
    gam = gama_ponderado(DF.get(), Hmax)
    q = ponderar.sobrecarga(gama_one.get(), gama_two.get(), gama_three.get())
    Cas = caso.get()
    df, b, fm, fir, carg = DF.get(), B.get(), FM.get(), fi_R.get(), carga.get()
    Kp = tan(radians(45 + fi / 2)) ** 2
    Nq = exp(pi * tan(radians(fi))) * tan(radians(45 + (fi / 2))) ** 2
    Ngama = (Nq-1)*tan(radians(1.4 * fi))
    Nc = (Nq-1)/tan(radians(fi))
    L = 0
    Dq = verifica_dq(Kp, fi, b)
    Dgama = verifica_dq(Kp, fi, b)
    solicitacion = 1
    ultima = 0
    while round(solicitacion, 3) != round(ultima*fir/fm, 3):
        L += 0.00001
        Sc = 1+0.2*Kp*b/L
        Dc = 1+0.2*sqrt(Kp)*df/b
        Sq = 1+0.1*Kp*b/L  # aquí existe una verificación, se omite
        Sgama = 1+0.1*Kp*b/L
        total1 = Coh*Nc*Sc*Dc
        total2 = 0.5*b*gam*Ngama*Sgama*Dgama
        total3 = q*Nq*Sq*Dq
        ultima = total1+total2+total3
        solicitacion = carg/(b*L)
        if L > 20:
            break
    precios = Costos()
    exc, con, lle, cos = precios.calcular(L, b, df)
    admisible = ultima*fir/fm
    datos.append(str(round(DF.get(), 3)) + "$" + str(round(gam, 3)) + "$"+str(round(fi, 3)) + "$"
                 + str(round(Hmax, 3)) + "$" + str(round(Coh, 3)) + "$" + str(round(b, 3)) + "$"
                 + str(round(abs(L), 3)) + "$" + str(round(solicitacion, 3)) + "$"+str(round(admisible, 3)) + "$")
    escribir_contacto()
    caso.set("")
    gama_three.set(0)
    consultar()

def guardar2(): # Hallar B
    b = 0
    df, cas, fm, fir, carg, L, esp1 = DF.get(), caso.get(), FM.get(), fi_R.get(), carga.get(), l.get(), espesor_one.get()
    esp2 = espesor_two.get()
    solicitacion = 1
    admisible = 0
    while round(solicitacion, 1) != round(admisible, 1):
        b += 0.0001
        ponderar = Pond(esp1, esp2, df, b)
        fi, Hmax = ponderar.angulo(fi_one.get(), fi_two.get(), fi_three.get())
        gam = gama_ponderado(df, Hmax)
        Coh = ponderar.cohesion(c_one.get(), c_two.get(), c_three.get())
        q = ponderar.sobrecarga(gama_one.get(), gama_two.get(), gama_three.get())
        Kp = tan(radians(45 + fi / 2)) ** 2
        Nq = exp(pi * tan(radians(fi))) * tan(radians(45 + (fi / 2))) ** 2
        Ngama = (Nq-1)*tan(radians(1.4 * fi))
        Nc = (Nq-1)/tan(radians(fi))
        Dq = 1+0.1*(sqrt(Kp))*df/b
        Dgama = Dq
        Sc = 1+0.2*Kp*b/L
        Dc = 1+0.2*sqrt(Kp)*df/b
        Sq = 1+0.1*Kp*b/L  # aquí existe una verificación, se omite
        Sgama = 1+0.1*Kp*b/L
        total1 = Coh*Nc*Sc*Dc
        total2 = 0.5*b*gam*Ngama*Sgama*Dgama
        total3 = q*Nq*Sq*Dq
        ultima = total1+total2+total3
        admisible = ultima*fir/fm
        solicitacion = carg/(b*L)
        if b >= 20:
            break
    admisible = ultima*fir/fm
    datos.append(str(round(DF.get(), 3)) + "$" +str(round(gam, 3)) + "$" +str(round(fi, 3))+ "$"
                 + str(round(Hmax, 3)) + "$" + str(round(Coh, 3)) + "$" +str(round(b, 3)) + "$"
                 + str(round(L, 3)) + "$" + str(round(solicitacion, 3)) + "$" + str(round(admisible, 3)) + "$")
    escribir_contacto()
    caso.set("")
    consultar()
    
def guardar3(): # Hallar DF
    b, Cas, fm, fir, carg, L = B.get(), caso.get(), FM.get(), fi_R.get(), carga.get(), l.get()
    esp1, esp2 = espesor_one.get(), espesor_two.get()
    fi1, fi2, fi3 = fi_one.get(), fi_two.get(), fi_three.get()
    c_1, c_2, c_3 = c_one.get(), c_two.get(), c_three.get()
    df = -0.0001
    solicitacion = 1
    ultima = 0
    while round(solicitacion, 1) != round(ultima*fir/fm, 1):
        df += 0.0001
        ponderar = Pond(esp1, esp2, df, b)
        fi, Hmax = ponderar.angulo(fi1, fi2, fi3)
        Coh = ponderar.cohesion(c_1, c_2, c_3)
        gam = gama_ponderado(df, Hmax)
        q = ponderar.sobrecarga(gama_one.get(), gama_two.get(), gama_three.get())
        Kp = tan(radians(45 + fi / 2)) ** 2
        Nq = exp(pi * tan(radians(fi))) * tan(radians(45 + (fi / 2))) ** 2
        Ngama = (Nq-1)*tan(radians(1.4 * fi))
        Nc = (Nq-1)/tan(radians(fi))
        Dq = 1+0.1*(sqrt(Kp))*df/b
        Dgama = Dq
        Sc = 1+0.2*Kp*b/L
        Dc = 1+0.2*sqrt(Kp)*df/b
        Sq = 1+0.1*Kp*b/L  # aquí existe una verificación, se omite
        Sgama = 1+0.1*Kp*b/L
        total1 = Coh*Nc*Sc*Dc
        total2 = 0.5*b*gam*Ngama*Sgama*Dgama
        total3 = q*Nq*Sq*Dq
        ultima = total1+total2+total3
        solicitacion = carg/(b*L)
        if df >= 20:
            break
    admisible = ultima*fir/fm
    datos.append(str(round(df, 3)) + "$" + str(round(gam, 3)) + "$" + str(round(fi, 3)) + "$"
                 + str(round(Hmax, 3)) + "$" + str(round(Coh, 3)) + "$" +str(round(b, 3)) + "$"
                 + str(round(L, 3)) + "$" + str(round(solicitacion, 3)) + "$" + str(round(admisible, 3)) + "$")
    escribir_contacto()
    # messagebox.showinfo("Guardado", "Nervio añadido")
    caso.set("")
    consultar()

def mostrar():
    consultar()

def eliminar():
    eliminado = conteliminar.get()
    for elemento in datos:
        arreglo = elemento.split("$")
        if eliminado == arreglo[0]:
            datos.remove(elemento)
    escribir_contacto()
    consultar()
    # if removido:
        # messagebox.showinfo("Eliminar","Elemento eliminado "+eliminado)
        
def nuevo_archivo():
    iniciar_archivo()
    cargar()
    consultar()

############################################ PRIMER ESTRATO ###############################
titulo = Label(pes_cero, text="Estrato 1").place(x=320, y=30)
para_e = crear(pes_cero)
para_e.label("e :", 320, 60)
para_e.caja(e_one, 7, 345, 60)
para_e.botonC("", check_e1, 300, 60)

para_Gs = crear(pes_cero)
para_Gs.label("Gs:", 320, 85)
para_Gs.caja(Gs_one, 7, 345, 85)
para_Gs.botonC("", check_Gs1, 300, 85)

para_S = crear(pes_cero)
para_S.label("S:", 320, 110)
para_S.caja(S_one, 7, 345, 110)
para_S.botonC("", check_S1, 300, 110)

para_w = crear(pes_cero)
para_w.label("w:", 320, 135)
para_w.caja(w_one, 7, 345, 135)
para_w.botonC("", check_w1, 300, 135)

para_gama = crear(pes_cero)
para_gama.label("\u03b3:", 320, 160)
for_gama = Entry(pes_cero, textvariable=gama_one, width=7).place(x=345, y=160)

para_cohesion = crear(pes_cero)
para_cohesion.label("C:", 320, 185)
para_cohesion.caja(c_one, 7, 345, 185)

para_fi = crear(pes_cero)
para_fi.label("\u03d5:", 320, 210)
para_fi.caja(fi_one, 7, 345, 210)

para_D1 = crear(pes_cero)
para_D1.label("D :", 320, 235)
para_D1.caja(espesor_one, 7, 345, 235)

######################################### SEGUNDO ESTRATO ############################################
titulo = Label(pes_cero, text="Estrato 2").place(x=450, y=30)
para_e = crear(pes_cero)
para_e.label("e :", 450, 60)
para_e.caja(e_two, 7, 475, 60)
para_e.botonC("", check_e2, 430, 60)

para_Gs = crear(pes_cero)
para_Gs.label("Gs:", 450, 85)
para_Gs.caja(Gs_two, 7, 475, 85)
para_Gs.botonC("", check_Gs2, 430, 85)

para_S = crear(pes_cero)
para_S.label("S:", 450, 110)
para_S.caja(S_two, 7, 475, 110)
para_S.botonC("",check_S2, 430, 110)

para_w = crear(pes_cero)
para_w.label("w:", 450, 135)
para_w.caja(w_two, 7, 475, 135)
para_w.botonC("", check_w2, 430, 135)

para_gama = crear(pes_cero)
para_gama.label("\u03b3:", 450, 160)
for_gama = Entry(pes_cero, textvariable=gama_two, width=7).place(x=475, y=160)

para_cohesion = crear(pes_cero)
para_cohesion.label("C:", 450, 185)
para_cohesion.caja(c_two, 7, 475, 185)

para_fi = crear(pes_cero)
para_fi.label("\u03d5:", 450, 210)
para_fi.caja(fi_two, 7, 475, 210)

para_D2 = crear(pes_cero)
para_D2.label("D :", 450, 235)
para_D2.caja(espesor_two, 7, 475, 235)

######################################### TERCER ESTRATO ############################################
titulo = Label(pes_cero, text="Estrato 2").place(x=580, y=30)
para_e = crear(pes_cero)
para_e.label("e :", 580, 60)
para_e.caja(e_three, 7, 605, 60)
para_e.botonC("", check_e3, 560, 60)

para_Gs = crear(pes_cero)
para_Gs.label("Gs:", 580, 85)
para_Gs.caja(Gs_three, 7, 605, 85)
para_Gs.botonC("",check_Gs3, 560, 85)

para_S = crear(pes_cero)
para_S.label("S:", 580, 110)
para_S.caja(S_three, 7, 605, 110)
para_S.botonC("", check_S3, 560, 110)

para_w = crear(pes_cero)
para_w.label("w:", 580, 135)
para_w.caja(w_three, 7, 605, 135)
para_w.botonC("", check_w3, 560, 135)

para_gama = crear(pes_cero)
para_gama.label("\u03b3:", 580, 160)
for_gama = Entry(pes_cero, textvariable=gama_three, width=7).place(x=605, y=160)

para_cohesion = crear(pes_cero)
para_cohesion.label("C:", 580, 185)
para_cohesion.caja(c_three, 7, 605, 185)

para_fi = crear(pes_cero)
para_fi.label("\u03d5:", 580, 210)
para_fi.caja(fi_three, 7, 605, 210)

para_carga = crear(pes_cero)
para_carga.label("Carga (kN): ", 30, 60)
para_carga.caja(carga, 8, 100, 60)

para_L = crear(pes_cero)
para_L.label("L :", 30, 90)
para_L.caja(l, 8, 100, 90)

para_B = crear(pes_cero)
para_B.label("B :", 30, 120)
para_B.caja(B, 8, 100, 120)

para_DF = crear(pes_cero)
para_DF.label("DF : ", 30, 150)
para_DF.caja(DF, 8, 100, 150)

para_Mx = crear(pes_cero)
para_Mx.label("Mx (kN) : ", 30, 180)
para_Mx.caja(Mx, 8, 100, 180)

para_My = crear(pes_cero)
para_My.label("My (kN) : ", 30, 210)
para_My.caja(My, 8, 100, 210)
consultar()

para_nombre_archivo = crear(pes_cero)
para_nombre_archivo.caja(nombre_archivo, 8, 30, 30)
para_nombre_archivo.boton("Cargar/abrir",nuevo_archivo, 100, 25, bg="#bebebe")

para_calcular = crear(pes_cero)
para_calcular.boton("Calcular L", guardar, 1000, 210, bg="#009", fg="white")

para_mostrar = crear(pes_cero)
para_mostrar.boton("Calcular B", guardar2, 1000, 240, bg="gray", fg="white")

para_mostrar = crear(pes_cero)
para_mostrar.boton("Calcular DF", guardar3, 1000, 270, bg="gray", fg="white")

spinTelefono = Spinbox(pes_cero, textvariable=conteliminar).place(x=920, y=50)
botonEliminar = Button(pes_cero, text="Eliminar", command=eliminar, bg="#009", fg="white").place(x=1000, y=80)
                     
Radio_LRFD = Radiobutton(pes_cero, text="LRFD", value=1,
                         variable=opcion, activebackground="#009").place(x=30, y=260)
para_LRFD1 = crear(pes_cero)
para_LRFD1.label("F.M.", 110, 243)
para_LRFD1.caja(FM, 8, 100, 260)
para_LRFD2 = crear(pes_cero)
para_LRFD2.label("\u03d5", 185, 243)
para_LRFD2.caja(fi_R, 8, 170, 260)

para_creditos = crear(pes_cero)
para_creditos.label("Desarrollado por: Daniel Parra H.", 900, 0)
#Radio_Europeo=Radiobutton(pes0, text="Europeos", value=2,\
                    #variable=opcion, activebackground="#bebebe").place(x=450,y=100)
#para_eur1=crear(pes0)
#para_eur1.label("FSc",560,83)
#para_eur1.caja(FS_c,8,550,100)
#para_eur2=crear(pes0)
#para_eur2.label("FS\u03d5",635,83)
#para_eur2.caja(FS_fi,8,620,100)

#Radio_global=Radiobutton(pes0, text="Global", value=3,\
                    #variable=opcion, activebackground="#bebebe").place(x=450,y=140) 
#para_glob=crear(pes0)
#para_glob.label("Global",555,122)
#para_glob.caja(Global,8,550,140)

ventana.mainloop()