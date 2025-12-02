from manim import *
import numpy as np


class ExponentialDecay(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.2, 0.2],
            x_length=6,
            y_length=3,
            tips=False,
        )
        labels = VGroup(
            ax.get_x_axis_label(MathTex("t")),
            ax.get_y_axis_label(MathTex("u(t)")),
        )
        self.play(Create(ax), Write(labels))

        lam = 1.0
        u0 = 1.0

        def u(t):
            return u0 * np.exp(-lam * t)

        t_vals = np.linspace(0, 5, 201)
        u_vals = u(t_vals)

        curve = ax.plot(lambda t: u(t), x_range=[0, 5], color=YELLOW)
        self.play(Create(curve), run_time=2)

        # Discrete points along the solution
        dots = VGroup(
            *[
                Dot(ax.coords_to_point(t, u(t)), radius=0.03, color=BLUE)
                for t in np.linspace(0, 5, 20)
            ]
        )
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.05))
        self.wait()
