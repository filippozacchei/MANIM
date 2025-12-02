from manim import * 

class demo(Scene):
    def construct(self):
        t = Text("Hello")
        self.play(Write(t))
            
