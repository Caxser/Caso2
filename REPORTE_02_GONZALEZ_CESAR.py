# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
#inicio de codigo
#abrir archivo
with open("synergy_logistics_database.csv", "r") as archivo_csv:
  lector= csv.DictReader(archivo_csv)
  
  
  #buscar rutas
  rutas=[]
  #siguiente loop identifica las rutas presentes en el archivo y las devuelve en un diccionario
  #anadir define si se agrega la ruta o no
  for linea in lector:

    origen=linea["origin"]
    destino=linea["destination"]
    anadir=1
    for ruta in rutas:
      if origen == ruta[0]:
        if destino == ruta[1]:
          anadir=0
          break
      continue
    if anadir==1:
      rutas.append([origen,destino])
    else:
      continue
  #lista con sublistas tipo ruta=[[origen1,destino1][origen2,destino2]...]

  #172 rutas
  #print(rutas)
  print(len(rutas))
  #transportes de cada ruta
  for ruta in rutas:

    tipo_transportes=[]
    archivo_csv= open("synergy_logistics_database.csv", "r")
    lector= csv.DictReader(archivo_csv)
    for linea in lector:
      if linea["origin"]== ruta[0]:
        if linea["destination"]==ruta[1]:
          if linea["transport_mode"] not in tipo_transportes:
            tipo_transportes.append(linea["transport_mode"])
    ruta.append(tipo_transportes)
    archivo_csv.close()
  #resultado lista
  #ruta=[[origen1,destino1,[transportes]]]
  
#sacar los valores de cada ruta dividiendo entre Exports e Imports
  #valores_ex=[]
  #valores_imp=[]
  for ruta in rutas:

    valores_ex=[]
    valores_imp=[]
    archivo_csv= open("synergy_logistics_database.csv", "r")
    lector= csv.DictReader(archivo_csv)
    for linea in lector:
      
      if linea["direction"] == "Exports":
        
        if linea["origin"] == ruta[0]:
          if linea["destination"]== ruta[1]:
            valor=int(linea["total_value"])
            valores_ex.append(valor)
            
      if linea["direction"] == "Imports":
        if linea["origin"] == ruta[0]:
          if linea["destination"]== ruta[1]:
            valor=int(linea["total_value"])
            valores_imp.append(valor)
    
    ruta.append(len(valores_ex))
    ruta.append(sum(valores_ex))
    ruta.append(len(valores_imp))
    ruta.append(sum(valores_imp))
    archivo_csv.close()

  
  for ruta in rutas:
      valor_total= ruta[4]+ruta[6]
      ruta.append(valor_total)
  #resultado lista rutas=[[origen1, destino1, transportes, #exportaciones1, valor_exportaciones1, #importaciones1, valor_importaciones1]...]

  
  #obtener transportes
  archivo_csv= open("synergy_logistics_database.csv", "r")
  lector= csv.DictReader(archivo_csv)
  transportes_valor=[]
  for linea in lector:
    transporte= linea["transport_mode"]
    if transporte not in transportes_valor:
      transportes_valor.append(transporte)
  #lista obtenida transportes_valor
  #transportes_valor=[tipo_de_transporte]
  archivo_csv.close()
  

  transportes_copia=[]
  #transformar lista en sublistas
  for transporte in transportes_valor:
    transporte_sublista=transporte
    transportes_copia.append([transporte_sublista])
  transportes_valor=transportes_copia[:]


  #valor total y frecuencia de cada transporte
  for transporte in transportes_valor:
    archivo_csv= open("synergy_logistics_database.csv", "r")
    lector= csv.DictReader(archivo_csv)
    valores=[]
    for line in lector:
      if transporte[0]== line["transport_mode"]:
        valores.append(int(line["total_value"]))
    transporte.append([sum(valores),len(valores)])
    archivo_csv.close()
  #lista obtenida transportes_valor
  #transportes_valor=[tipo_de_transporte1,[valor_total, frecuencia_uso]...]
  
  
  #obtiene los valores por importacion y exportacion dependiendo del tipo de transporte
  for transporte in transportes_valor:
    archivo_csv= open("synergy_logistics_database.csv", "r")
    lector= csv.DictReader(archivo_csv)
    valores_imp=[]
    valores_exp=[]
    for line in lector:
      if line["direction"]=="Exports":
        if transporte[0]== line["transport_mode"]:
          valores_exp.append(int(line["total_value"]))
      if line["direction"]=="Imports":
        if transporte[0]== line["transport_mode"]:
          valores_imp.append(int(line["total_value"]))
    transporte.append([sum(valores_exp),len(valores_exp)])
    transporte.append([sum(valores_imp),len(valores_imp)])
    archivo_csv.close()
  #lista obtenida
  #transportes_valor=[[tipo_de_trassporte1,[valor_total,frecuencia_total],[valor_exportacion,frec_exportacion],[valor_importacion,frec_importacion]]...]

#comienza análisis de datos
#ejemplo sorted(student_objects, key=lambda student: student[2])   # sort by age
#ordenar los transportes de menor a mayor
transportes_ordenada_total=sorted(transportes_valor, key=lambda transporte: transporte[1][0])
transportes_ordenada_exp=sorted(transportes_valor, key=lambda transporte: transporte[2][0])
transportes_ordenada_imp=sorted(transportes_valor, key=lambda transporte: transporte[3][0])


#ordenar las rutas de mayor a menor conforme a sus exportaciones
rutas_ordenadas_exp=sorted(rutas, key=lambda ruta: ruta[4],reverse=True)
#ordenar las rutas de mayor a menor conforme a sus importaciones
rutas_ordenadas_imp=sorted(rutas, key=lambda ruta: ruta[6],reverse=True)
#orden mayor a menor del total
rutas_ordenadas_total=sorted(rutas, key=lambda ruta: ruta[7],reverse=True)


