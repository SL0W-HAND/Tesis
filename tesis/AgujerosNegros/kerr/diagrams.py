import numpy as np
from manim import *



class kerr_BH_regions(ThreeDScene):
    def construct(self):
        # Fondo blanco
        self.camera.background_color = "#FFFFFF"

        # Ejes 3D
        axes = ThreeDAxes(
            axis_config={"color": GREY},
        )

        # Parámetros del agujero negro
        a = 0.99  # momento angular (rotación)
        m = 1   # masa

        r_plus = m + np.sqrt(m**2 - a**2)   # horizonte externo
        r_minus = m - np.sqrt(m**2 - a**2)  # horizonte interno

        # --------------------
        # Singularidad en anillo
        # --------------------
        ring = ParametricFunction(
            lambda u: (a * np.cos(u), a * np.sin(u), 0),
            t_range=[0, TAU],
            color=RED
        )
        ring_label = Text("Singularidad en anillo", color=RED, font_size=28).next_to(ring, DOWN, buff=0.3)

        # --------------------
        # Horizonte externo (esfera)
        # --------------------
        def horizon_outer_func(u, v):
            x = r_plus * np.sin(u) * np.cos(v)
            y = r_plus * np.sin(u) * np.sin(v)
            z = r_plus * np.cos(u)
            return np.array([x, y, z])
        horizon_outer = Surface(
            horizon_outer_func,
            u_range=[0, np.pi],
            v_range=[0.5*np.pi, 2 * np.pi],
            checkerboard_colors=[BLUE, BLUE],
            fill_opacity=0.15
        )
        horizon_outer_label = Text("Horizonte de eventos", color=BLUE, font_size=28).next_to(horizon_outer, UP+RIGHT, buff=0.3)

        # --------------------
        # Horizonte interno (esfera)
        # --------------------
        def horizon_inner_func(u, v):
            x = r_minus * np.sin(u) * np.cos(v)
            y = r_minus * np.sin(u) * np.sin(v)
            z = r_minus * np.cos(u)
            return np.array([x, y, z])
        horizon_inner = Surface(
            horizon_inner_func,
            u_range=[0, np.pi],
            v_range=[0.5*np.pi, 2 * np.pi],
            checkerboard_colors=[GREEN, GREEN],
            fill_opacity=0.15
        )
        horizon_inner_label = Text("Horizonte interno", color=GREEN, font_size=28).next_to(horizon_inner, LEFT, buff=0.3)

        # --------------------
        # Ergosfera (esfera deformada en z)
        # --------------------
        def ergosphere_func(u, v):
            r_ergosphere = m + np.sqrt(m**2 - a**2 * np.cos(u)**2)
            x = r_ergosphere * np.sin(u) * np.cos(v)
            y = r_ergosphere * np.sin(u) * np.sin(v)
            z = r_ergosphere * np.cos(u)
            return np.array([x, y, z])
        ergosphere = Surface(
            ergosphere_func,
            u_range=[0, np.pi],
            v_range=[0.5*np.pi, 2 * np.pi],
            checkerboard_colors=[ORANGE, ORANGE],
            fill_opacity=0.15
        )
        ergosphere_label = Text("Ergosfera", color=ORANGE, font_size=28).next_to(ergosphere, OUT, buff=0.3)
        
        # --------------------
        # Ergosfera interna
        # --------------------
        def ergosphere_inner_func(u, v):
            r_ergo_inner = m - np.sqrt(m**2 - a**2 * np.cos(u)**2)
            x = r_ergo_inner * np.sin(u) * np.cos(v)
            y = r_ergo_inner * np.sin(u) * np.sin(v)
            z = r_ergo_inner * np.cos(u)
            return np.array([x, y, z])

        interior_ergosphere = Surface(
            ergosphere_inner_func,
            u_range=[0, np.pi],
            v_range=[0, 2*np.pi],
            checkerboard_colors=[YELLOW, YELLOW],
            fill_opacity=0.15
        )
        ergosphere_inner_label = Text(
            "Ergosfera interna",
            color=YELLOW,
            font_size=28
        ).next_to(interior_ergosphere, IN, buff=0.5)
        #---------------
        # Agrupamos todo
        # --------------------
        bh_group = VGroup(
            axes,ring, horizon_outer, horizon_inner, ergosphere, interior_ergosphere,
            horizon_outer_label, horizon_inner_label, ergosphere_label, ring_label
        )

        self.set_camera_orientation(theta=45 * DEGREES, phi=75 * DEGREES,zoom=2.5)
        self.add(bh_group)



class GeodesicFunction(Scene):
    def construct(self):
        # Fondo blanco
        self.camera.background_color = "#FFFFFF"

        # Parámetros físicos
        E = 0.95   # Energía específica
        Lz = 3.0   # Momento angular específico
        Q = 15.0   # Constante de Carter
        m = 1.0    # Masa del agujero
        a = 0.95   # Parámetro de espín
        mu = 1.0   # Masa de la partícula
        c = 1.0    # Velocidad de la luz

        # Funciones auxiliares
        def delta(r):
            return r**2 - 2*m*r + a**2

        def P_func(r):
            return E*(r**2 + a**2) - a*Lz

        def R_func(r):
            return (P_func(r))**2 - delta(r)*(mu**2*r**2*c**2 + (Lz - a*E)**2 + Q)

        # Sistema de ejes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-50, 200, 50],
            axis_config={"color": BLACK},
            x_length=6,
            y_length=4
        ).to_edge(LEFT, buff=1)

        # Gráfica de R(r)
        graph = axes.plot(R_func, x_range=[0.1, 10], color=BLUE)

        # Etiquetas de los ejes
        labels = axes.get_axis_labels(x_label="r", y_label="R(r)")

        # Texto del título
        title = Text("Función Geodésica R(r)", font_size=36, color=BLACK).to_edge(UP, buff=0.5)

        # Texto explicativo de la fórmula
        R_text = MathTex(
            "R(r) = (E(r^2+a^2) - aL_z)^2 - \\Delta(r) (\\mu^2 r^2 + (L_z - aE)^2 + Q)",
            font_size=28,
            color=BLACK
        ).to_edge(DOWN, buff=0.5)

        # Añadir todo en la escena
        self.play(Write(title))
        self.play(Create(axes), Write(labels))
        self.play(Create(graph))
        self.play(Write(R_text))

        self.wait(2)

with tempconfig({"quality": "medium_quality", "preview": False, "pixel_width": 1520, "pixel_height": 1080 }):
    scene = kerr_BH_regions()
    scene.render()
