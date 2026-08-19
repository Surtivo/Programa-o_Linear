import highspy
import numpy as np

T = 22
l  = [2, 1.5, 2, 5.9, 8.1, 13, 14.7, 51, 33.12, 8, 15.6, 2, 3, 3, 11.8, 43.47, 20, 4.9, 2.36, 89, 89, 3.9]
g  = [640, 630, 1512, 13950, 11240, 20160, 15876, 30618, 5985, 560, 4851, 7942, 12060, 33840, 11232, 10800]
k  = [560, 1458, 1458, 40824, 40824, 7830]
fc = [3, 3.5, 5, 7, 18.8, 36.4, 24, 34, 48, 40, 24, 3, 16, 2, 14, 113.4, 70, 8, 5.56, 200, 200, 10]
de = [144, 216, 72, 108, 48, 72, 6, 12, 4.8, 7.2, 5.6, 8.4, 5.6, 8.4, 5, 10, 8, 12, 4.8, 7.2, 9.6,
      14.4, 3.2, 4.8, 4, 6, 8, 12, 6, 11, 5.6, 8.4, 10, 18, 7, 9, 3.2, 4.8, 4, 6, 4, 6, 4, 6]

h = highspy.Highs()

# Usando o solver Simplex padrão para garantir cálculo de duais limpos
options = highspy.HighsOptions()
options.solver = "simplex"
h.passOptions(options)

h.changeObjectiveSense(highspy.ObjSense.kMaximize)

# Mudamos para kContinuous para permitir a análise marginal (preço-sombra)
for t in range(T):
    h.addVar(float(de[2*t]), float(de[2*t+1]))
    h.changeColIntegrality(t, highspy.HighsVarType.kContinuous) 

for t in range(T):
    h.changeColCost(t, float(l[t]))

h.addRow(-highspy.kHighsInf, 1369900.0, len(g), [i for i in range(3, 19)], g) 
h.addRow(-highspy.kHighsInf, 1984000.0, len(k), [0, 1, 2, 19, 20, 21], k)    
h.addRow(-highspy.kHighsInf, 6000.0, len(fc), [i for i in range(22)], fc)     

h.run()

if h.getModelStatus() == highspy.HighsModelStatus.kOptimal:
    print(f"Lucro Máximo (Relaxado): {h.getInfo().objective_function_value:.2f}\n")
    
    sol = h.getSolution()
    
    # ==========================================================
    # 1. ANÁLISE DE VARIÁVEIS E CUSTOS REDUZIDOS (COLUNAS)
    # ==========================================================
    print("="*75)
    print("ANÁLISE DAS VARIÁVEIS DE DECISÃO E CUSTO REDUZIDO")
    print("="*75)
    print(f"{'Variável':<10} | {'Qtd Espacial':<12} | {'Lucro Unit':<12} | {'Custo Reduzido':<15}")
    print("-"*75)
    for t in range(T):
        qtd = sol.col_value[t]
        lucro_u = l[t]
        custo_red = sol.col_dual[t] # No HiGHS, col_dual representa o custo reduzido
        
        print(f"x[{t}]".ljust(10) + f" | {qtd:<12.2f} | {lucro_u:<12.2f} | {custo_red:<15.4f}")
        
    print("\n" + "> Custo Reduzido zerado indica que a variável está na base.")
    print("> Se for negativo em Maximização, indica o quanto o lucro cairia se você fosse forçado a colocar mais unidades dela.")

    # ==========================================================
    # 2. ANÁLISE DE RECURSOS E PREÇOS SOMBRA (RESTRIÇÕES / LINHAS)
    # ==========================================================
    print("\n" + "="*75)
    print("ANÁLISE DOS RECURSOS (PREÇO SOMBRA / VALOR DUAL)")
    print("="*75)
    print(f"{'Restrição':<15} | {'Consumo Real':<15} | {'Limite (RHS)':<15} | {'Preço Sombra':<15}")
    print("-"*75)
    
    nomes_restricoes = ["Geladeira", "Kombi", "Fluxo Caixa"]
    limites_originais = [1369900.0, 1984000.0, 6000.0]
    
    for idx, nome in enumerate(nomes_restricoes):
        consumo = sol.row_value[idx]
        limite = limites_originais[idx]
        preco_sombra = sol.row_dual[idx] # row_dual representa o preço sombra marginal do recurso
        
        print(f"{nome:<15} | {consumo:<15.2f} | {limite:<15.2f} | {preco_sombra:<15.4f}")

    print("\n" + "> Preço Sombra indica o impacto no lucro total por unidade extra adicionada ao recurso.")
    print("> Um recurso com folga (consumo < limite) sempre terá Preço Sombra = 0.0000.")

else:
    print(f"Status do modelo: {h.getModelStatus()}")