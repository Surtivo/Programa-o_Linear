import highspy

h = highspy.Highs()
T = 20          #Exemplo de horizonte de tempo;
c = 100         #Custo unitário x;
n = 60          #Custo unitário y;
d = [500] * T   #Demanda (exemplo);
e = [120] * T   #Capacidade existente (exemplo);

#Criar Variáveis. Como temos 4 variáveis por período, o total é 4*T;
for t in range(4 * T):
    h.addVar(0.0, highspy.kHighsInf)
    h.changeColIntegrality(t, highspy.HighsVarType.kInteger)

#Definir Custos (Função Objetivo). Definimos apenas até a parte x e y (via índices), pois wt e zt não têm custo no somatório da imagem;
for t in range(T):
    h.changeColCost(t, float(c))
    h.changeColCost(t + T, float(n))

#Adicionar Restrições para cada t. As restrições são adicionadas em um loop para cada período t, garantindo que as relações entre as variáveis sejam mantidas ao longo do tempo;
for t in range(T):
    #Restrição 1: wt - sum(xs) = 0. Reescrevendo: wt - x_{s...t} = 0. Aqui, usamos uma janela deslizante para incluir as variáveis x dos últimos 20 períodos (ou menos, se t < 20).
    indices_x = list(range(max(0, t-19), t + 1))
    coefs_x = [-1.0] * len(indices_x)
    h.addRow(0.0, 0.0, len(indices_x) + 1, indices_x + [t + 2*T], coefs_x + [1.0])  #Adicionando o índice de wt (que é t + 2*T) para as variáveis da restrição;

    #Restrição 2: zt - sum(ys) = 0. Similar à restrição anterior, mas para as variáveis y, considerando os últimos 15 períodos;
    indices_y = list(range(T + max(0, t-14), T + t + 1))
    coefs_y = [-1.0] * len(indices_y)
    h.addRow(0.0, 0.0, len(indices_y) + 1, indices_y + [t + 3*T], coefs_y + [1.0]) #Adicionando o índice de zt (que é t + 3*T) para as variáveis da restrição;

    #Restrição 3: wt + zt >= dt - et. Esta restrição garante que a soma de wt e zt seja suficiente para atender à demanda líquida (demanda menos capacidade existente);
    limite_inf = float(d[t] - e[t])
    h.addRow(limite_inf, highspy.kHighsInf, 2, [t + 2*T, t + 3*T], [1.0, 1.0])

    #Restrição 4: 0.8zt - 0.2wt <= 0.2et. Esta restrição impõe que a quantidade de zt (nuclear) não exceda 20% da capacidade total;
    limite_sup = float(0.2 * e[t])
    h.addRow(-highspy.kHighsInf, limite_sup, 2, [t + 2*T, t + 3*T], [-0.2, 0.8])

#Executar;
h.run()

#Exibir resultados;
sol = h.getSolution()
if h.getModelStatus() == highspy.HighsModelStatus.kOptimal:
    print(f"\nCusto Mínimo: {h.getInfo().objective_function_value}")
    for t in range(T):
        print(f"x[{t}] = {sol.col_value[t]}")
        print(f"y[{t}] = {sol.col_value[t + T]}")
else:
    print(f"Status do modelo: {h.getModelStatus()}") 