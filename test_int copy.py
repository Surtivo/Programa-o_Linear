import highspy

h = highspy.Highs()
T = 5  
c = 100 
n = 150 
d = [50] * T 
e = [10] * T 

for t in range(4 * T):
    h.addVar(0.0, highspy.kHighsInf)

for t in range(T):
    h.changeColCost(t, float(c))       
    h.changeColCost(t + T, float(n))   


for t in range(T):

    indices_x = list(range(max(0, t-19), t + 1))
    coefs_x = [-1.0] * len(indices_x)

    h.addRow(0.0, 0.0, len(indices_x) + 1, indices_x + [t + 2*T], coefs_x + [1.0])


    indices_y = list(range(T + max(0, t-14), T + t + 1))
    coefs_y = [-1.0] * len(indices_y)
    h.addRow(0.0, 0.0, len(indices_y) + 1, indices_y + [t + 3*T], coefs_y + [1.0])

    limite_inf = float(d[t] - e[t])
    h.addRow(limite_inf, highspy.kHighsInf, 2, [t + 2*T, t + 3*T], [1.0, 1.0])

    limite_sup = float(0.2 * e[t])
    h.addRow(-highspy.kHighsInf, limite_sup, 2, [t + 2*T, t + 3*T], [-0.2, 0.8])

h.run()

sol = h.getSolution()
if h.getModelStatus() == highspy.HighsModelStatus.kOptimal:
    print(f"Custo Mínimo: {h.getInfo().objective_function_value}")
    print(f"x[0] = {sol.col_value[0]}")
    print(f"y[0] = {sol.col_value[T]}")
else:
    print(f"Status do modelo: {h.getModelStatus()}") 