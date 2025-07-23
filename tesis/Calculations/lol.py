from sympy import symbols, trigsimp, factor, cancel, Matrix, Rational, diff, simplify, latex, init_printing, sin, cos

# Inicializa impresión simbólica bonita
init_printing(use_unicode=True)

# Coordenadas y parámetros
t, r, theta, phi = symbols('t r theta phi')
indices = [t, r, theta, phi]

a, m = symbols('a m', real=True)
delta_s, sigma_s, rho_s = symbols('Delta Sigma rho', real=True)  # versiones simplificadas para sustituciones

# Subexpresiones comunes
sin2 = sin(theta)**2
cos2 = cos(theta)**2
delta = r**2 - 2*m*r + a**2
sigma = (r**2 + a**2)**2 - a**2 * sin2 * delta
rho = r**2 + a**2 * cos2
rho2 = rho

# Métrica de Kerr (g_ij)
g_ij = [
    [-(1 - 2*m*r/rho2), 0, 0, -2*m*a*r*sin2/rho2],
    [0, rho2/delta, 0, 0],
    [0, 0, rho2, 0],
    [-2*m*a*r*sin2/rho2, 0, 0, sigma*sin2/rho2]
]

# Inversa de la métrica g^ij
gij_matrix = Matrix(g_ij).inv()
gij = [[gij_matrix[i, j] for j in range(4)] for i in range(4)]

# Diccionario para convertir índices a LaTeX
def latex_index(index_symbol):
    index_dict = {'t': 't', 'r': 'r', 'theta': '\\theta', 'phi': '\\phi'}
    return index_dict.get(str(index_symbol), str(index_symbol))

# Reemplazos para simplificación
replacements = {
    r**2 - 2*m*r + a**2: delta_s,
    (r**2 + a**2)**2 - a**2 * sin2 * delta: sigma_s,
    r**2 + a**2 * cos2: rho_s
}

# Función para calcular un símbolo de Christoffel
def Christoffel(upperIndex, lowerIndex1, lowerIndex2):
    upper = indices[upperIndex - 1]
    lower1 = indices[lowerIndex1 - 1]
    lower2 = indices[lowerIndex2 - 1]

    summation = 0
    for i in range(4):
        g_inv = gij[upperIndex - 1][i]
        term1 = diff(g_ij[i][lowerIndex2 - 1], lower1)
        term2 = diff(g_ij[i][lowerIndex1 - 1], lower2)
        term3 = diff(g_ij[lowerIndex1 - 1][lowerIndex2 - 1], indices[i])
        summation += Rational(1, 2) * g_inv * (term1 + term2 - term3)

    expr = summation.subs(replacements)
    expr = trigsimp(cancel(expr))

    if expr != 0:
        latex_str = f"\\Gamma^{{{latex_index(upper)}}}{{ }}_{{{latex_index(lower1)} {latex_index(lower2)}}} &= {latex(expr)} \\\\"
        print(latex_str)
        return latex_str

# Calcular todos los símbolos
print("Calculando los símbolos de Christoffel para la métrica de Kerr:\n")

for i in range(1, 5):        # Índice superior
    for j in range(1, 5):    # Índice inferior 1
        for k in range(1, 5):  # Índice inferior 2
            Christoffel(i, j, k)

print("\nCálculo completado.")
