
from tkinter import *
# matplotlib
import matplotlib.pyplot as plt
import statistics
import seaborn as sns

import pandas as pd
from PIL import *
import os

# Explorador de arquivos
from tkinter import filedialog

global M
global SD
global median
global MAD
M = 0
SD = 0
median = 0
MAD = 0

def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir=sys.path[0],
                                          title="Escolle un arquivo",
                                          filetypes=(("Datos de LabView",
                                                      "*.lvm*"),
                                                     ("Ficheiros de texto",
                                                      "*.txt*"),
                                                     ("Todos os formatos",
                                                      "*.*")))

    # Etiqueta do ficheiro utilizado
    label_file_explorer.configure(text=filename)


def guillotina():
    my_file = open(filename)
    string_list = my_file.readlines()
    string_list[0:21] = ""  # Crea 0 liñas baleiras no espazo ocupado antes por 21 liñas.

    my_file = open(filename, "w")
    new_file_contents = "".join(string_list)
    my_file.write(new_file_contents)
    my_file.close()  # Abre o arquivo de datos e substitúe o encabezado polo novo. Despois, pecha o arquivo.

    readable_file = open(filename)
    read_file = readable_file.read()
    print(read_file)  # Amosa o resultado en consola.

    print("Chop chop!")  # Amosa unha confirmación da execución en consola.


# Fixación tempos
def time():
    global Ti
    global Tf
    try:
        Ti = float(Tempiniw.get())
        Tf = float(Tempfinw.get())
        print("Time set to interval between " + str(Ti) + " and " + str(Tf) + " s.")

    except:
        Ti = "tiempo1"
        Tf = "tiempo2"
        print("Time restrictions removed.")


# Media e desv. típica no rango de tempos
def MDT():
    file = open(filename, 'r')
    lines = file.readlines()
    # print(lines)
    del lines[0]
    try:
        # Tempo:
        tempo = []
        for x in lines:
            tempo.append(x.split('\t')[1])  # Extrae os tempos
            # print(tempo)
        tempo1 = []  # Esta lista incluirá os datos de tempo con puntos en vez de comas
        for string in tempo:
            new_stringt = string.replace(",", ".")
            new_stringt1 = float(new_stringt)
            tempo1.append(new_stringt1)
        tempo2 = []  # Esta segunda lista serve para recoller os datos só no intervalo de tempo solicitado
        tindex = []  # Lista de índices dos datos de interese na lista global, para poder relacionalos con outros parámetros
        for x in tempo1:
            if Tf > x > Ti:
                tempo2.append(x)
                tindex.append(tempo1.index(x))

        # Variable a analizar
        analito = []
        for x in lines:
            analito.append(x.split('\t')[opcionso1.index(variableo1.get())])
        analito1 = []
        for string in analito:
            new_stringana = string.replace(",", ".")
            new_stringana1 = float(new_stringana)
            analito1.append(new_stringana1)
        analito2 = []
        for x in analito1:
            for n in tindex:
                if analito1.index(x) == n and len(analito2) < len(tindex):
                    analito2.append(x)

        M = round(statistics.mean(analito2), 2)
        median = round(statistics.median(analito2), 2)
        SD = round(statistics.stdev(analito2), 2)
        series = pd.Series(analito2)
        MAD = round(series.mad())

    except:
        # Tempo:
        tempo = []
        for x in lines:
            tempo.append(x.split('\t')[1])  # Extrae os tempos
            # print(tempo)
        tempo1 = []  # Esta lista incluirá os datos de tempo con puntos en vez de comas
        for string in tempo:
            new_stringt = string.replace(",", ".")
            new_stringt1 = float(new_stringt)
            tempo1.append(new_stringt1)

        # Variable a analizar
        analito = []
        for x in lines:
            analito.append(x.split('\t')[opcionso1.index(variableo1.get())])
        analito1 = []
        for string in analito:
            new_stringana = string.replace(",", ".")
            new_stringana1 = float(new_stringana)
            analito1.append(new_stringana1)

        M = round(statistics.mean(analito1), 2)
        median = round(statistics.median(analito1), 2)
        SD = round(statistics.stdev(analito1), 2)
        series = pd.Series(analito1)
        MAD = round(series.mad())

    file.close()

    label_Mean.configure(text="Mean" + " " + str(M))
    label_Median.configure(text="Median:" + " " + str(median))
    label_SD.configure(text="Desv. Est." + " " + str(SD))
    label_MAD.configure(text="Mean Abs. Dev.:" + " " + str(MAD))


