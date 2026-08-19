import highspy
import numpy as np

h = highspy.Highs()

# 1. Adicionar variáveis passando APENAS (limite_inferior, limite_superior)
# Isso retorna um HighsStatus, não o índice. O HiGHS assume a ordem de criação.
h.addVar(0.0, highspy.kHighsInf) # P1 (índice 0)
h.addVar(0.0, highspy.kHighsInf) # P2 (índice 1)

# 2. Definir os coeficientes da função objetivo SEPARADAMENTE
# changeColCost(índice_da_coluna, novo_custo)
h.changeColCost(0, 4)
h.changeColCost(1, 12)

# 3. Adicionar as restrições
# addRow(limite_inferior, limite_superior, num_coeficientes, lista_indices, lista_valores)
h.addRow(-highspy.kHighsInf, 6.0, 2, [0, 1], [2, 1])  # 2x1 + 3x2 <= 6
h.addRow(8, highspy.kHighsInf, 2, [0, 1], [1, 3]) # -x1 + x2 <= 1
h.addRow(-highspy.kHighsInf, 4, 1, [0], [1]) # -x1 + x2 <= 1

# 4. Executar
h.run()

# 5. Extrair resultados
info = h.getInfo()
sol = h.getSolution()

if h.getModelStatus() == highspy.HighsModelStatus.kOptimal:
    print(f"Status: Ótimo!")
    print(f"x1 = {sol.col_value[0]:.2f}")
    print(f"x2 = {sol.col_value[1]:.2f}")
    print(f"Objetivo = {info.objective_function_value:.2f}")
else:
    print(f"Status do modelo: {h.getModelStatus()}")