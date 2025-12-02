from manim import *
import numpy as np


class Lorenz3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES, zoom=1.4)

        def lorenz_step(x, y, z, s=10, r=28, b=8/3, dt=0.01):
            dx = s * (y - x)
            dy = x * (r - z) - y
            dz = x * y - b * z
            return x + dx * dt, y + dy * dt, z + dz * dt

        def generate_lorenz(T=30, dt=0.01, init=(1, 1, 1)):
            n = int(T / dt)
            x = np.zeros(n)
            y = np.zeros(n)
            z = np.zeros(n)
            x[0], y[0], z[0] = init
            for i in range(1, n):
                x[i], y[i], z[i] = lorenz_step(x[i-1], y[i-1], z[i-1], dt=dt)
            return np.stack([x, y, z], axis=1)

        traj = generate_lorenz(T=40, dt=0.01, init=(10, -10, 25))
        traj -= traj.mean(axis=0)
        traj /= np.max(np.linalg.norm(traj, axis=1)) * 1.1
        traj *= 3.0

        points = [np.array([px, py, pz]) for px, py, pz in traj]

        curve = VMobject(color=YELLOW)
        curve.set_points_smoothly(points)

        axes = ThreeDAxes(
            x_range=[-4, 4, 2],
            y_range=[-4, 4, 2],
            z_range=[-4, 4, 2],
            x_length=6,
            y_length=6,
            z_length=6,
        )
        axes.set_stroke(opacity=0.25)

        self.add(axes)
        self.play(Create(curve), run_time=4)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(25)
        self.stop_ambient_camera_rotation()
