
def guillotina():
    # Abrir o arquivo cos datos e un workbook paralelo de destino dos mesmos
    my_file = load_workbook(filename=filename)
    try:
        my_sheet = my_file.worksheets[1]
    except:
        my_sheet = my_file.worksheets[0]
    global wb
    global datos
    wb = Workbook()
    datos = wb.active

    # Contar filas e columnas do arquivo orixinal e pegalas no arquivo de destino
    mr = my_sheet.max_row
    mc = my_sheet.max_column

    for i in range(1, mr + 1):
        for j in range(1, mc + 1):
            c = my_sheet.cell(row=i, column=j)
            datos.cell(row=i, column=j).value = c.value
    print("Raw target file created!")

    # Eliminar os datos innecesarios
    datos.delete_cols(4)
    datos.delete_cols(7, 3)
    datos.delete_cols(16, 7)
    datos.delete_cols(18)
    datos.delete_cols(20)
    datos.delete_cols(30, 4)
    datos.delete_cols(34)
    datos.delete_cols(37, 2)
    datos.delete_cols(39)
    datos.delete_cols(40, 9)

    # Identificador de fin de ensaio e guillotina de filas sobrantes
    vali = 0
    for i in range(2, mr + 1):
        fin = datos.cell(i, 39).value
        if fin == 1:
            vali = i
    global mr2
    mr2 = vali
    datos.delete_rows(mr2 + 1, mr + 1)
    print("End of Test located and data trimmed.")

    # Conversor de CO a CO (ppm) e vacía cela en caso de CO<200
    datos.cell(1, 40).value = "CO (ppm) corr"
    for i in range(2, mr2 + 1):
        ttl = datos.cell(i, 31).value * 10000
        if ttl > 200:
            datos.cell(i, 40).value = ttl
    print("Corrected CO (ppm) and limited to over 200.")

    # Cálculo de TL promedios
    datos.cell(1, 41).value = "TL Alta (1-3)"
    for i in range(2, mr2 + 1):
        tlalta = (datos.cell(i, 20).value + datos.cell(i, 21).value + datos.cell(i, 22).value) / 3
        if tlalta > 0:
            datos.cell(i, 41).value = tlalta

    datos.cell(1, 42).value = "TL Media (4-6)"
    for i in range(2, mr2 + 1):
        tlmedia = (datos.cell(i, 23).value + datos.cell(i, 24).value + datos.cell(i, 25).value) / 3
        if tlmedia > 0:
            datos.cell(i, 42).value = tlmedia

    datos.cell(1, 43).value = "TL Baixa (7-9)"
    for i in range(2, mr2 + 1):
        tlbaixa = (datos.cell(i, 26).value + datos.cell(i, 27).value + datos.cell(i, 28).value) / 3
        if tlbaixa > 0:
            datos.cell(i, 43).value = tlbaixa

    print("Mean temperatures in Combustion Chamber calculated.")

    # Eliminación de datos sobrantes
    datos.delete_cols(20, 9)  # TL1 a TL9
    datos.delete_cols(22)  # CO

    # Pechar o arquivo orixinal e gardar un Excel cos datos de traballo
    my_file.close()
    wb.save(filename="datos.xlsx")  # Abre o arquivo de datos e garda unha copia da folla de interese.

    print("Guillotinado!")  # Amosa unha confirmación da execución en consola.

if __name__ == '__main__':
    guillotina()