from manim import *
import numpy as np


class rayos_Luz_Schwarzschild(Scene):
    def construct(self):
        # Constants
        Schwarzschild_radius = 2
        epsilon = 0.001
        min_y = -2.8
        max_y = 3
        x_extension = 5

        # Light ray function
        def light_ray(x, k, sign):
            if x == Schwarzschild_radius:
                return 0
            val = x + Schwarzschild_radius * np.log(np.abs(x - Schwarzschild_radius) + 1e-6) + k
            return val if sign == 'plus' else -val

        # Background
        self.camera.background_color = WHITE

        # Axes
        axes = Axes(
            x_range=[0, x_extension+0.5],
            y_range=[min_y -0.3, max_y+0.3],
            x_length=8.5,
            y_length=6.5,
            axis_config={"color": GRAY, "stroke_width": 1.5,
            "include_ticks": False},
            tips=True,
        )
        axes.to_edge(DOWN, buff=1).shift(DOWN*0.3).scale(1.3)

        # Axis labels
        x_label = MathTex("r", color=BLACK).next_to(axes.x_axis, RIGHT, buff=0.3)
        y_label = MathTex("ct", color=BLACK).next_to(axes.y_axis, UP, buff=0.3)

        # Schwarzschild radius line
        rs_line = DashedLine(
            axes.c2p(Schwarzschild_radius, min_y),
            axes.c2p(Schwarzschild_radius, max_y),
            color=BLACK,
            stroke_width=2
        )
        rs_label = MathTex("r_s", color=BLACK, font_size=30).next_to(rs_line, UP, buff=0.2)

        # === Filtered light ray curves ===
        def make_filtered_curve(k, sign, color):
            curve = VMobject(color=color, stroke_width=2.5)
            points = []
            arrows = VGroup()

            # Left side of r_s
            for x in np.arange(0.03, Schwarzschild_radius - epsilon, 0.01):
                y = light_ray(x, k, sign)
                if min_y <= y <= max_y:   
                    points.append(axes.c2p(x, y))
                 
            if points:
                curve.set_points_smoothly(points)
            
          
            for x in np.arange(0.2, Schwarzschild_radius - epsilon, 0.6):
                y = light_ray(x, k, sign)
                dy =  light_ray(x+0.005, k, sign)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x+0.005,dy ),
                                end=axes.c2p(x,y),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =15,
                                max_tip_length_to_length_ratio= 15,
                            ))

            # Right side
            right_curve = VMobject(color=color, stroke_width=2.5)
            points_right = []
            
            for x in np.arange(Schwarzschild_radius + epsilon, x_extension, 0.01):
                y = light_ray(x, k, sign)
                if min_y <= y <= max_y:
                    points_right.append(axes.c2p(x, y))
                        
            if points_right:
                right_curve.set_points_smoothly(points_right)
            
            for x in np.arange(Schwarzschild_radius + epsilon,x_extension, 0.6):
                y = light_ray(x, k, sign)
                dy =  light_ray(x+0.001, k, sign)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x,y ) if sign == 'plus' else axes.c2p(x+0.001,dy),
                                end=axes.c2p(x+0.001,dy)if sign == 'plus' else axes.c2p(x,y ),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =45,
                                max_tip_length_to_length_ratio= 45,
                            ))

            

            return VGroup(curve, right_curve,arrows)

        # Light rays
        rayos_entrantes = VGroup(*[
            make_filtered_curve(k, 'minus', RED_D) for k in [-6.5, -5, -3.5, -2, 0, 2]
        ])


        rayos_salientes = VGroup(*[
            make_filtered_curve(k, 'plus', BLUE_D) for k in [-6.3, -4.8, -3.3, -1.8, 0,1.8]
        ])

        # === Group all and add ===
        self.add(axes, x_label, y_label)
        self.add(rs_line, rs_label)
        self.add(rayos_entrantes, rayos_salientes)

