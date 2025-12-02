from manim import * 

class demo(Scene):
    def construct(self):
        t = Text("Hello", color=DARK_BLUE, weight=BOLD, font_size=48)
        self.play(Write(t))
        self.wait(3)
        self.play(Unwrite(t))
        self.wait(1)
