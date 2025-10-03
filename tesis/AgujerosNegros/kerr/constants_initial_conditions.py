import numpy as np
from sympy import symbols, Matrix, sin, cos, solveset

# ------------------------------
# 1. Definición de Símbolos
# ------------------------------
r, theta = symbols('r, theta', real=True)
a, M = symbols('a, M', real=True, positive=True)

# ------------------------------
# 2. Definición de Expresiones Auxiliares
# ------------------------------
delta = r**2 - 2 * M * r + a**2
rho2 = r**2 + a**2 * cos(theta)**2
sigma = (r**2 + a**2)**2 - a**2 * sin(theta)**2 * delta

# ------------------------------
# 3. Métrica de Kerr (Covariante g_μν)
# ------------------------------
g_uv = Matrix([
    [-(1 - 2 * M * r / rho2), 0, 0, -2 * M * a * r * sin(theta)**2 / rho2],
    [0, rho2 / delta, 0, 0],
    [0, 0, rho2, 0],
    [-2 * M * a * r * sin(theta)**2 / rho2, 0, 0, sigma * sin(theta)**2 / rho2]
])

# ------------------------------
# 4. Función para Calcular las Constantes de Movimiento Totales
# ------------------------------

def get_total_constants_of_motion(r_0: float, theta_0: float, 
                                  u_r0: float, u_theta0: float, u_phi0: float, 
                                  a_val: float = 0.9, M_val: float = 1.0,
                                  mu: float = 1.0, c: float = 1.0):
    """
    Calcula las constantes de movimiento TOTALES.
    Versión robusta que maneja correctamente el caso ecuatorial (theta = pi/2).
    """
    g_uv_val = g_uv.subs([(r, r_0), (theta, theta_0), (a, a_val), (M, M_val)])

    u_t0_sym = symbols('u_t', real=True, positive=True)
    u_vector = [u_t0_sym, u_r0, u_theta0, u_phi0]
    
    # Ecuación de normalización: g_μν * U^μ * U^ν = -c^2
    norm_eq = sum(g_uv_val[i, j] * u_vector[i] * u_vector[j] for i in range(4) for j in range(4)) + c**2
    
    solutions = solveset(norm_eq, u_t0_sym)
    u_t0_val = None
    for sol in solutions:
        if sol.is_real and sol > 0:
            u_t0_val = float(sol)
            break
            
    if u_t0_val is None:
        raise ValueError("No se encontró una solución real y positiva para dt/dτ. Revisa las condiciones iniciales.")

    # Calcular E y Lz (escalados por la masa mu)
    E = mu * -(g_uv_val[0, 0] * u_t0_val + g_uv_val[0, 3] * u_phi0)
    Lz = mu * (g_uv_val[3, 0] * u_t0_val + g_uv_val[3, 3] * u_phi0)

    # --- Calcular la Constante de Carter Total (Q) - FORMA ROBUSTA ---
    rho2_val = float(rho2.subs([(r, r_0), (theta, theta_0), (a, a_val)]))
    
    # Comprobar si estamos en el ecuador para usar la fórmula simplificada
    # Se usa una pequeña tolerancia para evitar errores de punto flotante
    if abs(theta_0 - np.pi/2) < 1e-9:
        # En el ecuador, cos(theta) es 0, por lo que Q se simplifica drásticamente
        Q = (mu * r_0**2 * u_theta0)**2 #  rho2 en el ecuador es r^2
    else:
        # Si no estamos en el ecuador, usamos la fórmula completa
        cos_theta0_val = cos(theta_0)
        sin_theta0_val = sin(theta_0)

        p_theta_sq = (mu * rho2_val * u_theta0)**2

        if abs(sin_theta0_val) < 1e-9:
            term_Lz = 0 if abs(Lz) < 1e-9 else float('inf')
        else:
            term_Lz = Lz**2 / sin_theta0_val**2

        term_E = a_val**2 * (mu**2 * c**2 - E**2 / c**2)
        Q = p_theta_sq + cos_theta0_val**2 * (term_Lz + term_E)

    return E, Lz, Q

# ------------------------------
# 5. Ejemplo de Uso 
# ------------------------------
print("--- Test partícula en caída ---")
try:
    E_fall, Lz_fall, Q_fall = get_total_constants_of_motion(
        r_0=6.0, theta_0=np.pi/2, 
        u_r0=0.0, u_theta0=0.0, u_phi0=0.0,
        a_val=0.9, M_val=1.0, mu=1.0, c=1.0
    )
    print(f"  - Energía Total: {E_fall:.6f}")
    print(f"  - Momento Angular Total: {Lz_fall:.6f}")
    print(f"  - Constante de Carter Total: {Q_fall:.6f}")

except ValueError as e:
    print(f"Error: {e}")
