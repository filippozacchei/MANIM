from manim import *
import numpy as np

class parabula(Scene):
    def construct(self):
        
        ax = Axes(x_range=(-4,4),y_range=(0,16),x_length=4,y_length=6,tips=False)
        # ax = Axes(x_range=(-4,4),y_range=(0,16),x_length=4,y_length=6,tips=False)
        x_lab = ax.get_x_axis_label("X")
        y_lab = ax.get_y_axis_label("Y")
        
        self.play(Write(ax),Write(x_lab),Write(y_lab))
        
        number= ValueTracker(1)
        
        # always_redraw needs a *function* that returns a Mobject
        curve = always_redraw(
            lambda: ax.plot(
                lambda x: number.get_value() * x**2,
            )
        )
        
        self.play(Create(curve))
        self.play(number.animate.set_value(2),run_time=2)
        self.play(number.animate.set_value(0.1),run_time=2)
        self.play(number.animate.set_value(0.5),run_time=2)
        
        self.wait(3)