# Gráficos
def grafico():
    file = open(filename, 'r')
    lines = file.readlines()
    # print(lines)
    del lines[0]

    # Se a checkbox está desmarcada, fai gráficos só cunha variable en Y. Dentro de cada tipo de gráfico
    # hai un bucle para comprobar se se pide o gráfico nun tempo limitado ou para todo o set de datos.

    if bo2.get() == 0:
        try:
            # Tempo:
            abscisa = []
            for x in lines:
                abscisa.append(x.split('\t')[opcionsa1.index(variablea1.get())])  # Extrae os tempos
                # print(tempo)
            abscisa1 = []  # Esta lista incluirá os datos de tempo con puntos en vez de comas
            for string in abscisa:
                new_stringt = string.replace(",", ".")
                new_stringt1 = float(new_stringt)
                abscisa1.append(new_stringt1)
            abscisa2 = []  # Esta segunda lista serve para recoller os datos só no intervalo de tempo solicitado
            tindex = []  # Lista de índices dos datos de interese na lista global, para poder relacionalos con outros parámetros
            for x in abscisa1:
                if x < Tf and x > Ti:
                    abscisa2.append(x)
                    tindex.append(abscisa1.index(x))

            # Variable a analizar
            analito = []
            for x in lines:
                analito.append(x.split('\t')[opcionso1.index(variableo1.get())])
            analito1 = []
            for string in analito:
                new_stringana = string.replace(",", ".")
                new_stringana1 = float(new_stringana)
                analito1.append(new_stringana1)
            analito2 = []
            for x in analito1:
                for n in tindex:
                    if analito1.index(x) == n and len(analito2) < len(tindex):
                        analito2.append(x)


            file.close()

            # plot
            plt.plot(abscisa2, analito2, color='green', linestyle=' ', linewidth=3,
                     marker='.', markerfacecolor='blue', markersize=3)

            # naming the x axis
            plt.xlabel(variablea1.get())
            # naming the y axis
            plt.ylabel(variableo1.get())

            # giving a title to my graph
            plt.title(str(variablea1.get()) + " vs. " + str(variableo1.get()))


        except:
            # Tempo:
            tempo = []
            for x in lines:
                tempo.append(x.split('\t')[opcionsa1.index(variablea1.get())])  # Extrae os tempos
                # print(tempo)
            tempo1 = []  # Esta lista incluirá os datos de tempo con puntos en vez de comas
            for string in tempo:
                new_stringt = string.replace(",", ".")
                new_stringt1 = float(new_stringt)
                tempo1.append(new_stringt1)

            # Variable a analizar
            analito = []
            for x in lines:
                analito.append(x.split('\t')[opcionso1.index(variableo1.get())])
            analito1 = []
            for string in analito:
                new_stringana = string.replace(",", ".")
                new_stringana1 = float(new_stringana)
                analito1.append(new_stringana1)

            file.close()

            # plot
            plt.plot(tempo1, analito1, color='green', linestyle=' ', linewidth=3,
                     marker='.', markerfacecolor='blue', markersize=3)

            # naming the x axis
            plt.xlabel(variablea1.get())
            # naming the y axis
            plt.ylabel(variableo1.get())

            # giving a title to my graph
            plt.title(str(variablea1.get()) + " vs. " + str(variableo1.get()))

    # Se a checkbox está marcada, fai o mesmo que antes pero con dúas variables no eixo Y.

    else:
        try:
            # Tempo:
            abscisa = []
            for x in lines:
                abscisa.append(x.split('\t')[opcionsa1.index(variablea1.get())])  # Extrae os tempos
                # print(tempo)
            abscisa1 = []  # Esta lista incluirá os datos de tempo con puntos en vez de comas
            for string in abscisa:
                new_stringt = string.replace(",", ".")
                new_stringt1 = float(new_stringt)
                abscisa1.append(new_stringt1)
            abscisa2 = []  # Esta segunda lista serve para recoller os datos só no intervalo de tempo solicitado
            tindex = []  # Lista de índices dos datos de interese na lista global, para poder relacionalos con outros parámetros
            for x in abscisa1:
                if x < Tf and x > Ti:
                    abscisa2.append(x)
                    tindex.append(abscisa1.index(x))


            # Variables a analizar
            analitoa = []
            for x in lines:
                analitoa.append(x.split('\t')[opcionso1.index(variableo1.get())])
            analitoa1 = []
            for string in analitoa:
                new_stringana = string.replace(",", ".")
                new_stringana1 = float(new_stringana)
                analitoa1.append(new_stringana1)
            analitoa2 = []
            for x in analitoa1:
                for n in tindex:
                    if analitoa1.index(x) == n and len(analitoa2) < len(tindex):
                        analitoa2.append(x)

            analitob = []
            for x in lines:
                analitob.append(x.split('\t')[opcionso2.index(variableo2.get())])
            analitob1 = []
            for string in analitob:
                new_stringana = string.replace(",", ".")
                new_stringana1 = float(new_stringana)
                analitob1.append(new_stringana1)
            analitob2 = []
            for x in analitob1:
                for n in tindex:
                    if analitob1.index(x) == n and len(analitob2) < len(tindex):
                        analitob2.append(x)


            file.close()

            # plot
            plt.plot(abscisa2, analitoa2, color='green', linestyle=' ', linewidth=3,
                     marker='.', markerfacecolor='blue', markersize=3)

            plt.plot(abscisa2, analitob2, color='red', linestyle=' ', linewidth=3,
                     marker='.', markerfacecolor='red', markersize=3)

            # naming the x axis
            plt.xlabel(variablea1.get())
            # naming the y axis
            plt.ylabel(variableo1.get() + " and " + variableo2.get())

            # giving a title to my graph
            plt.title(str(variablea1.get()) + " vs. " + str(variableo1.get() + " and " + variableo2.get()))


        except:
            # Tempo:
            tempo = []
            for x in lines:
                tempo.append(x.split('\t')[opcionsa1.index(variablea1.get())])  # Extrae os tempos
                # print(tempo)
            tempo1 = []  # Esta lista incluirá os datos de tempo con puntos en vez de comas
            for string in tempo:
                new_stringt = string.replace(",", ".")
                new_stringt1 = float(new_stringt)
                tempo1.append(new_stringt1)

            # Variables a analizar
            analitoa = []
            for x in lines:
                analitoa.append(x.split('\t')[opcionso1.index(variableo1.get())])
            analitoa1 = []
            for string in analitoa:
                new_stringana = string.replace(",", ".")
                new_stringana1 = float(new_stringana)
                analitoa1.append(new_stringana1)

            analitob = []
            for x in lines:
                analitob.append(x.split('\t')[opcionso2.index(variableo2.get())])
            analitob1 = []
            for string in analitob:
                new_stringana = string.replace(",", ".")
                new_stringana1 = float(new_stringana)
                analitob1.append(new_stringana1)

            file.close()

            # plot
            plt.plot(tempo1, analitoa1, color='green', linestyle=' ', linewidth=3,
                     marker='.', markerfacecolor='blue', markersize=3)

            plt.plot(tempo1, analitob1, color='red', linestyle=' ', linewidth=3,
                     marker='.', markerfacecolor='red', markersize=3)

            # naming the x axis
            plt.xlabel(variablea1.get())
            # naming the y axis
            plt.ylabel(variableo1.get() + " and " + variableo2.get())

            # giving a title to my graph
            plt.title(str(variablea1.get()) + " vs. " + str(variableo1.get() + " and " + variableo2.get()))

    # function to show the plot
    plt.show()


