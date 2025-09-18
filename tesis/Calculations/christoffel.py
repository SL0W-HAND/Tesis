from sympy import symbols,trigsimp,factor,cancel, Function, Matrix, Rational, diff, simplify, latex, init_printing, sin, cos

# Definición de Símbolos

t, r, theta, phi, Gamma_sym = symbols('t r theta phi Gamma') 

indices = [t, r, theta, phi] 


# Parámetros y expresiones para la métrica de Kerr
a, m, c, delta_s, sigma_s, rho_s = symbols('a m c Delta Sigma rho', real=True) # Delta y Sigma (mayúsculas) son símbolos, delta y sigma (minúsculas) se definen abajo

# Expresiones para la métrica (usando _expr para distinguirlas de los símbolos si fuera necesario)
delta = r**2 - 2*m*r + a**2
sigma = (r**2 + a**2)**2 - a**2*sin(theta)**2*delta 
rho = r**2 + a**2*cos(theta)**2


# Función para convertir índices a su forma de LaTeX
def latex_index(index_symbol): 
    index_dict = {'t': 't', 'r': 'r', 'theta': '\\theta', 'phi': '\\phi'}
    return index_dict.get(str(index_symbol), str(index_symbol))


init_printing(use_unicode=True)

A = Function('A', real=True)(r)
B = Function('B', real=True)(r)

## Métrica de Kerr (g_ij)
# g_ij = [
#     [-(1 - 2*m*r/((r**2 + a**2*cos(theta)**2)**2)), 0, 0, -2*m*c*a*r*(sin(theta)**2)/((r**2 + a**2*cos(theta)**2)**2)],
#     [0, (r**2 + a**2*cos(theta)**2)**2/(r**2 - 2*m*r + a**2), 0, 0],
#     [0, 0, (r**2 + a**2*cos(theta)**2)**2, 0],
#     [-2*m*c*a*r*(sin(theta)**2)/((r**2 + a**2*cos(theta)**2)**2), 0, 0, ((r**2 + a**2)**2 - a**2*sin(theta)**2*(r**2 - 2*m*r + a**2))*(sin(theta)**2)/((r**2 + a**2*cos(theta)**2)**2)]
# ]

# Metrica generica para la derivacion de la metrica de Schwarzschild

#metrica de Schwarzschild (g_schwarzschild)
g_ij = [
    [-1 + 2*m/r, 0, 0, 0],
    [0, 1/(1 - 2*m/r), 0, 0],
    [0, 0, r**2, 0],
    [0, 0, 0, r**2*sin(theta)**2]
]

# Métrica inversa g^ij (tu variable 'gij')
gij = [[Matrix(g_ij).inv()[i, j] for j in range(0, len(g_ij))] for i in range(0, len(g_ij))]

# Función para calcular Símbolos de Christoffel
# upperIndex, lowerIndex1, lowerIndex2 son enteros 1-basados (1, 2, 3, 4)
def Christoffel(upperIndex, lowerIndex1, lowerIndex2, latex_output=True):
    
    # Obtener los símbolos de coordenadas correspondientes a los índices
    # Ahora 'indices' es la lista [t, r, theta, phi]
    upperIndexSymbol = indices[upperIndex ]
    lowerIndexSymbol1 = indices[lowerIndex1 ]
    lowerIndexSymbol2 = indices[lowerIndex2 ]

    Christoffel_sum = 0 # Usé Christoffel_sum para la variable de suma, pero tu 'Christoffel = 0' original también funciona debido al alcance.
    
    # La suma ahora itera correctamente de 0 a 3 (len(indices) es 4)
    for i in range(0, len(indices), 1): # 'i' es el índice de suma (0-basado)
        
       
        term_inv_metric = gij[upperIndex][i]
        
        diff1 = diff(g_ij[i][lowerIndex2], lowerIndexSymbol1)
        diff2 = diff(g_ij[i][lowerIndex1], lowerIndexSymbol2)
        diff3 = diff(g_ij[lowerIndex1][lowerIndex2], indices[i])
        
        Christoffel_sum += Rational(1,2)*term_inv_metric * (diff1 + diff2 - diff3)    
            # Imprimir en pantalla los coeficientes no cero
    if (Christoffel_sum != 0):
        if (latex_output == True):
            latex_str = f"\\Gamma^{{{latex_index(upperIndexSymbol)}}}{{ }}_{{{latex_index(lowerIndexSymbol1)} {latex_index(lowerIndexSymbol2)}}} &= {latex(Christoffel_sum)} \\\\"
            print(latex_str)
        else:
            latex_str = f"\\Gamma^{{{upperIndex}}}{{ }}_{{{lowerIndex1} {lowerIndex2}}} &= {latex(Christoffel_sum)} \\\\"
            print(latex_str)
    
    return Christoffel_sum

# Función para calcular todos los Símbolos de Christoffel y almacenarlos en una lista anidada   

def Christoffel_all(latex_output=False):
    """
    Crea un objeto con indices tipo tensor (que no es un tensor) que contiene todos los Christoffel

    """
    Christoffel_list = []
    for i in range(0, 4, 1):      # Índice superior k
        i_list = []
        for j in range(0, 4, 1):  # Primer índice inferior m
            j_list = []
            for k_loop in range(0, 4, 1): # Segundo índice inferior n 
                Christoffel_sym = Christoffel(i, j, k_loop, latex_output=latex_output)
                j_list.append(Christoffel_sym)
            i_list.append(j_list)
        Christoffel_list.append(i_list)

    return Christoffel_list

Christoffel_all()