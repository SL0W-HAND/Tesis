# -*- coding: utf-8 -*-
"""
Solver numérico para geodésicas de Kerr.
Escenario: Órbita inclinada mostrando la precesión de Lense-Thirring.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# --- Variables Globales para el Manejo de Puntos de Inflexión ---
# Guardan el signo de la velocidad para saber si la partícula va hacia adentro/afuera
# o hacia arriba/abajo.
sign_r = 1.0  # Empezamos moviéndonos hacia afuera
sign_theta = 1.0 # Empezamos moviéndonos hacia el polo norte

# Guardan el valor de la derivada anterior para ayudar a detectar el cambio de signo.
dr_dtau_prev = 0.0
dtheta_dtau_prev = 0.0

# --- 1. Definición del Sistema de Ecuaciones Diferenciales ---

def kerr_geodesics(tau, y, M, a, E, Lz, Q):
    """
    Define el sistema de EDOs para las geodésicas de Kerr en tiempo Mino (tau).
    El vector de estado es y = [r, theta, phi, t].
    """
    global sign_r, sign_theta, dr_dtau_prev, dtheta_dtau_prev
    r, theta, phi, t = y

    # Términos auxiliares de la métrica
    rho2 = r**2 + a**2 * np.cos(theta)**2
    Delta = r**2 - 2 * M * r + a**2

    # Potencial radial V_r(r). Define las regiones permitidas para el movimiento radial.
    Rr = ((r**2 + a**2) * E - a * Lz)**2 - Delta * (r**2 + (Lz - a * E)**2 + Q)
    
    # Potencial polar V_theta(theta). Define las regiones permitidas para el movimiento latitudinal.
    # El término np.sin(theta)**2 + 1e-9 evita la división por cero en los polos.
    Th = Q - np.cos(theta)**2 * (a**2 * (1 - E**2) + Lz**2 / (np.sin(theta)**2 + 1e-9))
    
    # Se truncan a cero valores negativos pequeños que puedan surgir de errores de precisión.
    if Rr < 0: Rr = 0
    if Th < 0: Th = 0

    # Detección y manejo simple de puntos de inflexión (turning points)
    # Si el potencial es casi cero y la velocidad anterior era mayor, invertimos la dirección.
    if Rr < 1e-7 and dr_dtau_prev**2 > Rr:
        sign_r *= -1
    if Th < 1e-7 and dtheta_dtau_prev**2 > Th:
        sign_theta *= -1

    # Derivadas con respecto al tiempo Mino (tau)
    dr_dtau = sign_r * np.sqrt(Rr)
    dtheta_dtau = sign_theta * np.sqrt(Th)
    
    # Actualizamos los valores de las derivadas para la siguiente iteración
    dr_dtau_prev = dr_dtau
    dtheta_dtau_prev = dtheta_dtau
    
    dphi_dtau = (a * ((r**2 + a**2) * E - a * Lz) / Delta) + (Lz / (np.sin(theta)**2 + 1e-9) - a * E)
    dt_dtau = ((r**2 + a**2) * ((r**2 + a**2) * E - a * Lz) / Delta) - a * (a * E * np.sin(theta)**2 - Lz)

    return [dr_dtau, dtheta_dtau, dphi_dtau, dt_dtau]

# --- 2. Configuración y Ejecución de la Simulación ---

if __name__ == '__main__':
    # Parámetros del agujero negro
    M = 1.0      # Masa (normalizada a 1)
    a = 0.95     # Parámetro de espín (alto para un efecto de arrastre notable)

    # Constantes de movimiento para una órbita inclinada y en precesión
    E = 0.95     # Energía por unidad de masa
    Lz = 3.0     # Momento angular axial
    Q = 15.0     # Constante de Carter (alta para una gran inclinación)

    # Condiciones iniciales [r0, theta0, phi0, t0]
    r0 = 6.0
    theta0 = np.pi / 3  # Inclinación inicial de 60 grados respecto al ecuador
    phi0 = 0.0
    t0 = 0.0
    y0 = [r0, theta0, phi0, t0]

    # Rango de integración en tiempo Mino (suficientemente largo para ver la precesión)
    tau_max = 3500
    tau_span = [0, tau_max]

    print("🚀 Iniciando la integración numérica para la órbita precesante...")

    # Llamada al solver de EDOs de SciPy
    sol = solve_ivp(
        fun=kerr_geodesics,
        t_span=tau_span,
        y0=y0,
        args=(M, a, E, Lz, Q),
        method='Radau',      # Un método robusto para este tipo de problemas
        dense_output=True,   # Permite obtener una solución continua y suave
        rtol=1e-8,           # Tolerancia relativa para alta precisión
        atol=1e-8            # Tolerancia absoluta
    )

    print("✅ Integración completada con éxito.")

    # Extraer los resultados de la solución
    r, theta, phi, t = sol.y

    # --- 3. Visualización de la Órbita ---

    print("🎨 Generando la visualización 3D...")
    
    # Convertir de coordenadas de Boyer-Lindquist a cartesianas para la gráfica
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    # Crear la figura y el eje 3D
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Dibujar la trayectoria de la partícula
    ax.plot(x, y, z, label='Órbita Precesante', lw=1, color='cyan')
    
    # 
    
    # Dibujar una esfera negra para representar el horizonte de eventos
    r_h = M + np.sqrt(M**2 - a**2)  # Radio del horizonte de eventos exterior
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x_bh = r_h * np.outer(np.cos(u), np.sin(v))
    y_bh = r_h * np.outer(np.sin(u), np.sin(v))
    z_bh = r_h * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x_bh, y_bh, z_bh, color='black', rstride=5, cstride=5, zorder=10)

    # Configuración de la gráfica para una mejor visualización
    ax.set_title("Precesión de Lense-Thirring en el Espaciotiempo de Kerr", fontsize=16)
    ax.set_xlabel("X / M")
    ax.set_ylabel("Y / M")
    ax.set_zlabel("Z / M")
    ax.legend()
    
    # Ajustar los límites para centrar la vista en la órbita
    max_range = np.max(np.abs([x, y, z])) * 1.1
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])
    
    ax.view_init(elev=30, azim=45) # Ángulo de vista
    ax.set_facecolor('black') # Fondo oscuro para un look espacial
    fig.tight_layout()
    plt.show()