# Boxplots
def boxplot():
    file = open(filename, 'r')
    lines = file.readlines()
    # print(lines)
    del lines[0]
    if bv3.get() == 0:
        try:
            # Tempo:
            abscisa = []
            for x in lines:
                abscisa.append(x.split('\t')[opcionsv1.index(variable1.get())])  # Extrae os tempos
                # print(tempo)
            abscisa1 = []  # Esta lista incluirá os datos de tempo con puntos en vez de comas
            for string in abscisa:
                new_stringt = string.replace(",", ".")
                new_stringt1 = float(new_stringt)
                abscisa1.append(new_stringt1)
            abscisa2 = []  # Esta segunda lista serve para recoller os datos só no intervalo de tempo solicitado
            tindex = []  # Lista de índices dos datos de interese na lista global, para poder relacionalos con outros parámetros
            for x in abscisa1:
                if x < Tf and x > Ti:
                    abscisa2.append(x)
                    tindex.append(abscisa1.index(x))

            # Variable a analizar
            analito = []
            for x in lines:
                analito.append(x.split('\t')[opcionsv2.index(variable2.get())])
            analito1 = []
            for string in analito:
                new_stringana = string.replace(",", ".")
                new_stringana1 = float(new_stringana)
                analito1.append(new_stringana1)
            analito2 = []
            for x in analito1:
                for n in tindex:
                    if analito1.index(x) == n and len(analito2) < len(tindex):
                        analito2.append(x)

            sns.boxplot(data=analito2)

            # naming the x axis
            plt.xlabel(variable1.get())
            # naming the y axis
            plt.ylabel(variable2.get())

            plt.show()
            file.close()

        except:
            # Variable a analizar
            analito = []
            for x in lines:
                analito.append(x.split('\t')[opcionsv2.index(variable2.get())])
            analito1 = []
            for string in analito:
                new_stringana = string.replace(",", ".")
                new_stringana1 = float(new_stringana)
                analito1.append(new_stringana1)

            sns.boxplot(data=analito1)

            # naming the x axis
            plt.xlabel(variable1.get())
            # naming the y axis
            plt.ylabel(variable2.get())

            plt.show()
            file.close()
    else:
        try:
            # Tempo:
            abscisa = []
            for x in lines:
                abscisa.append(x.split('\t')[opcionsv1.index(variable1.get())])  # Extrae os tempos
                # print(tempo)
            abscisa1 = []  # Esta lista incluirá os datos de tempo con puntos en vez de comas
            for string in abscisa:
                new_stringt = string.replace(",", ".")
                new_stringt1 = float(new_stringt)
                abscisa1.append(new_stringt1)
            abscisa2 = []  # Esta segunda lista serve para recoller os datos só no intervalo de tempo solicitado
            tindex = []  # Lista de índices dos datos de interese na lista global, para poder relacionalos con outros parámetros
            for x in abscisa1:
                if x < Tf and x > Ti:
                    abscisa2.append(x)
                    tindex.append(abscisa1.index(x))

            # Variables a analizar
            analitoa = []
            for x in lines:
                analitoa.append(x.split('\t')[opcionsv2.index(variable2.get())])
            analitoa1 = []
            for string in analitoa:
                new_stringana = string.replace(",", ".")
                new_stringana1 = float(new_stringana)
                analitoa1.append(new_stringana1)
            analitoa2 = []
            for x in analitoa1:
                for n in tindex:
                    if analitoa1.index(x) == n and len(analitoa2) < len(tindex):
                        analitoa2.append(x)

            analitob = []
            for x in lines:
                analitob.append(x.split('\t')[opcionsv3.index(variable3.get())])
            analitob1 = []
            for string in analitob:
                new_stringana = string.replace(",", ".")
                new_stringana1 = float(new_stringana)
                analitob1.append(new_stringana1)
            analitob2 = []
            for x in analitob1:
                for n in tindex:
                    if analitob1.index(x) == n and len(analitob2) < len(tindex):
                        analitob2.append(x)

            df = pd.DataFrame(list(zip(analitoa2, analitob2)))

            sns.boxplot(data=df)

            # naming the x axis
            plt.xlabel(variable1.get())
            # naming the y axis
            plt.ylabel(variable2.get() + " and " + variable3.get())

            plt.show()
            file.close()

        except:
            # Variables a analizar
            analitoa = []
            for x in lines:
                analitoa.append(x.split('\t')[opcionsv2.index(variable2.get())])
            analitoa1 = []
            for string in analitoa:
                new_stringana = string.replace(",", ".")
                new_stringana1 = float(new_stringana)
                analitoa1.append(new_stringana1)

            analitob = []
            for x in lines:
                analitob.append(x.split('\t')[opcionsv3.index(variable3.get())])
            analitob1 = []
            for string in analitob:
                new_stringana = string.replace(",", ".")
                new_stringana1 = float(new_stringana)
                analitob1.append(new_stringana1)

            df = pd.DataFrame(list(zip(analitoa1, analitob1)))

            sns.boxplot(data=df)

            # naming the x axis
            plt.xlabel(variable1.get())
            # naming the y axis
            plt.ylabel(variable2.get() + " and " + variable3.get())

            plt.show()
            file.close()