class EddingtonFinkelsteinIngoingLight(Scene):
   def construct(self):
        # Constants
        Schwarzschild_radius = 2
        epsilon = 0.001
        min_y = -2.8
        max_y = 3
        x_extension = 5

        # Light ray function
        def light_ray(x, k, sign):
            if x == Schwarzschild_radius:
                return 0
            val = x + 2*Schwarzschild_radius * np.log(np.abs(x - Schwarzschild_radius) + 1e-6) + k
            return val if sign == 'plus' else -val
        
        def light_ray_in(x, k):
            return -x + k

        # Background
        self.camera.background_color = WHITE

        # Axes
        axes = Axes(
            x_range=[0, x_extension+0.5],
            y_range=[min_y -0.3, max_y+0.3],
            x_length=8.5,
            y_length=6.5,
            axis_config={"color": GRAY, "stroke_width": 1.5,
            "include_ticks": False},
            tips=True,
        )
        axes.to_edge(DOWN, buff=1).shift(DOWN*0.3).scale(1.3)

        # Axis labels
        x_label = MathTex("r", color=BLACK).next_to(axes.x_axis, RIGHT, buff=0.3)
        y_label = MathTex(r'c {\tilde{t}} ', color=BLACK).next_to(axes.y_axis, UP, buff=0.3)

        # Schwarzschild radius line
        rs_line = DashedLine(
            axes.c2p(Schwarzschild_radius, min_y),
            axes.c2p(Schwarzschild_radius, max_y),
            color=BLACK,
            stroke_width=2
        )
        rs_label = MathTex("r_s", color=BLACK, font_size=30).next_to(rs_line, UP, buff=0.2)

        # === Filtered light ray curves ===
        def make_filtered_curve(k, sign, color):
            curve = VMobject(color=color, stroke_width=2.5)
            points = []
            arrows = VGroup()

            # Left side of r_s
            for x in np.arange(0.03, Schwarzschild_radius - epsilon, 0.01):
                y = light_ray(x, k, sign)
                if min_y <= y <= max_y:   
                    points.append(axes.c2p(x, y))
                 
            if points:
                curve.set_points_smoothly(points)
            
          
            for x in np.arange(0.2, Schwarzschild_radius - epsilon, 0.6):
                y = light_ray(x, k, sign)
                dy =  light_ray(x+0.005, k, sign)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x+0.005,dy ),
                                end=axes.c2p(x,y),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =15,
                                max_tip_length_to_length_ratio= 15,
                            ))

            # Right side
            right_curve = VMobject(color=color, stroke_width=2.5)
            points_right = []
            
            for x in np.arange(Schwarzschild_radius + epsilon, x_extension, 0.01):
                y = light_ray(x, k, sign)
                if min_y <= y <= max_y:
                    points_right.append(axes.c2p(x, y))
                        
            if points_right:
                right_curve.set_points_smoothly(points_right)
            
            for x in np.arange(Schwarzschild_radius + epsilon,x_extension, 0.6):
                y = light_ray(x, k, sign)
                dy =  light_ray(x+0.001, k, sign)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x,y ) if sign == 'plus' else axes.c2p(x+0.001,dy),
                                end=axes.c2p(x+0.001,dy)if sign == 'plus' else axes.c2p(x,y ),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =45,
                                max_tip_length_to_length_ratio= 45,
                            ))

            

            return VGroup(curve, right_curve,arrows)


        # incoming light rays
        def make_incoming_curve(k, color):
            curve = VMobject(color=color, stroke_width=2.5)
            points = []
            arrows = VGroup()
            for x in np.arange(0.3, x_extension, 0.01):
                y = light_ray_in(x, k)
                if min_y <= y <= max_y:   
                    points.append(axes.c2p(x, y))
            if points:
                curve.set_points_smoothly(points)
            for x in np.arange(0.2, x_extension, 0.6):
                y = light_ray_in(x, k)
                dy =  light_ray_in(x+0.005, k)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x+0.005,dy ),
                                end=axes.c2p(x,y),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =45,
                                max_tip_length_to_length_ratio= 45,
                            ))
            return VGroup(curve,arrows)
        rayos_entrantes = VGroup(*[
            make_incoming_curve(k, RED_D) for k in np.arange(-6.5, 6.8, 1.5)
        ])

        rayos_salientes = VGroup(*[
            make_filtered_curve(k, 'plus', BLUE_D) for k in [-6.3, -4.8, -3.3, -1.8, 0,1.8, ]
        ])

        # === Group all and add ===
        self.add(axes, x_label, y_label)
        self.add(rs_line, rs_label)
        self.add(rayos_salientes, rayos_entrantes)

