from manim import *
import numpy as np


class rayos_Luz_Schwarzschild(Scene):
    def construct(self):
        Schwarzschild_radius = 2
        def light_ray(x, k, sign):
            if x == 2:
                return 0  # Evita valores indefinidos
            value = x + 2 * np.log(np.abs(x - 2) + 1e-6) + k  # Evita log(0)
            return value if sign == 'plus' else -value

        self.camera.background_color = "#FFF"

        # Configuración de los ejes
        axes = Axes(
            x_range=[-0, 5],
            y_range=[-2, 2],
            axis_config={"color": BLACK, "include_ticks": False},
            tips=True,
            x_length=10,
            y_length=10
        )

        # Etiquetas de los ejes
        x_label = MathTex("r").next_to(axes.x_axis, RIGHT).set_color(BLACK)
        y_label = MathTex("ct").next_to(axes.y_axis, LEFT).set_color(BLACK)


        Schwarzschild_line = DashedVMobject(Line(
            axes.coords_to_point(2, -2),
            axes.coords_to_point(2, 2),
            color=BLACK
        ))
        # Graficar múltiples rayos_entrantes de luz
        rayos_entrantes = VGroup()
        vectors_in = VGroup()
        in_color = RED
        for k in [-2, 0, 2]:
            graph_in = VGroup(
            axes.plot(
                lambda x: light_ray(x, k, 'minus'),
                x_range=[0, 1.9999, 0.01],
                color=in_color
            ),
            axes.plot(
                lambda x: light_ray(x, k, 'minus'),
                x_range=[2.0001, 5, 0.01],
                color=in_color
            )
            )
            for x in np.arange(0, 1.9999, 0.5):
                vectors_in.add(Arrow(
                    start=axes.c2p(x + 0.01, light_ray(x + 0.01, k, 'minus'), 0),
                    end=axes.c2p(x, light_ray(x, k, 'minus'), 0),
                    buff=0,
                    color=in_color,
                    stroke_width=20,
                    max_tip_length_to_length_ratio=40
                ))
            for x in np.arange(2.0001, 5, 0.5):
                vectors_in.add(Arrow(
                    start=axes.c2p(x + 0.01, light_ray(x + 0.01, k, 'minus'), 0),
                    end=axes.c2p(x, light_ray(x, k, 'minus'), 0),
                    buff=0,
                    color=in_color,
                    stroke_width=20,
                    max_tip_length_to_length_ratio=40
                ))
            rayos_entrantes.add(graph_in)

        # Graficar múltiples rayos_salientes de luz
        rayos_salientes = VGroup()
        vectors_out = VGroup()
        out_color = BLUE
        for k in [-2, 0, 2]:
            graph_out = VGroup(
            axes.plot(
                lambda x: light_ray(x, k, 'plus'),
                x_range=[0, 1.9999, 0.01],
                color=out_color
            ),
            axes.plot(
                lambda x: light_ray(x, k, 'plus'),
                x_range=[2.0001, 5, 0.01],
                color=out_color
            )
            )
            for x in np.arange(0.15, 1.9999, 0.5):
                vectors_out.add(Arrow(
                    start=axes.c2p(x , light_ray(x, k, 'plus'), 0),
                    end=axes.c2p(x+ 0.01, light_ray(x+ 0.01, k, 'plus'), 0),
                    buff=0,
                    color=out_color,
                    stroke_width=20,
                    max_tip_length_to_length_ratio=40
                ))
            for x in np.arange(2.0001, 5, 0.5):
                vectors_out.add(Arrow(
                    start=axes.c2p(x , light_ray(x, k, 'plus'), 0),
                    end=axes.c2p(x+ 0.01, light_ray(x+ 0.01, k, 'plus'), 0),
                    buff=0,
                    color=out_color,
                    stroke_width=20,
                    max_tip_length_to_length_ratio=40
                ))
            rayos_salientes.add(graph_out)
    


        # Agregar a la escena
        self.add(axes, x_label, y_label, rayos_entrantes, vectors_in, rayos_salientes, vectors_out,Schwarzschild_line)
 

