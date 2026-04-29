import highspy
import numpy as np

h = highspy.Highs()

h.addVar(0.0, highspy.kHighsInf) 
h.addVar(0.0, highspy.kHighsInf) 
h.addVar(0.0, highspy.kHighsInf)
h.addVar(0.0, highspy.kHighsInf)
h.addVar(0.0, highspy.kHighsInf)
h.addVar(0.0, highspy.kHighsInf)
h.addVar(0.0, highspy.kHighsInf)

for i in range(7):
    h.changeColIntegrality(i, highspy.HighsVarType.kInteger)

h.changeColCost(0, 1.0)
h.changeColCost(1, 1.0)
h.changeColCost(2, 1.0)
h.changeColCost(3, 1.0)
h.changeColCost(4, 1.0)
h.changeColCost(5, 1.0)
h.changeColCost(6, 1.0)

demanda = [10, 12, 15, 10, 14, 16, 11]

h.addRow(demanda[0], highspy.kHighsInf, 5, [0, 3, 4, 5, 6], [1, 1, 1, 1, 1])
h.addRow(demanda[1], highspy.kHighsInf, 5, [0, 1, 4, 5, 6], [1, 1, 1, 1, 1])
h.addRow(demanda[2], highspy.kHighsInf, 5, [0, 1, 2, 5, 6], [1, 1, 1, 1, 1])
h.addRow(demanda[3], highspy.kHighsInf, 5, [0, 1, 2, 3, 6], [1, 1, 1, 1, 1])
h.addRow(demanda[4], highspy.kHighsInf, 5, [0, 1, 2, 3, 4], [1, 1, 1, 1, 1])
h.addRow(demanda[5], highspy.kHighsInf, 5, [1, 2, 3, 4, 5], [1, 1, 1, 1, 1])
h.addRow(demanda[6], highspy.kHighsInf, 5, [2, 3, 4, 5, 6], [1, 1, 1, 1, 1])

h.run()

info = h.getInfo()
sol = h.getSolution()

if h.getModelStatus() == highspy.HighsModelStatus.kOptimal:
    sol = h.getSolution()
    total_pessoal = h.getInfo().objective_function_value
    print(f"Total de funcionários necessários: {int(total_pessoal)}")
    for i in range(7):
        print(f"x{i+1} (Iniciando no dia {i+1}): {int(sol.col_value[i])}")
else:
    print("Não foi encontrada solução ótima.")