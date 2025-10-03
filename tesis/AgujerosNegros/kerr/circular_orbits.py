import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, lambdify
from scipy.optimize import fsolve

# ------------------------------
# 1. PARÁMETROS DE CONFIGURACIÓN
# ------------------------------
# Constantes físicas y del agujero negro
PARAMS = {
    'm': 1.0,      # Masa del agujero negro
    'a': 0.9,      # Parámetro de espín (spin)
    'mu': 1.0,     # Masa de la partícula de prueba
    'c': 1.0       # Velocidad de la luz (unidades geometrizadas)
}

# Parámetros de simulación
R_START = PARAMS['m'] + np.sqrt(PARAMS['m']**2 - PARAMS['a']**2) + 0.1  # Justo fuera del horizonte
R_END = 6.0
N_POINTS = 5000
Q_VALS = [0, 5, 10] # Valores del parámetro de Carter a simular

# ------------------------------
# 2. DEFINICIÓN SIMBÓLICA (con SymPy)
# ------------------------------
r, a, m, E, Lz, Q, mu, c = symbols('r a m E L_z Q mu c', real=True)

# Ecuaciones de la geodésica de Kerr
delta = r**2 - 2*m*r + a**2
P_func = (r**2 + a**2)*E - a*Lz
R_func = P_func**2 - delta*(mu**2*r**2 + (Lz - a*E)**2 + Q)
R_prime = diff(R_func, r)

# ------------------------------
# 3. CONVERSIÓN A FUNCIONES NUMÉRICAS (con Lambdify)
# ------------------------------
# Se convierten las expresiones de SymPy en funciones de NumPy para un cálculo rápido.
VARIABLES = [E, Lz, r, Q, a, m, mu, c]
R_numeric = lambdify(VARIABLES, R_func, 'numpy')
R_prime_numeric = lambdify(VARIABLES, R_prime, 'numpy')

# ------------------------------
# 4. FUNCIÓN SOLUCIONADORA (con SciPy)
# ------------------------------
def solve_equations(initial_guess, r_val, Q_val, params):
    """
    Resuelve el sistema R=0 y R'=0 para E y Lz usando fsolve de SciPy.
    
    Args:
        initial_guess (list): Valores iniciales para [E, Lz].
        r_val (float): Valor del radio.
        Q_val (float): Valor del parámetro de Carter.
        params (dict): Diccionario con los parámetros del agujero negro.
        
    Returns:
        tuple: (E, Lz) o (nan, nan) si la solución no se encuentra.
    """
    # Función objetivo para fsolve. Debe devolver [0, 0] en la solución.
    def objective_func(variables):
        E_sol, Lz_sol = variables
        args = (r_val, Q_val, params['a'], params['m'], params['mu'], params['c'])
        
        eq1 = R_numeric(E_sol, Lz_sol, *args)
        eq2 = R_prime_numeric(E_sol, Lz_sol, *args)
        
        return [eq1, eq2]

    try:
        # fsolve es el equivalente numérico de nsolve
        solution, _, success_flag, _ = fsolve(objective_func, initial_guess, full_output=True)
        if success_flag == 1:
            return float(solution[0]), float(solution[1])
        else:
            return np.nan, np.nan
    except RuntimeError:
        # fsolve puede lanzar un error si no converge
        return np.nan, np.nan


r_consulta = 1.7179
q_consulta = 10
E_consulta, Lz_consulta = solve_equations([0.9, 2.0], r_consulta, q_consulta, PARAMS)
print(f"Para r={r_consulta} y Q={q_consulta}, se obtiene E={E_consulta:.6f}, Lz={Lz_consulta:.6f}")

# ------------------------------
# 5. BUCLE PRINCIPAL DE CÁLCULO
# ------------------------------
# print("Iniciando cálculos...")
# r_vals = np.linspace(R_START, R_END, N_POINTS)
# results = {}

# for q in Q_VALS:
#     print(f"Calculando para Q = {q}...")
#     E_vals, Lz_vals = [], []
#     # Valores iniciales para el primer punto del radio
#     current_guess = [0.9, 2.0] 
    
#     for rv in r_vals:
#         E_sol, Lz_sol = solve_equations(current_guess, rv, q, PARAMS)
#         E_vals.append(E_sol)
#         Lz_vals.append(Lz_sol)
        
#         # Optimización: Usa la solución actual como el valor inicial para el siguiente punto.
#         # Esto hace que el solucionador sea mucho más rápido y estable.
#         if not np.isnan(E_sol):
#             current_guess = [E_sol, Lz_sol]
            
#     results[q] = {'E': E_vals, 'Lz': Lz_vals}

# print("Cálculo finalizado.")

# # ------------------------------
# # 6. VISUALIZACIÓN DE RESULTADOS
# # ------------------------------
# # Usamos el modo orientado a objetos de Matplotlib para mayor control



# # Líneas verticales de referencia
# r_horizonte = PARAMS['m'] + np.sqrt(PARAMS['m']**2 - PARAMS['a']**2)
# r_ergoesfera = 2 * PARAMS['m']

# plt.figure()
# plt.axvline(x=r_horizonte, color='red', linestyle='--', label='Horizonte de eventos ($r_+$)')
# plt.axvline(x=r_ergoesfera, color='black', linestyle=':', label='Ergoesfera estática ($r_E$)')
# plt.grid(True, linestyle='--', alpha=0.6)

# # Gráfica para E(r)
# for q, data in results.items():
#     plt.plot(r_vals, data['E'], label=f'Q={q}')
# plt.ylabel("E")
# plt.xlabel("r")
# plt.legend()
# plt.ylim(0, 6)

# plt.show()


# plt.figure()
# plt.axvline(x=r_horizonte, color='red', linestyle='--', label='Horizonte de eventos ($r_+$)')
# plt.axvline(x=r_ergoesfera, color='black', linestyle=':', label='Ergoesfera estática ($r_E$)')
# plt.grid(True, linestyle='--', alpha=0.6)   
# # Gráfica para Lz(r)
# for q, data in results.items():
#     plt.plot(r_vals, data['Lz'], label=f'Q={q}')
# plt.ylabel("$L_z$")
# plt.xlabel("r")
# plt.legend()
# plt.ylim(0, 6)

# plt.show()
