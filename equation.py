from manim import *

class Eq(Scene):
    def construct(self):
        eqn = Tex("$\Xi=$",
                  "$(V \Theta \widehat{\Xi}-\dot{V} \mathbf{U})^T$",
                  "$(V \Theta \widehat{\Xi}-\dot{V} \mathbf{U})$",
                  "$+\lambda\|\widehat{\Xi}\|_2^2\right\}$")
        self.play(Write(eqn))
        group = VGroup(eqn[1],eqn[2])
        s = SurroundingRectangle(group)
        self.play(Write(s))
        self.wait(1)
        self.play(Unwrite(s))
        eqn2 = Tex("$\Xi=$",
                  "$(V \Theta \widehat{\Xi}-\dot{V} \mathbf{U})^T$",
                  "$\Sigma^{-1}$",
                  "$(V \Theta \widehat{\Xi}-\dot{V} \mathbf{U})$",
                  "$+\lambda\|\widehat{\Xi}\|_2^2\right\}$")
        self.play(TransformMatchingTex(eqn,eqn2))
        s = SurroundingRectangle(eqn2[2],color=BLUE)
        self.play(Write(s))
        te = Text("Weight Matrix",color=BLUE).next_to(s,DOWN,buff=0.5)
        self.play(Write(te))
        self.wait(3)
        
        
        
