from sympy import symbols,trigsimp,factor,cancel, Function, Matrix, Rational, diff, simplify, latex, init_printing, sin, cos

# Definición de Símbolos

t, r, theta, phi, Gamma_sym = symbols('t r theta phi Gamma') 

indices = [t, r, theta, phi] 


# Parámetros y expresiones para la métrica de Kerr
a, M, c, delta_s, sigma_s = symbols('a M c Delta Sigma', real=True) # Delta y Sigma (mayúsculas) son símbolos, delta y sigma (minúsculas) se definen abajo

# Expresiones para la métrica (usando _expr para distinguirlas de los símbolos si fuera necesario)
delta = r**2 - 2*M*r + a**2
sigma = r**2 + a**2*cos(theta)**2

# Función para convertir índices a su forma de LaTeX
def latex_index(index_symbol): 
    index_dict = {'t': 't', 'r': 'r', 'theta': '\\theta', 'phi': '\\phi'}
    return index_dict.get(str(index_symbol), str(index_symbol))

# christoffelSymbols = [] # Esta lista no se usaba, la comento o puedes eliminarla.
init_printing(use_unicode=True)

## Métrica de Kerr (g_ij)
g_ij = [
    [-(1 - 2*M*r/sigma)*c**2, 0, 0, -2*M*a*r*sin(theta)**2*c/sigma],
    [0, sigma/delta, 0, 0],
    [0, 0, sigma, 0],
    [-2*M*a*r*sin(theta)**2*c/sigma, 0, 0, (r**2 + a**2 + 2*M*a*r*sin(theta)**2/sigma)*sin(theta)**2]
]

# Métrica inversa g^ij (tu variable 'gij')
gij = [[Matrix(g_ij).inv()[i-1, j-1] for j in range(1, len(g_ij)+1)] for i in range(1, len(g_ij)+1)]

# Función para calcular Símbolos de Christoffel
# upperIndex, lowerIndex1, lowerIndex2 son enteros 1-basados (1, 2, 3, 4)
def Christoffel(upperIndex, lowerIndex1, lowerIndex2):
    # Obtener los símbolos de coordenadas correspondientes a los índices
    # Ahora 'indices' es la lista [t, r, theta, phi]
    upperIndexSymbol = indices[upperIndex - 1]
    lowerIndexSymbol1 = indices[lowerIndex1 - 1]
    lowerIndexSymbol2 = indices[lowerIndex2 - 1]

    Christoffel_sum = 0 # Usé Christoffel_sum para la variable de suma, pero tu 'Christoffel = 0' original también funciona debido al alcance.
    
    # La suma ahora itera correctamente de 0 a 3 (len(indices) es 4)
    for i in range(0, len(indices), 1): # 'i' es el índice de suma (0-basado)
        
       
        term_inv_metric = gij[upperIndex-1][i]
        
        diff1 = diff(g_ij[i][lowerIndex2-1], lowerIndexSymbol1)
        diff2 = diff(g_ij[i][lowerIndex1-1], lowerIndexSymbol2)
        diff3 = diff(g_ij[lowerIndex1-1][lowerIndex2-1], indices[i])
        
        Christoffel_sum = Christoffel_sum + Rational(1,2) * term_inv_metric * (diff1 + diff2 - diff3)

        # Reemplaza primero para que SymPy sepa que esas expresiones son Delta y Sigma
    expr = Christoffel_sum.replace(r**2 - 2*M*r + a**2, delta_s)
    expr = expr.replace(r**2 + a**2*cos(theta)**2, sigma_s)

    # Aplica simplificaciones trigonométricas, algebraicas y factorización
    expr = trigsimp(expr)               # Simplifica funciones trigonométricas
    expr = simplify(expr)               # Simplificación general
    expr = cancel(expr)                 # Cancela factores comunes en numerador/denominador
    expr = factor(expr)                 # Agrupa factores (incluye Sigma y Delta)

    Christoffel_simplified = expr


    if (Christoffel_simplified != 0):
        latex_str = f"\\Gamma^{{{latex_index(upperIndexSymbol)}}}{{ }}_{{{latex_index(lowerIndexSymbol1)} {latex_index(lowerIndexSymbol2)}}} &= {latex(Christoffel_simplified)} \\\\"
        print(latex_str)
        return latex_str # o Christoffel_simplified si prefieres devolver el valor SymPy

# Calcular todos los símbolos de Christoffel
print("Calculando todos los símbolos de Christoffel para la métrica de Kerr:")

for i in range(1, 5, 1):      # Índice superior k
    for j in range(1, 5, 1):  # Primer índice inferior m
        for k_loop in range(1, 5, 1): # Segundo índice inferior n 
            Christoffel(i, j, k_loop)

print("\nCálculo completado.")