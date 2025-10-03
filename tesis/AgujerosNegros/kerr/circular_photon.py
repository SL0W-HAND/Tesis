from sympy import symbols, Eq, sin, cos, nsolve, latex
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# Definición de símbolos
# ------------------------------
r, a, m, xi, eta = symbols('r a m xi eta', real=True)

# ------------------------------
# Definición de funciones
# ------------------------------
Delta = r**2 - 2*m*r + a**2

# Potencial radial para fotones en términos de parámetros de impacto
R_func = (r**2 + a**2 - a*xi)**2 - Delta*((xi - a)**2 + eta)

# Derivada radial
R_prime = R_func.diff(r).simplify()

# ------------------------------
# Parámetros físicos
# ------------------------------
params = {a: 0.9, m: 1}  # Agujero negro de Kerr en rotación
r_horizonte = params[m] + np.sqrt(params[m]**2 - params[a]**2)
r_static_limit = 2 * params[m]  # Límite estático en el ecuador

# Rango de radios candidatos
r_vals = np.linspace(r_horizonte, 4.5, 200)

xi_vals = []
eta_vals = []
# Estimación inicial para el primer punto del bucle
initial_guess = [2, 5]

# ------------------------------
# Resolver condiciones R=0, R'=0
# ------------------------------
# Para encontrar las órbitas fotónicas circulares e inestables, buscamos los
# máximos del potencial radial efectivo. Esto ocurre cuando el potencial (R) y
# su primera derivada (R') son cero simultáneamente.
for rv in r_vals:
    try:
        # Resolver el sistema de ecuaciones usando la estimación inicial
        sol = nsolve([R_func.subs({**params, r: rv}),
                      R_prime.subs({**params, r: rv})],
                     [xi, eta],
                     initial_guess)  # Usar la estimación actual

        xi_vals.append(float(sol[0]))
        eta_vals.append(float(sol[1]))

        # Actualizar la estimación para la siguiente iteración con la solución encontrada
        initial_guess = [sol[0], sol[1]]

    except:
        # Si el solver falla, se añade NaN y se podría resetear la estimación
        xi_vals.append(np.nan)
        eta_vals.append(np.nan)
        # initial_guess = [2, 5] # Opcional: resetear si falla

# ------------------------------
# Graficar resultados
# ------------------------------
plt.figure(figsize=(10, 6))
plt.plot(r_vals, xi_vals, label=r"$\xi(r)$")
plt.xlabel("r")
plt.ylabel(r" $\xi$")
plt.title(f"Parámetro de impacto $\\xi$ para un agujero de Kerr (a={params[a]})")
plt.axvline(x=r_horizonte, color='red', linestyle='--', label='Horizonte de eventos ($r_+$)')
plt.axvline(x=r_static_limit, color='black', linestyle=':', label='Ergoesfera ecuatorial ($2m$)')
plt.grid(True)
plt.legend()
plt.savefig("geodesics_plots/circular_xi_vs_r_kerr.png", dpi=300,bbox_inches='tight',)

plt.figure(figsize=(10, 6))
plt.plot(r_vals, eta_vals, label=r"$\eta(r)$", color='green')
plt.xlabel("r")
plt.ylabel(r"$\eta$")
plt.title(f"Parámetro de impacto $\\eta$ para un agujero de Kerr (a={params[a]})")
plt.axvline(x=r_horizonte, color='red', linestyle='--', label='Horizonte de eventos ($r_+$)')
plt.axvline(x=r_static_limit, color='black', linestyle=':', label='Ergoesfera ecuatorial ($2m$)')
plt.grid(True)
plt.legend()
plt.savefig("geodesics_plots/circular_eta_vs_r_kerr.png", dpi=300,bbox_inches='tight',)

## ------------------------------
## for individual point
#import sympy as sp

## --- Símbolos ---
# r = sp.Symbol('r', real=True)
# xi, eta = sp.symbols('xi eta', real=True)
# a, m = sp.symbols('a m', real=True)

# # Definiciones
# Delta = r**2 - 2*m*r + a**2
# R_expr = (r**2 + a**2 - a*xi)**2 - Delta * ((xi - a)**2 + eta)

# # Condiciones para órbitas de fotones
# eq1 = sp.Eq(R_expr, 0)
# eq2 = sp.Eq(sp.diff(R_expr, r), 0)

# # Parámetros del agujero negro
# params = {a:0.9, m:1.0}

# # Ejemplo: órbita de fotón en r=3M
# r_val = 1.70
# sol = sp.solve([eq1.subs({**params, r:r_val}),
#                 eq2.subs({**params, r:r_val})],
#                [xi, eta], dict=True)

# print(f"Soluciones para r={r_val}:")
# for s in sol:
#     xi_val = float(s[xi].evalf())
#     eta_val = float(s[eta].evalf())
#     print(f"xi = {xi_val:.6f}, eta = {eta_val:.6f}")