# Ventana principal
window = Tk()

# Titulo da ventá principal
window.title('FTDE: DROP')

# Tamaño da ventá principal
window.geometry("725x400")

# Cor de fondo da venta principal
window.config(background="white")

# Imos crear algúns frames de fondo
top_frame = Frame(window, bg="black", width=450, height=50, pady=3)
top_frame2 = Frame(window, bg="alice blue", width=450, height=50, pady=6)
middle_frame = Frame(window, bg="black", width=450, height=400, pady=3)
low_frame = Frame(window, bg="gray84", width=450, height=50, pady=3)

# Disposición dos frames de fondo
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
top_frame2.grid(row=1, sticky="nsew")
middle_frame.grid(row=2, sticky="ew")
low_frame.grid(row=3, sticky="ew")

# Creación e disposición dos frames de fronte (centro)
middle_frame.grid_rowconfigure(0, weight=1)
middle_frame.grid_columnconfigure(1, weight=1)

framea = Frame(middle_frame, bg='alice blue', width=250, height=400, padx=3, pady=3)
frameb = Frame(middle_frame, bg='alice blue', width=250, height=400, padx=3, pady=3)

framea.grid(row=0, column=0, columnspan=2, sticky="ns", padx=3)
frameb.grid(row=0, column=2, sticky="ns", padx=3)

