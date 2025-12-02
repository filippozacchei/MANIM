from manim import * 

class demo(Scene):
    def construct(self):
        # self.add(NumberPlane())
        t = Text("Hello", color="#922221",weight=BOLD,font_size=90)
        # t = Text("Hello", color=DARK_BLUE, weight=BOLD, font_size=90)

        
        
        s = Square(side_length=3,fill_opacity=0.7,color=BLUE)
        
        self.play(Write(t))
        self.wait(3)
        self.play(Transform(t,s),run_time=5)
        
        self.play(Unwrite(t))
        self.wait(1)
