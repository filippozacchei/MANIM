from manim import *

class demo(Scene):
    def construct(self):
        # # CONSTRUCT Circle
        s = Circle(radius=0.5, stroke_width=10, color=RED, fill_opacity=0.3)
        # Constrcut Rectangle
        r = SurroundingRectangle(s,color=BLUE,corner_radius=0.1)
        self.play(Write(s),Write(r))
        
        # # To Make stuff more Spicy
        # self.play(Write(s),DrawBorderThenFill(r))
        
        # # Add text
        # t = Text("Manim").next_to(r,UP,buff=0.5) # next to set the position to a object and whcih side. Buffer adjust space
        
        # self.play(Write(t))
        
        # # ANIMATIONS
        # np = NumberPlane()
        # self.play(Write(np))
        # # I want to move objects
        # x = 4
        # y = 0
        # z = 0
        # # self.play(t.animate.move_to([x,y,z]))
        
        # # COMBINE OBjects in one
        # sr = VGroup(s,r)
        # # x = 4
        # # y = 0
        # # z = 0
        # # self.play(sr.animate.move_to([x,y,z]))
        
        # # to do together
        # self.play(t.animate.move_to([-x,y,z]),
        #           sr.animate.move_to([x,y,z]))
        
        
        # # Now add the arrow 
        # # arrow = Line(buff=0.4, 
        # #              start=sr.get_left(),
        # #              end=t.get_right()).add_tip(tip_shape=StealthTip).add_tip(tip_shape=StealthTip,at_start=True)
        # arrow = always_redraw(lambda: Line(buff=0.4, 
        #              start=sr.get_left(),
        #              end=t.get_right()).add_tip(tip_shape=StealthTip).add_tip(tip_shape=StealthTip,at_start=True))
       
        # self.play(Write(arrow))
        
        # self.play(FadeOut(np))
        
        # # Animate Text
        # self.play(Indicate(t, 1.5, color=ORANGE))
        
        # # Animate Shapes
        # self.play(ScaleInPlace(s,2),Rotate(r, angle=PI/2))
        
        # # But UPDATE ARROW: UPDATER
        
        # # MOVE TO CENTER
        # self.play(sr.animate.move_to([0,0,0]))
        
        # # FadeOUt
        # self.play(FadeOut(arrow),FadeOut(t), run_time=0.25)
        
        # # SCALE
        # self.play(ShrinkToCenter(r), ScaleInPlace(s, 30))
        
        # # Fade Circle
        # self.play(FadeOut(s))
        
        # # wait a bit
        # self.wait() # 1 second by default

# class demo2(Scene):
#     def construct(self):
#         t = Tex("Hello ", "there ", "dog")
#         t[0].color = RED
#         t[1].color = YELLOW
#         t[2].color = GREEN
#         self.play(Write(t))
        
#         self.play(t[0].animate.to_edge(DR,buff=1),
#                   t[1].animate.to_edge(UR,buff=1),
#                   t[2].animate.move_to([0,2,0]))
        
#         self.wait(3)
    