# Etiquetas do Explorador de Arquivos
label_file_explorer = Label(top_frame,
                            text="Ferramenta de tratamento de datos experimentais do GTE: versión DROP",
                            width=105, height=4,
                            fg="blue")

# Etiqueta co logo do GTE
dirname = os.path.dirname(__file__)
photogte = PhotoImage(file=os.path.join(dirname, "imaxes", "gte2.png"))

photoimagegte = photogte.subsample(3, 3)

label_gte = Label(top_frame2,
                  image=photoimagegte)

# Botóns do Explorador de Arquivos
button_explore = Button(top_frame2,
                        text="Navegar arquivos",
                        command=browseFiles)

button_exit = Button(low_frame,
                     text="Saír",
                     fg="red",
                     command=exit)

# Etiqueta autoría
label_auth = Label(low_frame,
                 text="GNU-GPL   2021   Juan Jesús Rico Fuentes",
                 fg="black")

# Botón de guillotina
photo = PhotoImage(
    file=os.path.join(dirname, "imaxes", "guillo.png"))

photoimage = photo.subsample(17, 17)

button_guillotina = Button(top_frame2,
                           text="Guillotina",
                           image=photoimage,
                           command=guillotina)

# Widget entrada de tempos:

# Etiqueta para tempo inicial
Tempini_label = Label(top_frame2,
                      text='Tempo inicial')

# Entrada do tempo incial
Tempiniw = Entry(top_frame2,
                 width=10)

# Etiqueta para tempo final
Tempfin_label = Label(top_frame2,
                      text='Tempo final')

# Entrada do tempo final
Tempfinw = Entry(top_frame2,
                 width=10)

# Fixar tempos
button_tempos = Button(top_frame2,
                       text="Fixar tempos",
                       command=time)

# Etiqueta gráficos
label_partial_graph = Label(framea,
                            width=70, height=1,
                            text="Gráficos")

# Media e desv. típ.
button_MDT = Button(framea,
                    text="MDT (y)",
                    command=MDT)

# Etiqueta coa media
label_Mean = Label(framea,
                   text="Media:" + " " + str(M),
                   fg="blue")

# Etiqueta coa mediana
label_Median = Label(framea,
                   text="Median:" + " " + str(median),
                   fg="blue")

# Etiqueta coa standard dev.
label_SD = Label(framea,
                 text="Std. Dev.:" + " " + str(SD),
                 fg="blue")

# Etiqueta coa MAD
label_MAD = Label(framea,
                 text="Mean Abs. Dev.:" + " " + str(MAD),
                 fg="blue")

# Botón de Gráficos
button_graph = Button(framea,
                      text="Gráfico",
                      width=10, height=2,
                      command=grafico)

# Botón de Boxplots
button_boxp1 = Button(frameb,
                      text="Box Plot 1",
                      width=10, height=2,
                      command=boxplot)

# Etiqueta de boxplots
label_global_graph = Label(frameb,
                           width=20, height=1,
                           text="Boxplots")

# Etiqueta "Eixo X" grafico
label_a1 = Label(framea,
                 text="Eixo X:")

