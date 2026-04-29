import highspy

h = highspy.Highs()
T = 5  # Exemplo de horizonte de tempo
c = 100 # Custo unitário x
n = 150 # Custo unitário y
d = [50] * T # Demanda (exemplo)
e = [10] * T # Capacidade existente (exemplo)

# 1. Criar Variáveis
for t in range(4 * T):
    h.addVar(0.0, highspy.kHighsInf)

# 2. Definir Custos (Função Objetivo)
for t in range(T):
    h.changeColCost(t, float(c))       # Coeficientes de xt
    h.changeColCost(t + T, float(n))   # Coeficientes de yt
    # wt e zt têm custo 0 no somatório da imagem

# 3. Adicionar Restrições para cada t
for t in range(T):
    # --- Restrição 1: wt - sum(xs) = 0 ---
    # Reescrevendo: wt - x_{s...t} = 0
    indices_x = list(range(max(0, t-19), t + 1))
    coefs_x = [-1.0] * len(indices_x)
    # Adicionando o índice de wt (que é t + 2*T)
    h.addRow(0.0, 0.0, len(indices_x) + 1, indices_x + [t + 2*T], coefs_x + [1.0])

    # --- Restrição 2: zt - sum(ys) = 0 ---
    indices_y = list(range(T + max(0, t-14), T + t + 1))
    coefs_y = [-1.0] * len(indices_y)
    # Adicionando o índice de zt (que é t + 3*T)
    h.addRow(0.0, 0.0, len(indices_y) + 1, indices_y + [t + 3*T], coefs_y + [1.0])

    # --- Restrição 3: wt + zt >= dt - et ---
    limite_inf = float(d[t] - e[t])
    h.addRow(limite_inf, highspy.kHighsInf, 2, [t + 2*T, t + 3*T], [1.0, 1.0])

    # --- Restrição 4: 0.8zt - 0.2wt <= 0.2et ---
    limite_sup = float(0.2 * e[t])
    h.addRow(-highspy.kHighsInf, limite_sup, 2, [t + 2*T, t + 3*T], [-0.2, 0.8])

# 4. Resolver
h.run()

# 5. Extrair Resultados (Exemplo para o primeiro período)
sol = h.getSolution()
if h.getModelStatus() == highspy.HighsModelStatus.kOptimal:
    print(f"Custo Mínimo: {h.getInfo().objective_function_value}")
    print(f"x[0] = {sol.col_value[0]}")
    print(f"y[0] = {sol.col_value[T]}")
else:
    print(f"Status do modelo: {h.getModelStatus()}") 