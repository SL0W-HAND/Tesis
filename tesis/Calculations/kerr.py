from sympy import symbols, Matrix, sin, cos, simplify, pretty_print

# ------------------------------
# Definición de símbolos
# ------------------------------
t, r, theta, phi = symbols('t r theta phi', real=True)
a, m = symbols('a m', real=True)
# Estas son las variables objetivo para el resultado final
delta_s, rho_s, sigma_s = symbols('delta rho sigma', real=True)

# ------------------------------
# Definición de las expresiones completas
# ------------------------------
delta = r**2 - 2*m*r + a**2
rho = r**2 + a**2*cos(theta)**2
# Definimos sigma en términos de delta para asegurar consistencia
sigma = (r**2 + a**2)**2 - a**2*sin(theta)**2*delta

# ------------------------------
# Métrica de Kerr (g_ij)
# ------------------------------
# Se construye usando las expresiones para mantenerla legible
g_ij = Matrix([
    [-(1 - 2*m*r/rho),          0, 0, -2*m*a*r*sin(theta)**2/rho],
    [0,                             rho/delta, 0, 0],
    [0,                             0, rho, 0],
    [-2*m*a*r*sin(theta)**2/rho, 0, 0, sigma*sin(theta)**2/rho]
])

gij = Matrix([[-sigma/(delta*rho), 0, 0, -2*a*m*r/(delta*rho)], 
              [0, delta/rho, 0, 0], 
              [0, 0, 1/rho, 0], 
              [-2*a*m*r/(delta*rho), 0, 0, (-2*m*r + rho)/(delta*rho*sin(theta)**2)]
              ])
# ------------------------------
# ecuaciones de geodésicas
# ------------------------------
#constantes de movimiento
E = 0.95  # Energía específica
Lz = 3.0  # Momento angular específico
Q = 15.0  # Constante de Carter
# Parámetros del agujero
m = 1.0  #
a = 0.95  # Parámetro de espín
mu = 1.0  # Masa de la partícula (1 para masa normalizada)
c = 1.0   # Velocidad de la luz (1 en unidades naturales)
## Funciones auxiliares
def theta_func(theta):
    return Q - cos(theta)**2 *((Lz**2)/(sin(theta)**2) + a**2*(mu*c - E**2))
def P_func(r):
    return E*(r**2 + a**2) - a*Lz
def R_func(r):
    return (P_func(r))**2 - delta*(mu**2*r**2*c**2 + (Lz - a*E)**2 + Q)

