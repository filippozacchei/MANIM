from manim import *

class axes(Scene):
    def construct(self):
        
        # Generate Axes
        axes = Axes(x_range=(-20,20),y_range=(-15,15))
        
        self.play(Write(Axes))
        
        # put stuff in the axes
        
        tri = Triangle().scale(0.3)
        tri.move_to(axes.c2p(-7,10))
        self.play(Write(tri))
        
        dot = Dot(color=RED)
        self.play(Create(Dot))
        self.play(Dot.animate.move_to(7,-10))
        
        
        self.wait(3)
