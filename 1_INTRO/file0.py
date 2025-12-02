from manim import * 

class demo(Scene):
    def construct(self):
        t = Text("Hello")
        self.play(Write(t), run_time=1)     
        self.wait(1)      
        self.play(Unwrite(t))
        self.wait(3) 
