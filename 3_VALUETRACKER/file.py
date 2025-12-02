from manim import *

class valuetracker(Scene):
    def construct(self):
        t1 = ValueTracker(999)
        number = always_redraw(lambda : DecimalNumber(t1.get_value()))
                               
        self.play(Write(number))    
        self.play(t1.animate.set_value(30),run_time=5)       
        
        self.play(Wait(3))        
