from manim import *
import numpy as np

class zoom(Scene):
    def construct(self):
        x=ValueTracker(7)
        ax = always_redraw(lambda: Axes(x_range=(-8,8),y_range=(-1,1),x_length=x.get_value(),y_length=4,tips=False).add_coordinates())

        self.play(Write(ax))
        
        num = ValueTracker(1)
        curve = always_redraw(lambda : ax.plot(lambda x: np.sin(num.get_value()*x),color=BLUE))
        self.play(Create(curve))
        self.wait()
        self.play(x.animate.set_value(30))
        self.wait()
        self.play(num.animate.set_value(10))
        self.wait()
        self.play(x.animate.set_value(5))
        
        
        self.wait(3)