# Etiqueta "Eixo Y" grafico
label_o1 = Label(framea,
                 text="Eixo Y:")

# Etiqueta "Eixo Y 2" grafico e checkbutton para activala
label_o2 = Label(framea,
                 text="Eixo Y 2:")

bo2 = IntVar()
button_o2 = Checkbutton(framea, text='', variable=bo2, onvalue=1, offvalue=0)

# Etiqueta "Var 1" boxplot
label_v1 = Label(frameb,
                 text="Variable 1 (t):")

# Etiqueta "Var 2" boxplot
label_v2 = Label(frameb,
                 text="Variable 2:")

# Etiqueta "Var 3" boxplot con botón para activar
label_v3 = Label(frameb,
                 text="Variable 3:")
bv3 = IntVar()
button_v3 = Checkbutton(frameb, text='', variable=bv3, onvalue=1, offvalue=0)

# Widget para selección de variable a plottear. A orde das variables é a do LabView do Drop, así que haberá que
# axustala se se cambia de instalación

# Lista e widget de selección para abscisas do gráfico
opcionsa1 = ["X_Value", "Tempo (s)", "Tª Agua Entrada", "Tª Agua Salida", "Caudal Aire Prim",
             "Cauda Aire Sec", "Tª Humos", "Tª Chimenea", "Caudal Agua", "Peso Pellet (kg)",
             "% Pellet", "Segundos ON", "Segundos OFF", "NO (vpm)", "NOx (vpm)", "O2 (%)",
             "CO (%)", "CO2 (%)", "TC0", "TC1", "TC2", "TC3", "TC4", "TC5"]

variablea1 = StringVar(window)
variablea1.set(opcionsa1[1])

menua1 = OptionMenu(framea, variablea1, *opcionsa1)

# Lista e widget de selección para ordenadas 1 do gráfico
opcionso1 = ["X_Value", "Tempo (s)", "Tª Agua Entrada", "Tª Agua Salida", "Caudal Aire Prim",
             "Cauda Aire Sec", "Tª Humos", "Tª Chimenea", "Caudal Agua", "Peso Pellet (kg)",
             "% Pellet", "Segundos ON", "Segundos OFF", "NO (vpm)", "NOx (vpm)", "O2 (%)",
             "CO (%)", "CO2 (%)", "TC0", "TC1", "TC2", "TC3", "TC4", "TC5"]

variableo1 = StringVar(window)
variableo1.set(opcionso1[3])

menuo1 = OptionMenu(framea, variableo1, *opcionso1)

# Lista e widget de selección para ordenadas 2 do gráfico
opcionso2 = ["X_Value", "Tempo (s)", "Tª Agua Entrada", "Tª Agua Salida", "Caudal Aire Prim",
             "Cauda Aire Sec", "Tª Humos", "Tª Chimenea", "Caudal Agua", "Peso Pellet (kg)",
             "% Pellet", "Segundos ON", "Segundos OFF", "NO (vpm)", "NOx (vpm)", "O2 (%)",
             "CO (%)", "CO2 (%)", "TC0", "TC1", "TC2", "TC3", "TC4", "TC5"]

variableo2 = StringVar(window)
variableo2.set(opcionso2[3])

menuo2 = OptionMenu(framea, variableo2, *opcionso2)

# Lista e widget de selección para Variable 1 Boxplot
opcionsv1 = ["X_Value", "Tempo (s)", "Tª Agua Entrada", "Tª Agua Salida", "Caudal Aire Prim",
             "Cauda Aire Sec", "Tª Humos", "Tª Chimenea", "Caudal Agua", "Peso Pellet (kg)",
             "% Pellet", "Segundos ON", "Segundos OFF", "NO (vpm)", "NOx (vpm)", "O2 (%)",
             "CO (%)", "CO2 (%)", "TC0", "TC1", "TC2", "TC3", "TC4", "TC5"]

variable1 = StringVar(window)
variable1.set(opcionsv1[1])

menuv1 = OptionMenu(frameb, variable1, *opcionsv1)

