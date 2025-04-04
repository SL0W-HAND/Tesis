from sympy import *

r, theta, phi, Gamma = symbols('r theta phi Gamma')
indices = symbols(['r', 'theta', 'phi'])
A = Function('A')(r)

# Función para convertir índices a su forma de LaTeX
def latex_index(index):
    # Diccionario para mapear los nombres de índices a sus equivalentes en LaTeX
    index_dict = {'r': 'r', 'theta': '\\theta', 'phi': '\\phi'}
    return index_dict.get(str(index), str(index))
christoffelSymbols = []
init_printing(use_unicode=True)

g_ij = [
    [A,0,0],
    [0,r**2,0],
    [0,0,r**2*(sin(theta))**2]
]

gij = [[Matrix(g_ij).inv()[i-1, j-1] for j in range(1, 4)] for i in range(1, 4)]

def Christoffel(upperIndex,lowerIndex1,lowerIndex2):
    upperIndexSymbol = indices[upperIndex - 1]
    lowerIndexSymbol1 = indices[lowerIndex1 - 1]
    lowerIndexSymbol2 = indices[lowerIndex2 - 1]

    Christoffel = 0 
    for i in range(0,len(indices),1):
        Christoffel = Christoffel +Rational(1,2)*gij[upperIndex-1][i]*(diff(g_ij[i][lowerIndex2-1],lowerIndexSymbol1)+diff(g_ij[i][lowerIndex1-1],lowerIndexSymbol2)-diff(g_ij[lowerIndex1-1][lowerIndex2-1],indices[i]))
   

    # Simplificar la expresión para evitar decimales
    Christoffel_simplified = simplify(Christoffel)

    # Crear la cadena de LaTeX personalizada con el espacio entre índices
    latex_str = f"\\Gamma^{{{latex_index(upperIndexSymbol)}}}{{}}_{{{latex_index(lowerIndexSymbol1)} {latex_index(lowerIndexSymbol2)}}} &= {latex(Christoffel_simplified)} \\\\"
    
    print(latex_str)  # Muestra en formato LaTeX personalizado
    return latex_str
    
#calcular todos los simbolos de Christoffel
for i in range(1,4,1):
    for j in range(1,4,1):
        for k in range(1,4,1):
            Christoffel(i,j,k)
