from manim import *
import numpy as np


class LorenzTrajectories(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # GLOBAL STYLE
        # ------------------------------------------------------------------
        # Set a dark background to mimic the “phase–portrait in space” look.
        self.camera.background_color = "#000000"

        # Colors (one per trajectory) and noise levels
        colors = ["#8d4af9", "#4ebff7", "#ffc078"]
        noise_levels = [0.0, 0.1, 0.5]
        seeds = [8676, 8089, 435451]
        inits = [(10, -10, 31), (-10.5, 22, 41.3), (0.5, 0.8, 21.5)]

        # ------------------------------------------------------------------
        # LORENZ SYSTEM + TRAJECTORY GENERATION
        # ------------------------------------------------------------------
        # These are plain numerical routines. Manim is mainly used for
        # the *visualisation*, not the numerical integration itself.

        def lorenz_step(x, y, z, s=10, r=28, b=8 / 3, dt=0.001):
            """One explicit Euler step of the Lorenz system."""
            dx = s * (y - x)
            dy = x * (r - z) - y
            dz = x * y - b * z
            return x + dx * dt, y + dy * dt, z + dz * dt

        def generate_trajectory(T=30, dt=0.0005, noise=0.0, seed=0, init=(1, 1, 1)):
            """
            Integrate Lorenz forward in time and optionally add
            Gaussian measurement noise (on x and y only).
            """
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

            return np.stack([x, y, z], axis=1)  # shape (N, 3)

        # ------------------------------------------------------------------
        # COORDINATE NORMALISATION
        # ------------------------------------------------------------------
        # We project to 2D (x, y), center, normalise and scale so that
        # everything fits nicely in the camera frame.

        base_traj = generate_trajectory(T=50, noise=0.0, seed=1)
        xy = base_traj[:, :2]
        xy -= xy.mean(axis=0)                  # center in (x, y)
        xy /= np.max(np.abs(xy)) * 1.2         # normalise radius
        scale_factor = 6.0                     # global scale

        def to_points(traj):
            """
            Map Lorenz (x, y, z) to 2D Manim points in the scene.
            Only x,y are used; z is ignored in this projection.
            """
            xy = traj[:, :2].copy()
            xy -= xy.mean(axis=0)
            xy /= np.max(np.abs(xy)) * 1.2
            xy *= scale_factor
            # Optional anisotropic scaling to get a pleasing aspect ratio
            xy[:, 0] *= 2.0
            xy[:, 1] *= 0.75
            # Convert to Manim points
            return [np.array([px, py, 0.0]) for px, py in xy]

        # ------------------------------------------------------------------
        # BACKGROUND ATTRACTOR (FAINT REFERENCE)
        # ------------------------------------------------------------------
        # Here Manim helps by letting us create a smooth curve and keep it
        # fixed in the background as a reference "attractor" geometry.

        base_points = to_points(base_traj[::10])  # subsample for speed
        base_line = VMobject(color=GRAY_D, stroke_opacity=0.25)
        base_line.set_points_smoothly(base_points)
        self.add(base_line)

        # ------------------------------------------------------------------
        # MOVING TRAJECTORIES WITH FADING TAILS (MANIM WAY)
        # ------------------------------------------------------------------
        # Instead of manually looping with self.wait() inside Python,
        # we let Manim handle the frame-by-frame updating via ValueTrackers
        # and always_redraw. This is also more efficient.
        #
        # For each trajectory:
        #   - Precompute the list of points
        #   - Use a ValueTracker to represent the "head" index
        #   - Use always_redraw to build a VGroup of dots corresponding
        #     to the last TAIL_LENGTH points.
        #   - Animate the ValueTracker from 0 to N over time.

        TAIL_LENGTH = 100          # maximum number of trail points
        STEP_SUBSAMPLE = 6         # temporal subsampling

        head_trackers = []
        trail_groups = []

        # Precompute trajectories and corresponding Manim points
        for color, nl, seed, init in zip(colors, noise_levels, seeds, inits):
            traj = generate_trajectory(T=40, noise=nl, seed=seed, init=init)
            pts = to_points(traj[::STEP_SUBSAMPLE])   # subsample for efficiency
            n_pts = len(pts)

            # This ValueTracker will move from 0 to n_pts - 1
            head_tracker = ValueTracker(0)

            # Precompute opacities for the tail, from faint to bright
            # (0 at the tail’s start, 1 at the “head”).
            alphas = np.linspace(0.1, 0.9, TAIL_LENGTH)

            def make_trail(head=head_tracker, points=pts, col=color, alpha_values=alphas):
                """
                Rebuild the trail group at each frame.
                This function is called automatically by always_redraw.
                """
                head_idx = int(head.get_value())
                # Indices for the trail: [head_idx - TAIL_LENGTH + 1, ..., head_idx]
                start = max(0, head_idx - TAIL_LENGTH + 1)
                segment = points[start: head_idx + 1]
                # Match opacity to segment length
                L = len(segment)
                if L == 0:
                    return VGroup()
                # Resample alphas to current segment length
                op = np.linspace(0.1, 0.9, L)
                dots = [
                    Dot(p, color=col, radius=0.05, fill_opacity=op[k])
                    for k, p in enumerate(segment)
                ]
                return VGroup(*dots)

            trail = always_redraw(make_trail)
            self.add(trail)

            head_trackers.append(head_tracker)
            trail_groups.append(trail)

        # ------------------------------------------------------------------
        # ANIMATION OF THE HEAD INDEX
        # ------------------------------------------------------------------
        # Now we animate the ValueTrackers together. This is where Manim
        # shines: you express *what* should change (the head indices), and
        # Manim handles interpolation and redrawing of all dependent objects.

        # All trajectories have the same number of subsampled points here
        n_points = len(to_points(generate_trajectory(T=40)[::STEP_SUBSAMPLE]))

        self.play(
            *[
                head.animate.set_value(n_points - 1)
                for head in head_trackers
            ],
            run_time=25,
            rate_func=linear,
        )

        self.wait(2)
