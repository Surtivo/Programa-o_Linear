import highspy
import numpy as np

T = 22
# c  = [5, 5, 7, 12.9, 26.9, 49.4, 38.7, 85, 81.12, 48, 39.6, 5, 19, 5, 25.8, 156.87, 90, 12.9, 7.92, 289, 289, 13.9]       #Custo por unidade de produto;
l  = [2, 1.5, 2, 5.9, 8.1, 13, 14.7, 51, 33.12, 8, 15.6, 2, 3, 3, 11.8, 43.47, 20, 4.9, 2.36, 89, 89, 3.9]                  #Lucro por unidade de produto;
g  = [640, 630, 1512, 13950, 11240, 20160, 15876, 30618, 5985, 560, 4851, 7942, 12060, 33840, 11232, 10800]                 #Volume de cada produto que necessita geladeira;
k  = [560, 1458, 1458, 40824, 40824, 7830]                                                                                  #Volume de cada produto que vai apenas na kombi;
fc = [3, 3.5, 5, 7, 18.8, 36.4, 24, 34, 48, 40, 24, 3, 16, 2, 14, 113.4, 70, 8, 5.56, 200, 200, 10]                         #Fluxo de caixa;
de = [144, 216, 72, 108, 48, 72, 6, 12, 4.8, 7.2, 5.6, 8.4, 5.6, 8.4, 5, 10, 8, 12, 4.8, 7.2, 9.6,                          #Demanda de cada produto;
      14.4, 3.2, 4.8, 4, 6, 8, 12, 6, 11, 5.6, 8.4, 10, 18, 7, 9, 3.2, 4.8, 4, 6, 4, 6, 4, 6]

h = highspy.Highs()
h.changeObjectiveSense(highspy.ObjSense.kMaximize)

for t in range(T):
    h.addVar(float(de[2*t]), float(de[2*t+1]))
    h.changeColIntegrality(t, highspy.HighsVarType.kInteger)

for t in range(T):
    h.changeColCost(t, float(l[t]))

# 3. Adicionar as restrições
# addRow(limite_inferior, limite_superior, num_coeficientes, lista_indices, lista_valores)
h.addRow(-highspy.kHighsInf, 1369900, len(g), [i for i in range(3, 19)], g)                                                 #Restrição de volume total da geladeira;
h.addRow(-highspy.kHighsInf, 1984000, len(k), [0, 1, 2, 19, 20, 21], k)                                                     #Restrição de volume total da kombi;                                             
h.addRow(-highspy.kHighsInf, 6000, len(fc), [i for i in range(22)], fc)                                                     #Restrição de fluxo de caixa (quanto pode ser gasto para comprar os produtos);

# 4. Executar
h.run()

# 5. Extrair resultados
sol = h.getSolution()
if h.getModelStatus() == highspy.HighsModelStatus.kOptimal:
    print(f"\nLucro Máximo: {h.getInfo().objective_function_value}")
    for t in range(T):
        print(f"x[{t}] = {sol.col_value[t]}")
else:
    print(f"Status do modelo: {h.getModelStatus()}")
    
print("")
print("Lucro total proposto pelo artigo original: R$: 2916.68")
print("Lucro total proposto por este modelo: R$: ", h.getInfo().objective_function_value)
print("Diferença entre os lucros: R$: ", h.getInfo().objective_function_value - 2916.68)
# print("Lucro total proposto por este modelo: R$: ", (10804.73)-(5999.80))