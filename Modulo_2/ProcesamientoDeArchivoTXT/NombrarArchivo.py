import pandas as pd

with open('Dataset/25001.txt', 'r', encoding='utf-8') as f:
    lineas = f.readlines() #readlines regresa una lista de lineas del archivo 
    linea_string = lineas[4].strip() # El indice 4 es la linea 5

print(linea_string)