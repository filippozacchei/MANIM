from manim import *
import numpy as np

class cosine(Scene):
    def construct(self):
        ax = Axes(x_range=(-8,8),y_range=(-1.5,1.5),x_length=13,y_length=3,tips=False)
        x_lab = ax.get_x_axis_label("X")
        y_lab = ax.get_y_axis_label("Y")
        self.play(Write(ax),Write(x_lab),Write(y_lab))
        
        curve = ax.plot(lambda x: np.cos(x),color=RED)
        self.play(Write(curve))
        
        self.wait(3)