class EddingtonFinkelsteinOutgoingLight(Scene):
   def construct(self):
        # Constants
        Schwarzschild_radius = 2
        epsilon = 0.001
        min_y = -2.8
        max_y = 3
        x_extension = 5

        # Light ray function
        def light_ray(x, k, sign):
            if x == Schwarzschild_radius:
                return 0
            val = x + 2*Schwarzschild_radius * np.log(np.abs(x - Schwarzschild_radius) + 1e-6) + k
            return val if sign == 'plus' else -val
        
        def light_ray_out(x, k):
            return x + k

        # Background
        self.camera.background_color = WHITE

        # Axes
        axes = Axes(
            x_range=[0, x_extension+0.5],
            y_range=[min_y -0.3, max_y+0.3],
            x_length=8.5,
            y_length=6.5,
            axis_config={"color": GRAY, "stroke_width": 1.5,
            "include_ticks": False},
            tips=True,
        )
        axes.to_edge(DOWN, buff=1).shift(DOWN*0.3).scale(1.3)

        # Axis labels
        x_label = MathTex("r", color=BLACK).next_to(axes.x_axis, RIGHT, buff=0.3)
        y_label = MathTex(r'c {\tilde{t}} ', color=BLACK).next_to(axes.y_axis, UP, buff=0.3)

        # Schwarzschild radius line
        rs_line = DashedLine(
            axes.c2p(Schwarzschild_radius, min_y),
            axes.c2p(Schwarzschild_radius, max_y),
            color=BLACK,
            stroke_width=2
        )
        rs_label = MathTex("r_s", color=BLACK, font_size=30).next_to(rs_line, UP, buff=0.2)

        # === Filtered light ray curves ===
        def make_filtered_curve(k, sign, color):
            curve = VMobject(color=color, stroke_width=2.5)
            points = []
            arrows = VGroup()

            # Left side of r_s
            for x in np.arange(0.03, Schwarzschild_radius - epsilon, 0.01):
                y = light_ray(x, k, sign)
                if min_y <= y <= max_y:   
                    points.append(axes.c2p(x, y))
                 
            if points:
                curve.set_points_smoothly(points)
            
          
            for x in np.arange(0.2, Schwarzschild_radius - epsilon, 0.6):
                y = light_ray(x, k, sign)
                dy =  light_ray(x+0.005, k, sign)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x+0.005,dy ),
                                end=axes.c2p(x,y),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =15,
                                max_tip_length_to_length_ratio= 15,
                            ))

            # Right side
            right_curve = VMobject(color=color, stroke_width=2.5)
            points_right = []
            
            for x in np.arange(Schwarzschild_radius + epsilon, x_extension, 0.01):
                y = light_ray(x, k, sign)
                if min_y <= y <= max_y:
                    points_right.append(axes.c2p(x, y))
                        
            if points_right:
                right_curve.set_points_smoothly(points_right)
            
            for x in np.arange(Schwarzschild_radius + epsilon,x_extension, 0.6):
                y = light_ray(x, k, sign)
                dy =  light_ray(x+0.001, k, sign)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x,y ) if sign == 'plus' else axes.c2p(x+0.001,dy),
                                end=axes.c2p(x+0.001,dy)if sign == 'plus' else axes.c2p(x,y ),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =45,
                                max_tip_length_to_length_ratio= 45,
                            ))

            

            return VGroup(curve, right_curve,arrows)


        # incoming light rays
        def make_incoming_curve(k, color):
            curve = VMobject(color=color, stroke_width=2.5)
            points = []
            arrows = VGroup()
            for x in np.arange(0, x_extension, 0.01):
                y = light_ray_out(x, k)
                if min_y <= y <= max_y:   
                    points.append(axes.c2p(x, y))
            if points:
                curve.set_points_smoothly(points)
            for x in np.arange(0.2, x_extension, 0.6):
                y = light_ray_out(x, k)
                dy =  light_ray_out(x+0.005, k)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x,y),
                                end=axes.c2p(x+0.005,dy ),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =45,
                                max_tip_length_to_length_ratio= 45,
                            ))
            return VGroup(curve,arrows)
        rayos_entrantes = VGroup(*[
            make_incoming_curve(k, BLUE_D) for k in np.arange(-6.5, 6.8, 1.5)
        ])

        rayos_salientes = VGroup(*[
            make_filtered_curve(k, 'minus', RED_D) for k in [-6.3, -4.8, -3.3, -1.8, 0,1.8, ]
        ])

        # === Group all and add ===
        self.add(axes, x_label, y_label)
        self.add(rs_line, rs_label)
        self.add(rayos_salientes, rayos_entrantes)


