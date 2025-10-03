import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.patches import Circle


# --- Variables Globales para el Manejo de Puntos de Inflexión ---
# Guardan el signo de la velocidad para saber si la partícula va hacia adentro/afuera
# o hacia arriba/abajo.
sign_r = 1.0  # Empezamos moviéndonos hacia afuera
sign_theta = 1.0 # Empezamos moviéndonos hacia el polo norte

# Guardan el valor de la derivada anterior para ayudar a detectar el cambio de signo.
dr_dtau_prev = 0.0
dtheta_dtau_prev = 0.0


# Constantes del agujero negro
a = 0.9
m = 1.0
c = 1.0

# Constantes de la geodésica
# Estas se calclulan por separado
# Constantes de movimiento para una órbita inclinada y en precesión
E = 0.816497 # Energía 
Lz = -0.367423 # Momento angular axial
Q = 0 # Constante de Carter (alta para una gran inclinación)
mu = 1    # Masa de la partícula (1 para masiva, 0 para fotón)

# Condiciones iniciales [r0, theta0, phi0, t0]
r0 = 6*m
theta0 = np.pi / 2  # Inclinación inicial de 90 grados respecto al ecuador
phi0 = 0.0
t0 = 0.0
y0 = [r0, theta0, phi0, t0]

name = "geodesica_caida"

tau_max = 800  # Tiempo Mino máximo para la integración
tau_span = [0, tau_max]
numpoints = 20000  # Número de puntos en la solución

def kerr_geodesics(tau, y, m, a, E, Lz, Q,c, mu):
    """
    Define el sistema de EDOs para las geodésicas de Kerr en tiempo Mino (tau).
    El vector de estado es y = [r, theta, phi, t].
    """
    global sign_r, sign_theta, dr_dtau_prev, dtheta_dtau_prev
    r, theta, phi, t = y

    # Términos auxiliares de la métrica
    Delta = r**2 - 2 * m * r + a**2


    Rr = ((r**2 + a**2) * (E/c) - a * Lz)**2 - Delta * ((mu * c * r)**2 + (Lz - a * (E/c))**2 + Q)

    # El término np.sin(theta)**2 + 1e-9 evita la división por cero en los polos.
    Th = Q - np.cos(theta)**2 * (Lz**2 / (np.sin(theta)**2 + 1e-9)+a**2 * ((mu* c)**2 - (E/c)**2))

    # Se truncan a cero valores negativos pequeños que puedan surgir de errores de precisión.
    Rr = max(Rr, 0.0)
    Th = max(Th, 0.0)

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

    dphi_dtau = (Lz / (np.sin(theta)**2 + 1e-9) - a * (E/c)) + (a *((r**2 + a**2) * (E/c) - a * Lz) / Delta)

    dt_dtau = - a * (a * (E/c) * np.sin(theta)**2 - Lz) + ((r**2 + a**2) * ((r**2 + a**2) * (E/c) - a * Lz) / Delta)

    return [dr_dtau, dtheta_dtau, dphi_dtau, dt_dtau]

print("Iniciando la integración numérica...")

# Genera 2000 puntos espaciados uniformemente para una curva suave.
t_eval_points = np.linspace(tau_span[0], tau_span[1], numpoints) 

# Llamada al solver de EDOs de SciPy
sol = solve_ivp(
    fun=kerr_geodesics,
    t_span=tau_span,
    y0=y0,
    args=(m, a, E, Lz, Q, c, mu),
    method='Radau',      # Un método robusto para este tipo de problemas
    dense_output=True,   # Permite obtener una solución continua y suave
    rtol=1e-8,           # Tolerancia relativa para alta precisión
    atol=1e-8,           # Tolerancia absoluta
    #t_eval=t_eval_points # Puntos donde se evalúa la solución
)


print("Integración completada con éxito.")


# Extraer los resultados de la solución
r, theta, phi, t = sol.y

# --- 3. Visualización de la Órbita ---

print("Generando la visualización 3D...")

# Convertir de coordenadas de Boyer-Lindquist a cartesianas para la gráfica
x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)

# Crear la figura y el eje 3D
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Malla de parámetros
u = np.linspace(0, 2 * np.pi, 200)
v = np.linspace(0, np.pi, 200)

# Ergoesfera
r_e = m + np.sqrt(m**2 - (a*np.cos(v))**2)
x_e = r_e * np.outer(np.cos(u), np.sin(v))
y_e = r_e * np.outer(np.sin(u), np.sin(v))
z_e = r_e * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x_e, y_e, z_e, color='purple', alpha=0.25, rstride=5, cstride=5)

# Horizonte de sucesos
r_h = m + np.sqrt(m**2 - a**2)
x_bh = r_h * np.outer(np.cos(u), np.sin(v))
y_bh = r_h * np.outer(np.sin(u), np.sin(v))
z_bh = r_h * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x_bh, y_bh, z_bh, color='black', alpha=0.6, rstride=5, cstride=5)

# Círculo del horizonte en el plano ecuatorial
theta = np.linspace(0, 2*np.pi, 400)
x_circ = a * np.cos(theta)
y_circ = a * np.sin(theta)
z_circ = np.zeros_like(theta)
ax.plot(x_circ, y_circ, z_circ, color="red", lw=2, label="Singularidad r=a")

# --- Trayectoria (se dibuja al final, queda arriba de todo) ---
ax.plot(x, y, z, label='Trayectoria Geodésica', lw=1, color='cyan')

# Configuración de la gráfica
#ax.set_title("Orbita en el espacio-tiempo de Kerr", fontsize=16)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend()

legend_elements = [
    Patch(facecolor='purple', edgecolor='k', alpha=0.25, label='Ergoesfera'),
    Patch(facecolor='black', edgecolor='k', alpha=0.6, label='Horizonte de sucesos'),
]

ax.legend(handles=legend_elements + ax.get_legend_handles_labels()[0], loc="upper right")

# Ajustar límites
max_range = np.max(np.abs([x, y, z])) * 1.2
ax.set_xlim([-max_range, max_range])
ax.set_ylim([-max_range, max_range])
ax.set_zlim([-max_range, max_range])

# Ángulo de vista
ax.view_init(elev=30, azim=45)




# Fondo blanco
ax.set_facecolor("white")
plt.tight_layout()
plt.savefig(f'geodesics_plots/{name}.png', dpi=300,bbox_inches='tight',)



fig, ax = plt.subplots(figsize=(8, 8))

# Trayectoria proyectada en XY
ax.plot(x, y, color="cyan", lw=1, label="Trayectoria Geodésica")

# Horizonte de sucesos (círculo en XY)
circle_h = Circle((0, 0), r_h, color="black", alpha=0.6, label="Horizonte de sucesos")
ax.add_patch(circle_h)

# Ergoesfera (círculo en XY en el ecuador, donde θ = π/2 → cosθ=0)
r_e_eq = m + np.sqrt(m**2 - 0)  # ergo radio en el ecuador
circle_e = Circle((0, 0), r_e_eq, color="purple", alpha=0.25, label="Ergoesfera")
ax.add_patch(circle_e)

#Singularidad
circle_s = Circle((0, 0), a, color="red", alpha=0.9, label="Singularidad", fill=False)
ax.add_patch(circle_s)

# Configuración
ax.set_aspect("equal")
ax.set_xlabel("X")
ax.set_ylabel("Y")

ax.legend()


plt.savefig(f'geodesics_plots/{name}_planoxy.png', dpi=300,bbox_inches='tight',)


