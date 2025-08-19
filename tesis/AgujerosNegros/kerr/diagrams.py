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