class EddingtonFinkelsteinVR(Scene):
   def construct(self):
        # Constants
        Schwarzschild_radius = 2
        epsilon = 0.001
        min_y = -2.8
        max_y = 3
        x_extension = 5

        # Light ray function
        def light_ray(x, k, sign):
            if x == Schwarzschild_radius:
                return 0
            val =  2*(x + Schwarzschild_radius * np.log(np.abs(x - Schwarzschild_radius) )) + k
            return val if sign == 'plus' else -val
        
        def light_ray_in(x, k):
            return  k

        # Background
        self.camera.background_color = WHITE

        # Axes
        axes = Axes(
            x_range=[0, x_extension+0.5],
            y_range=[min_y -0.3, max_y+0.3],
            x_length=8.5,
            y_length=6.5,
            axis_config={"color": GRAY, "stroke_width": 1.5,
            "include_ticks": False},
            tips=True,
        )
        axes.to_edge(DOWN, buff=1).shift(DOWN*0.3).scale(1.3)

        # Axis labels
        x_label = MathTex("r_{in}", color=BLACK).next_to(axes.x_axis, RIGHT, buff=0.3)
        y_label = MathTex(r'v', color=BLACK).next_to(axes.y_axis, UP, buff=0.3)

        # Schwarzschild radius line
        rs_line = DashedLine(
            axes.c2p(Schwarzschild_radius, min_y),
            axes.c2p(Schwarzschild_radius, max_y),
            color=BLACK,
            stroke_width=2
        )
        rs_label = MathTex("r_s", color=BLACK, font_size=30).next_to(rs_line, UP, buff=0.2)

        # === Filtered light ray curves ===
        def make_filtered_curve(k, sign, color):
            curve = VMobject(color=color, stroke_width=2.5)
            points = []
            arrows = VGroup()

            # Left side of r_s
            for x in np.arange(0.03, Schwarzschild_radius - epsilon, 0.01):
                y = light_ray(x, k, sign)
                if min_y <= y <= max_y:   
                    points.append(axes.c2p(x, y))
                 
            if points:
                curve.set_points_smoothly(points)
            
          
            for x in np.arange(0.2, Schwarzschild_radius - epsilon, 0.6):
                y = light_ray(x, k, sign)
                dy =  light_ray(x+0.005, k, sign)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x+0.005,dy ),
                                end=axes.c2p(x,y),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =15,
                                max_tip_length_to_length_ratio= 15,
                            ))

            # Right side
            right_curve = VMobject(color=color, stroke_width=2.5)
            points_right = []
            
            for x in np.arange(Schwarzschild_radius + epsilon, x_extension, 0.01):
                y = light_ray(x, k, sign)
                if min_y <= y <= max_y:
                    points_right.append(axes.c2p(x, y))
                        
            if points_right:
                right_curve.set_points_smoothly(points_right)
            
            for x in np.arange(Schwarzschild_radius + epsilon,x_extension, 0.6):
                y = light_ray(x, k, sign)
                dy =  light_ray(x+0.001, k, sign)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x,y ) if sign == 'plus' else axes.c2p(x+0.001,dy),
                                end=axes.c2p(x+0.001,dy)if sign == 'plus' else axes.c2p(x,y ),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =45,
                                max_tip_length_to_length_ratio= 45,
                            ))

            

            return VGroup(curve, right_curve,arrows)


        # incoming light rays
        def make_incoming_curve(k, color):
            curve = VMobject(color=color, stroke_width=2.5)
            points = []
            arrows = VGroup()
            for x in np.arange(0.3, x_extension, 0.01):
                y = light_ray_in(x, k)
                if min_y <= y <= max_y:   
                    points.append(axes.c2p(x, y))
            if points:
                curve.set_points_smoothly(points)
            for x in np.arange(0.2, x_extension, 0.6):
                y = light_ray_in(x, k)
                dy =  light_ray_in(x+0.005, k)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x+0.005,dy ),
                                end=axes.c2p(x,y),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =45,
                                max_tip_length_to_length_ratio= 45,
                            ))
            return VGroup(curve,arrows)
        rayos_entrantes = VGroup(*[
            make_incoming_curve(k, RED_D) for k in np.arange(-6.5, 6.8, 1.5)
        ])

        rayos_salientes = VGroup(*[
            make_filtered_curve(k, 'plus', BLUE_D) for k in [-6.3, -4.8, -3.3, -1.8, 0,1.8, ]
        ])

        # === Group all and add ===
        self.add(axes, x_label, y_label)
        self.add(rs_line, rs_label)
        self.add(rayos_salientes, rayos_entrantes)



