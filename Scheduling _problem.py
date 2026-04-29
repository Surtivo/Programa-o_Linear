import highspy
import numpy as np

h = highspy.Highs()

#Iniciando o modelo com 7 variáveis inteiras e custo unitário (definição do modelo);
for i in range(7):
    h.addVar(0.0, highspy.kHighsInf)
    h.changeColIntegrality(i, highspy.HighsVarType.kInteger)
    h.changeColCost(i, 1.0)

demanda = [10, 12, 15, 10, 14, 16, 11]

#Adicionar as restrições;
h.addRow(demanda[0], highspy.kHighsInf, 5, [0, 3, 4, 5, 6], [1, 1, 1, 1, 1])
h.addRow(demanda[1], highspy.kHighsInf, 5, [0, 1, 4, 5, 6], [1, 1, 1, 1, 1])
h.addRow(demanda[2], highspy.kHighsInf, 5, [0, 1, 2, 5, 6], [1, 1, 1, 1, 1])
h.addRow(demanda[3], highspy.kHighsInf, 5, [0, 1, 2, 3, 6], [1, 1, 1, 1, 1])
h.addRow(demanda[4], highspy.kHighsInf, 5, [0, 1, 2, 3, 4], [1, 1, 1, 1, 1])
h.addRow(demanda[5], highspy.kHighsInf, 5, [1, 2, 3, 4, 5], [1, 1, 1, 1, 1])
h.addRow(demanda[6], highspy.kHighsInf, 5, [2, 3, 4, 5, 6], [1, 1, 1, 1, 1])

#Executar;
h.run()

#Exibir resultados;
info = h.getInfo()
sol = h.getSolution()

if h.getModelStatus() == highspy.HighsModelStatus.kOptimal:
    sol = h.getSolution()
    total_pessoal = h.getInfo().objective_function_value
    print(f"\nTotal de funcionários necessários: {int(total_pessoal)}")
    for i in range(7):
        print(f"x{i+1} (Iniciando no dia {i+1}): {int(sol.col_value[i])}")
else:
    print("Não foi encontrada solução ótima.")