import highspy
import numpy as np


g  = [640, 630, 1512, 13950, 11240, 20160, 15876, 30618, 5985, 560, 4851, 7942, 12060, 33840, 11232, 10800]
k  = [560, 1458, 1458, 40824, 40824, 7830]
# de2 = [10.4, 4.8, 5.6, 5.6, 12.3, 8, 4.8, 9.6, 3.2, 4, 8, 14.7, 5.6, 12, 21.5, 3.2, 4, 4, 6]
demanda_minima_original_geladeira = [19.2, 4.8, 5.6, 5.6, 28.8, 8, 4.8, 9.6, 3.2, 4, 8, 19.2, 5.6, 12, 38.4, 3.2]
demanda_minima_proposta_geladeira = [6, 4.8, 5.6, 5.6, 5, 8, 4.8, 9.6, 3.2, 4, 8, 6, 5.6, 11, 7, 3.2]

demanda_completa_proposta = [144, 216, 72, 108, 48, 72, 6, 12, 4.8, 7.2, 5.6, 8.4, 5.6, 8.4, 5, 10, 8, 12, 4.8, 7.2, 9.6,
      14.4, 3.2, 4.8, 4, 6, 8, 12, 6, 11, 5.6, 8.4, 11, 18, 7, 9, 3.2, 4.8, 4, 6, 4, 6, 4, 6]

de = [144, 216, 72, 108, 48, 72, 6, 12, 4.8, 7.2, 5.6, 8.4, 5.6, 8.4, 5, 10, 8, 12, 4.8, 7.2, 9.6,                         
      14.4, 3.2, 4.8, 4, 6, 8, 12, 6, 11, 5.6, 8.4, 10, 18, 7, 9, 3.2, 4.8, 4, 6, 4, 6, 4, 6]

d1 = [144, 216, 72, 108, 48, 72, 19.2, 28.8, 4.8, 7.2, 5.6, 8.4, 5.6, 8.4, 28.8, 43.2, 8, 12, 4.8, 
      7.2, 9.6, 14.4, 3.2, 4.8, 4, 6, 8, 12, 19.2, 28.8, 5.6, 8.4, 12, 18, 38.4, 57.6, 3.2, 4.8, 4, 6, 4, 6, 4, 6]

valores_x = [216, 76, 48, 12, 5, 6, 6, 6, 8, 5, 10, 4, 4, 9, 6, 6, 10, 7, 4, 4, 4, 4]
precos = [3.00, 3.50, 5.00, 7.00, 18.80, 36.40, 24.00, 34.00, 48.00, 40.00,
    24.00, 3.00, 16.00, 2.00, 14.00, 113.40, 70.00, 8.00, 5.56, 200.00,
    200.00, 10.00]



print(len(valores_x), len(precos))
mult = 0

for t in range(22):
    mult += valores_x[t] * precos[t]
print("Valor total gasto para comprar os produtos: R$: ", mult)

kombi = 0 
for t in range(3):
    kombi += valores_x[t] * k[t]

for t in range(19, 22):
    kombi += valores_x[t] * k[t-16]
print("Valor total kombi: R$: ", kombi)
print("Restrição kombi: 1984000")


soma_original = 0

print(len(g), len(demanda_minima_proposta_geladeira), len(demanda_minima_original_geladeira), len(d1), len(de))
print("")

# print("Diferença entre as demandas originais e as demandas propostas:")
# for t in range(44):
#     print(f"x[{t+1}] = {d1[t] - de[t]}")
# print("")

for t in range(16):
    soma_original += float(g[t]) * float(demanda_minima_original_geladeira[t])
print("Soma original:", soma_original)

if soma_original < 1369900:
    print("Soma é menor que 1.369.900")
else:
    print("Soma é maior ou igual a 1.369.900")
    print(soma_original - 1369900)

print("")
soma_proposta = 0

for t in range(16):
    soma_proposta += float(g[t]) * float(demanda_minima_proposta_geladeira[t])
print("Soma proposta:", soma_proposta)

if soma_proposta < 1369900:
    print("Soma é menor que 1.369.900")
    print(soma_proposta - 1369900)
else:    print("Soma é maior ou igual a 1.369.900")

print("")
print("Soma 1:", soma_original)
print("Soma 2:", soma_proposta)
print("Diferença entre as somas:", soma_original - soma_proposta)