# Lista e widget de selección para Variable 2 Boxplot
opcionsv2 = ["X_Value", "Tempo (s)", "Tª Agua Entrada", "Tª Agua Salida", "Caudal Aire Prim",
             "Cauda Aire Sec", "Tª Humos", "Tª Chimenea", "Caudal Agua", "Peso Pellet (kg)",
             "% Pellet", "Segundos ON", "Segundos OFF", "NO (vpm)", "NOx (vpm)", "O2 (%)",
             "CO (%)", "CO2 (%)", "TC0", "TC1", "TC2", "TC3", "TC4", "TC5"]

variable2 = StringVar(window)
variable2.set(opcionsv2[2])

menuv2 = OptionMenu(frameb, variable2, *opcionsv2)

# Lista e widget de selección para Variable 3 Boxplot
opcionsv3 = ["X_Value", "Tempo (s)", "Tª Agua Entrada", "Tª Agua Salida", "Caudal Aire Prim",
             "Cauda Aire Sec", "Tª Humos", "Tª Chimenea", "Caudal Agua", "Peso Pellet (kg)",
             "% Pellet", "Segundos ON", "Segundos OFF", "NO (vpm)", "NOx (vpm)", "O2 (%)",
             "CO (%)", "CO2 (%)", "TC0", "TC1", "TC2", "TC3", "TC4", "TC5"]

variable3 = StringVar(window)
variable3.set(opcionsv3[2])

menuv3 = OptionMenu(frameb, variable3, *opcionsv3)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns

label_file_explorer.grid(column=1, row=1)

button_explore.grid(column=1, row=1, rowspan=2, pady=10, padx=5)
button_guillotina.grid(column=2, row=1, rowspan=2, pady=10, padx=5)

label_gte.grid(column=8, row=1, rowspan=2, padx=5)

top_frame2.grid_columnconfigure(7, weight=4)

button_exit.grid(column=3, row=7, padx=5)
low_frame.grid_columnconfigure(4, weight=4)
label_auth.grid(column=5, row=7, padx=5, sticky=E)

# Widget entrada de tempos


Tempini_label.grid(column=3, row=1, pady=5, padx=5)
Tempiniw.grid(column=4, row=1, pady=5, padx=5)
Tempfin_label.grid(column=3, row=2, pady=5, padx=5)
Tempfinw.grid(column=4, row=2, pady=5, padx=5)
button_tempos.grid(column=5, row=1, rowspan=2, pady=5, padx=5)

# Gráficos
label_partial_graph.grid(column=1, row=1, columnspan=6, pady=5, padx=5)

button_MDT.grid(column=4, row=2, rowspan=4, pady=5, padx=5)
label_Mean.grid(column=5, row=2, pady=5, padx=5)
label_Median.grid(column=5, row=3, pady=5, padx=5)
label_SD.grid(column=5, row=4, pady=5, padx=5)
label_MAD.grid(column=5, row=5, pady=5, padx=5)

# Widget de lista desplegable abscisas

label_a1.grid(column=2, row=2, pady=5, padx=5, sticky=E)
menua1.grid(column=3, row=2, pady=5, padx=5)

# Widget de lista desplegable ordenadas 1

label_o1.grid(column=2, row=3, pady=5, padx=5, sticky=E)
menuo1.grid(column=3, row=3, pady=5, padx=5)

# Widget de lista desplegable ordenadas 2

label_o2.grid(column=2, row=4, pady=5, padx=5, sticky=E)
menuo2.grid(column=3, row=4, pady=5, padx=5)
button_o2.grid(column=2, row=4, pady=5, sticky=W)

button_graph.grid(column=1, row=5, columnspan=3, pady=5)

# Widget de Variable temporal Boxplot

label_v1.grid(column=2, row=1, pady=5, padx=5, sticky=E)
label_global_graph.grid(column=2, row=0, columnspan=2, pady=5, padx=5, sticky="N")
menuv1.grid(column=3, row=1, pady=8, padx=5)
frameb.rowconfigure((1, 5), weight=1)

# Widget de Variable 2 Boxplot

label_v2.grid(column=2, row=3, pady=5, padx=5, sticky=E)
menuv2.grid(column=3, row=3, pady=8, padx=5)

# Widget de Variable 3 Boxplot + Checkbutton

label_v3.grid(column=2, row=4, pady=5, padx=5, sticky=E)
button_v3.grid(column=2, row=4, pady=5, sticky=W)
menuv3.grid(column=3, row=4, pady=5, padx=5)

button_boxp1.grid(column=1, row=5, columnspan=3, pady=5, padx=5)

# Let the window wait for any events
window.mainloop()
