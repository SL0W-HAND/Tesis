from sympy import cancel, latex, symbols, Matrix, sin, cos, simplify, pretty_print, roots, together, factor, trigsimp

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
## Funciones auxiliares
eta,E, Lz, Q, mu, c = symbols('\\eta E Lz Q mu c', real=True)

P_func = E*(r**2 + a**2) - a*Lz
R_func = (P_func)**2 - delta*(mu**2*r**2*c**2 + (Lz - a*E)**2 + Q)
theta_func = Q - cos(theta)**2 *((Lz**2)/(sin(theta)**2) + a**2*(mu*c - E**2))

# ------------------------------
# derivada de R

R_prime = R_func.diff(r).simplify()
pretty_print(R_prime)
#print(latex(R_prime))
R_prime = R_prime.subs(r,eta*m)
pretty_print(R_prime)

# ------------------------------
zeros = roots(R_prime, eta)


delta_s, rho_s, sigma_s = symbols('delta rho sigma', real=True)

subs_dict = {
    sigma: sigma_s,
    delta: delta_s,
    rho: rho_s
}

for key, value in zeros.items():
    print(f"r = {simplify(key)}, multiplicidad = {value}")
pretty_print(zeros)