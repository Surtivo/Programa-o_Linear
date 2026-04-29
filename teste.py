import highspy
import numpy as np

h = highspy.Highs()
x0 = h.addVariable(lb = 0, ub = highspy.kHighsInf)
x1 = h.addVariable(lb = 0, ub = highspy.kHighsInf)

h.addConstr(-highspy.kHighsInf <=   2*x0 + 3*x1 <= 6)
h.addConstr(-highspy.kHighsInf <= -1*x0 + 1*x1 <= 1)

h.minimize(x0 + x1)

h.run()

info = h.getInfo()
sol = h.getSolution()

if h.getModelStatus() == highspy.HighsModelStatus.kOptimal:
    print(f"Status: Ótimo!")
    print(f"x1 = {sol.col_value[0]:.2f}")
    print(f"x2 = {sol.col_value[1]:.2f}")
    print(f"Objetivo = {info.objective_function_value:.2f}")
else:
    print(f"Status do modelo: {h.getModelStatus()}")