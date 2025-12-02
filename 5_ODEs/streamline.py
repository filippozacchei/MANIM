from manim import *
import numpy as np

class SimpleField(Scene):
    def construct(self):
        # Define the vector field f(x, y) = (y, -x)
        def f(pos):
            x, y = pos[:2]
            return np.array([y, -x, 0.0])

        # Optional background plane
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
        )
        self.play(Create(plane))

        # Use ArrowVectorField (not VectorField) in v0.18
        field = ArrowVectorField(
            f,
            x_range=[-3, 3, 1],     # [min, max, step]
            y_range=[-3, 3, 1],
            length_func=lambda norm: 0.5 * np.tanh(norm),
        )

        self.play(Create(field), run_time=2)
        self.wait()