class Kruskal_Szekeres_diagram(Scene):
    def construct(self):
        self.camera.background_color = "#FFF"
        plane = NumberPlane(
            x_range=(-2, 2),
            y_range=(-2, 2),
            background_line_style={
                "stroke_color": WHITE,
                "stroke_width": 0,
                "stroke_opacity": 0.6
            },
            axis_config={"color": WHITE},
        )
        # Configuración de los ejes
        #Ecuacion de la singularidad
        singularity = plane.plot_implicit_curve(lambda x, y: y**2 - x**2 - 1 , color=BLACK,stroke_width = 3)

       
        #Lineas de r constante
        r_group = VGroup()
        #interior
        for r in np.arange(0, 0.95, 0.07):
            r_const = plane.plot_implicit_curve(lambda x,y: y**2 - x**2 + np.exp(r)*(r-1),
                color=RED,
                stroke_width=1
            )
            r_group.add(r_const)
        #exterior
        for r in np.arange(1.2, 5, 0.1):
            r_const = plane.plot_implicit_curve(
                lambda x,y: y**2 - x**2 + np.exp(r)*(r-1),
                color=RED,
                stroke_width = 1
            )
            r_group.add(r_const)
        


        #Horizonte de Schwarzschild
        horizon = plane.plot_implicit_curve(lambda x, y: y**2 - x**2 , color=BLACK,)
        horizon = DashedVMobject(horizon,num_dashes=100)
        

        plane = NumberPlane(
            x_range=(-2, 2),
            y_range=(-2, 2),
            background_line_style={
                "stroke_color": WHITE,
                "stroke_width": 0,
                "stroke_opacity": 0.6
            },
            axis_config={"color":WHITE},
        )
        #Lineas de t constante
        t_const_group = VGroup()
        for t in np.arange(-20, 20, 0.3):
            #Izquierda y derecha
            t_const = plane.plot_implicit_curve(
            lambda x,y: y - x*np.tanh(t/2),
            color=BLACK,
            stroke_width = 1,
            )
            t_const_group.add(t_const)
           # Top & bottom curves (red)
            y_max = np.sqrt(1/(1-np.tanh(t/2)**2))
            t_const = plane.plot_implicit_curve(
                lambda x, y: np.where(y <= y_max and y>= - y_max, x - y * np.tanh(t / 2), np.nan),
                color=RED,
                stroke_width=1,
            )
            t_const_group.add(t_const)

            
        Kruskal_diag = VGroup( plane, singularity, r_group, horizon, t_const_group,)
       
        self.add(Kruskal_diag)
        directions = Axes(
            x_range=[0, 1],
            y_range=[0, 1],
            axis_config={"color": BLACK},
            tips=True,
            x_length=2,
            y_length=2
        )
        x_label = MathTex("U").next_to(directions.x_axis, RIGHT).set_color(BLACK)
        y_label = MathTex("V").next_to(directions.y_axis, UP).set_color(BLACK)
        directions.shift(3*LEFT + 2*DOWN)
        self.add(directions, x_label, y_label)

        
class kerr_BH_regions(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#FFF"
        axes = ThreeDAxes(
            axis_config={"color": BLACK}
        )
        sphere = Surface(
            lambda u, v: np.array([
                1.5 * np.cos(u) * np.cos(v),
                1.5 * np.cos(u) * np.sin(v),
                1.5 * np.sin(u)
            ]), v_range=[(1/4)*TAU, TAU], u_range=[-PI / 2, PI / 2],
            checkerboard_colors=[RED_D, RED_E], resolution=(60, 60)
        )
        #euler 
        curve1 = ParametricFunction(
            lambda u: (
                1.6 * np.cos(u),
                1.6 * np.sin(u),
                0
            ), color=BLUE, t_range = (-3*TAU, 5*TAU, 0.01)
        ).set_shade_in_3d(True)
        
        self.renderer.camera.light_source.move_to(4*IN) # changes the source of the light
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES,zoom=1.6)
        self.add(axes, sphere,curve1)        



with tempconfig({"quality": "medium_quality", "preview": False, "pixel_width": 1920, "pixel_height": 1080 }):
    scene = kerr_BH_regions()
    scene.render()
