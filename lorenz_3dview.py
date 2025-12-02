from manim import *
import numpy as np


class LorenzTrajectories3D(ThreeDScene):
    def construct(self):
        # --------------------------------------------------------------
        # GLOBAL STYLE
        # --------------------------------------------------------------
        self.camera.background_color = "#000000"
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES, zoom=1.2)

        # Colors (one per trajectory) and noise levels
        colors = ["#8d4af9", "#4ebff7", "#ffc078"]
        noise_levels = [0.0, 0.1, 0.5]
        seeds = [8676, 8089, 435451]
        inits = [(10, -10, 31), (-10.5, 22, 41.3), (0.5, 0.8, 21.5)]

        # --------------------------------------------------------------
        # LORENZ SYSTEM + TRAJECTORY GENERATION
        # --------------------------------------------------------------
        def lorenz_step(x, y, z, s=10, r=28, b=8 / 3, dt=0.001):
            dx = s * (y - x)
            dy = x * (r - z) - y
            dz = x * y - b * z
            return x + dx * dt, y + dy * dt, z + dz * dt

        def generate_trajectory(T=30, dt=0.0005, noise=0.0, seed=0, init=(1, 1, 1)):
            np.random.seed(seed)
            n = int(T / dt)
            x = np.zeros(n)
            y = np.zeros(n)
            z = np.zeros(n)
            x[0], y[0], z[0] = init
            for i in range(1, n):
                x[i], y[i], z[i] = lorenz_step(x[i - 1], y[i - 1], z[i - 1], dt=dt)

            if noise > 0:
                x += np.random.normal(0, noise, n)
                y += np.random.normal(0, noise, n)
                z += np.random.normal(0, noise, n)

            return np.stack([x, y, z], axis=1)  # (N, 3)

        # --------------------------------------------------------------
        # COORDINATE NORMALISATION TO 3D SCENE
        # --------------------------------------------------------------
        base_traj = generate_trajectory(T=50, noise=0.0, seed=1)
        xyz = base_traj.copy()
        xyz -= xyz.mean(axis=0)
        xyz /= np.max(np.linalg.norm(xyz, axis=1)) * 1.1
        scale_factor = 3.5

        def to_points_3d(traj):
            pts = traj.copy()
            pts -= pts.mean(axis=0)
            pts /= np.max(np.linalg.norm(pts, axis=1)) * 1.1
            pts *= scale_factor
            # Optional anisotropic scaling for aesthetics
            pts[:, 0] *= 1.5  # x
            pts[:, 1] *= 1.0  # y
            pts[:, 2] *= 0.8  # z
            return [np.array([px, py, pz]) for px, py, pz in pts]

        # --------------------------------------------------------------
        # BACKGROUND ATTRACTOR (FAINT 3D CURVE)
        # --------------------------------------------------------------
        base_points_3d = to_points_3d(base_traj[::10])
        base_line = VMobject(color=GRAY_D, stroke_opacity=0.25)
        base_line.set_points_smoothly(base_points_3d)
        self.add(base_line)

        # Optionally add faint axes (no tick labels to keep it clean)
        axes = ThreeDAxes(
            x_range=(-4, 4, 2),
            y_range=(-4, 4, 2),
            z_range=(-4, 4, 2),
            x_length=6,
            y_length=6,
            z_length=6,
        )
        axes.set_stroke(opacity=0.25)
        self.add(axes)

        # --------------------------------------------------------------
        # MOVING 3D TRAJECTORIES WITH FADING TAILS
        # --------------------------------------------------------------
        TAIL_LENGTH = 120       # number of points in trail
        STEP_SUBSAMPLE = 6      # temporal subsampling

        head_trackers = []
        trails = []

        for color, nl, seed, init in zip(colors, noise_levels, seeds, inits):
            traj = generate_trajectory(T=40, noise=nl, seed=seed, init=init)
            pts = to_points_3d(traj[::STEP_SUBSAMPLE])
            n_pts = len(pts)

            head = ValueTracker(0)
            head_trackers.append(head)

            alphas = np.linspace(0.1, 0.9, TAIL_LENGTH)

            def make_trail(head=head, points=pts, col=color, alpha_vals=alphas):
                head_idx = int(head.get_value())
                start = max(0, head_idx - TAIL_LENGTH + 1)
                segment = points[start : head_idx + 1]
                L = len(segment)
                if L == 0:
                    return VGroup()

                op = np.linspace(0.1, 0.9, L)
                spheres = [
                    Sphere(
                        center=p,
                        radius=0.05,
                        resolution=(12, 12),
                        fill_opacity=op[k],
                        fill_color=col,
                        stroke_opacity=0.0,
                    )
                    for k, p in enumerate(segment)
                ]
                return VGroup(*spheres)

            trail = always_redraw(make_trail)
            trails.append(trail)
            self.add(trail)

        # All trajectories use same T, dt, subsampling
        n_points = len(to_points_3d(generate_trajectory(T=40)[::STEP_SUBSAMPLE]))

        # Start a gentle ambient camera rotation
        self.begin_ambient_camera_rotation(rate=0.15)

        self.play(
            *[head.animate.set_value(n_points - 1) for head in head_trackers],
            run_time=25,
            rate_func=linear,
        )

        self.wait(2)
        self.stop_ambient_camera_rotation()