#rescatar cada país que se encuentra en los datos
paises=[]
for ruta in rutas:
    origen=ruta[0]
    destino=ruta[1]
    if origen or destino not in paises:
        if origen not in paises:
            paises.append(origen)
        if destino not in paises:
            paises.append(destino)
#pasar paises a lista con sublistas
paises_importantes=[]
for pais in paises:
    paises_importantes.append([pais,0,0,0,0,0])
#lista resutlante
#paises_importantes=[pais, #export,valor export, #import, valor de import, total valor]

#contabilizar valor de los paises dependiendo de si exportan o importan
#si exportan, el pais importante es el origen 
#si impirtan, el pais importante es el destino
for ruta in rutas:
    origen=ruta[0]
    destino=ruta[1]
    anadir=0
    anadir_2=0
    for pais in paises_importantes:
        if origen == pais[0] or destino== pais[0]:
            if origen==pais[0]:
                contador_exp=ruta[3]
                valor_exp=ruta[4]
                pais[1]+= contador_exp
                pais[2]+= valor_exp
                pais[5]+= valor_exp
                anadir=1
            
            if destino == pais[0]:
                contador_imp=ruta[5]
                valor_imp=ruta[6]
                pais[3]+= contador_imp
                pais[4]+= valor_imp
                pais[5]+= valor_imp
                anadir_2=1


#paises_importantes=[pais, #export,valor export, #import, valor de import, total valor]
#ejemplo sorted(student_objects, key=lambda student: student[2])   # sort by age
paises_importantes_ord=sorted(paises_importantes, key=lambda pais: pais[5],reverse=True)

#verificación de los datos
total=0
for pais in paises_importantes_ord:
    total+=pais[5]
#sacar el 80%
porcentaje=total*0.8
total_sum=0
paises_importantes_porcentaje=[]
for pais in paises_importantes_ord:
    
    if total_sum<porcentaje:
        paises_importantes_porcentaje.append(pais)
        total_sum+=pais[5]
        
    else:
        break
#paises_importantes_porcentaje=[pais, #export,valor export, #import, valor de import, total valor]


#print(total)
#total_1=0
#for ruta in rutas:
#    total_1+=ruta[7]
#print(total_1)
#archivo_csv= open("synergy_logistics_database.csv", "r")
#lector= csv.DictReader(archivo_csv)
#total_2=0
#for linea in lector:
#    suma=int(linea["total_value"])
#    total_2+=suma
#print(total_2)
#archivo_csv.close()

#rutas=[[origen1,destino1,transport,#export1,valor_export1,#import1,valor_import1,valor total]...]
#transportes_valor=[[tipo_de_trassporte1,[valor_total,frecuencia_total],[valor_exportacion,frec_exportacion],[valor_importacion,frec_importacion]]...]


#impresion de la información
print("""
      
          Estas son las rutas más demandas por importaciones y exportaciones
      
      """)
print("""
          10 rutas con mejores importaciones
      
        """)
contador=0
for ruta in rutas_ordenadas_imp:
    contador+=1
    print(contador,".- Ruta", ruta[0],"-",ruta[1], " con un total de $", ruta[6], "; rutas de transporte usadas: ", ruta[2])
    if contador==10:
        break
print("""
          10 rutas con mejores exportaciones
      """)   
contador=0
for ruta in rutas_ordenadas_exp:
    contador+=1
    print(contador,".- Ruta", ruta[0],"-",ruta[1], " con un total de $", ruta[4], "; rutas de transporte usadas: ", ruta[2])
    if contador==10:
        break
print(""" 
          10 Mejores rutas con la valoración total    
      """)
contador=0
for ruta in rutas_ordenadas_total:
    contador+=1
    print(contador,".- Ruta", ruta[0],"-",ruta[1], " con un total de $", ruta[7], "; rutas de transporte usadas: ", ruta[2])
    if contador==10:
        break

print("""
      Mejores formas de transporte por cantidad de importación y exportación
      
      """)
print("""
      Tomando en cuenta solo la exportación
      """)
contador=0
for transporte in transportes_ordenada_exp:
    contador+=1
    print(contador,".- Tipo de transporte: ", transporte[0], " total de exportaciones: ",transporte[2][1]," valor:", transporte[2][0] )
        
print("""
      Tomando en cuenta solo la importación
      """)
contador=0
for transporte in transportes_ordenada_imp:
    contador+=1
    print(contador,".- Tipo de transporte: ", transporte[0], " total de exportaciones: ",transporte[3][1]," valor:", transporte[3][0] )
print("""
      Tomando en importación y exportación
      """)
contador=0
for transporte in transportes_ordenada_exp:
    contador+=1
    print(contador,".- Tipo de transporte: ", transporte[0], " total de importaciones y exportaciones: ",transporte[2][1]+transporte[3][1]," valor total:", transporte[1][0] )
print("")
print("Valor total de importaciones y exportaciones: $", total)
print("80%=", total*0.8)

print("""
      Paises que acaparan el 80% del comercio
      """)
#paises_importantes=[pais, #export,valor export, #import, valor de import, total valor]
contador=0
total_pais_porcentaje=0
for pais in paises_importantes_porcentaje:
    contador+=1
    print(contador,".- ", pais[0], "con: ", pais[1]," importaciones, valor: ", pais[2], "; importaciones: ", pais[3]," valor: ", pais[4], "; valor total: ", pais[5] )
    total_pais_porcentaje+= pais[5]
print("Total entre los ", contador, " paises: ", total_pais_porcentaje)