class EddingtonFinkelsteinUR(Scene):
   def construct(self):
        # Constants
        Schwarzschild_radius = 2
        epsilon = 0.001
        min_y = -2.8
        max_y = 3
        x_extension = 5

        # Light ray function
        def light_ray(x, k, sign):
            if x == Schwarzschild_radius:
                return 0
            val = 2*(x + Schwarzschild_radius * np.log(np.abs(x - Schwarzschild_radius) )) + k
            return val if sign == 'plus' else -val
        
        def light_ray_out(x, k):
            return  k

        # Background
        self.camera.background_color = WHITE

        # Axes
        axes = Axes(
            x_range=[0, x_extension+0.5],
            y_range=[min_y -0.3, max_y+0.3],
            x_length=8.5,
            y_length=6.5,
            axis_config={"color": GRAY, "stroke_width": 1.5,
            "include_ticks": False},
            tips=True,
        )
        axes.to_edge(DOWN, buff=1).shift(DOWN*0.3).scale(1.3)

        # Axis labels
        x_label = MathTex("r_{out}", color=BLACK).next_to(axes.x_axis, RIGHT, buff=0.3)
        y_label = MathTex(r'u', color=BLACK).next_to(axes.y_axis, UP, buff=0.3)

        # Schwarzschild radius line
        rs_line = DashedLine(
            axes.c2p(Schwarzschild_radius, min_y),
            axes.c2p(Schwarzschild_radius, max_y),
            color=BLACK,
            stroke_width=2
        )
        rs_label = MathTex("r_s", color=BLACK, font_size=30).next_to(rs_line, UP, buff=0.2)

        # === Filtered light ray curves ===
        def make_filtered_curve(k, sign, color):
            curve = VMobject(color=color, stroke_width=2.5)
            points = []
            arrows = VGroup()

            # Left side of r_s
            for x in np.arange(0.03, Schwarzschild_radius - epsilon, 0.01):
                y = light_ray(x, k, sign)
                if min_y <= y <= max_y:   
                    points.append(axes.c2p(x, y))
                 
            if points:
                curve.set_points_smoothly(points)
            
          
            for x in np.arange(0.2, Schwarzschild_radius - epsilon, 0.6):
                y = light_ray(x, k, sign)
                dy =  light_ray(x+0.005, k, sign)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x+0.005,dy ),
                                end=axes.c2p(x,y),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =15,
                                max_tip_length_to_length_ratio= 15,
                            ))

            # Right side
            right_curve = VMobject(color=color, stroke_width=2.5)
            points_right = []
            
            for x in np.arange(Schwarzschild_radius + epsilon, x_extension, 0.01):
                y = light_ray(x, k, sign)
                if min_y <= y <= max_y:
                    points_right.append(axes.c2p(x, y))
                        
            if points_right:
                right_curve.set_points_smoothly(points_right)
            
            for x in np.arange(Schwarzschild_radius + epsilon,x_extension, 0.6):
                y = light_ray(x, k, sign)
                dy =  light_ray(x+0.001, k, sign)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x,y ) if sign == 'plus' else axes.c2p(x+0.001,dy),
                                end=axes.c2p(x+0.001,dy)if sign == 'plus' else axes.c2p(x,y ),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =45,
                                max_tip_length_to_length_ratio= 45,
                            ))

            

            return VGroup(curve, right_curve,arrows)


        # incoming light rays
        def make_incoming_curve(k, color):
            curve = VMobject(color=color, stroke_width=2.5)
            points = []
            arrows = VGroup()
            for x in np.arange(0, x_extension, 0.01):
                y = light_ray_out(x, k)
                if min_y <= y <= max_y:   
                    points.append(axes.c2p(x, y))
            if points:
                curve.set_points_smoothly(points)
            for x in np.arange(0.2, x_extension, 0.6):
                y = light_ray_out(x, k)
                dy =  light_ray_out(x+0.005, k)
                if min_y <= y <= max_y:  
                    arrows.add(Arrow(
                                start= axes.c2p(x,y),
                                end=axes.c2p(x+0.005,dy ),
                                buff=0,
                                color=color,
                                stroke_width=20,
                                max_stroke_width_to_length_ratio =45,
                                max_tip_length_to_length_ratio= 45,
                            ))
            return VGroup(curve,arrows)
        rayos_entrantes = VGroup(*[
            make_incoming_curve(k, BLUE_D) for k in np.arange(-6.5, 6.8, 1.5)
        ])

        rayos_salientes = VGroup(*[
            make_filtered_curve(k, 'minus', RED_D) for k in [-6.3, -4.8, -3.3, -1.8, 0,1.8, ]
        ])

        # === Group all and add ===
        self.add(axes, x_label, y_label)
        self.add(rs_line, rs_label)
        self.add(rayos_salientes, rayos_entrantes)




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
            x_length=6,
            y_length=6
        )
        # Configuración de los ejes
        #Ecuacion de la singularidad
        singularity = plane.plot_implicit_curve(lambda x, y: y**2 - x**2 - 1 , color=BLACK,stroke_width = 5)
        singularity = DashedVMobject(singularity,num_dashes=100)
       
        #Lineas de r constante
        r_group = VGroup()
        #interior
        for r in np.arange(0.2, 0.98, 0.07):
            r_const = plane.plot_implicit_curve(lambda x,y: y**2 - x**2 + np.exp(r)*(r-1),
                color=RED,
                stroke_width=1
            )
            r_group.add(r_const)
        #exterior
        for r in np.arange(1.05, 5, 0.1):
            r_const = plane.plot_implicit_curve(
                lambda x,y: y**2 - x**2 + np.exp(r)*(r-1),
                color=RED,
                stroke_width = 1
            )
            r_group.add(r_const)
        


        #Horizonte de Schwarzschild
        horizon = plane.plot_implicit_curve(lambda x, y: y**2 - x**2 , color=BLACK,stroke_width = 5 )
        horizon = DashedVMobject(horizon,num_dashes=100)
        

        #Lineas de t constante
        t_const_group = VGroup()
        for t in np.arange(-4.3, 4.3, 0.3):
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
                color=BLUE,
                stroke_width=1,
            )
            t_const_group.add(t_const)

            
        Kruskal_diag = VGroup( plane, singularity, r_group, horizon, t_const_group,).scale(1.6)
       
        self.add(Kruskal_diag)
        directions = Axes(
            x_range=[0, 1],
            y_range=[0, 1],
            axis_config={"color": BLACK},
            tips=True,
            x_length=2,
            y_length=2
        )
        x_label = MathTex("U").next_to(directions.x_axis, RIGHT).set_color(BLACK).shift(2.3*DOWN).shift(3.2*LEFT)
        y_label = MathTex("V").next_to(directions.y_axis, UP).set_color(BLACK).shift(3*LEFT).shift(2.1*DOWN)
        directions.shift(3*LEFT + 2*DOWN)

        reference = VGroup(directions, x_label, y_label).scale(0.7).shift(DOWN).shift(LEFT)
        self.add(reference)

        


with tempconfig({"quality": "medium_quality", "preview": False, "pixel_width": 1520, "pixel_height": 1080 }):
    scene = LightCone2D()
    scene.render()
