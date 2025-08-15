# scene.py
from manim import *
import matplotlib.pyplot as plt
# Import our simulation engine from the other file
from GrayyScott import GrayScottSimulation

class MorphingPatternsScene(Scene):
    """
    A Manim scene that visualizes the Gray-Scott model with
    parameters that change over time, causing the pattern to morph.
    """
    def construct(self):
        # --- Define the start and end parameters for the morph ---
        params = {
            "Worms": (0.078, 0.061),
            "Mazes": (0.029, 0.057),
        }
        f_start, k_start = params["Worms"]
        f_end, k_end = params["Mazes"]

        # 1. --- Set up Manim ValueTrackers ---
        f_tracker = ValueTracker(f_start)
        k_tracker = ValueTracker(k_start)

        # 2. --- Initialize the Simulation ---
        sim = GrayScottSimulation(size=256, f_tracker=f_tracker, k_tracker=k_tracker)

        # 3. --- Create the On-Screen Text and Equations ---
        pde_text = MathTex(
            r"\frac{\partial u}{\partial t} = D_u \nabla^2 u - uv^2 + f(1-u) \\",
            r"\frac{\partial v}{\partial t} = D_v \nabla^2 v + uv^2 - (f+k)v",
            font_size=32
        ).to_corner(UL, buff=0.2)

        f_label = MathTex("f = ", font_size=36)
        k_label = MathTex("k = ", font_size=36)
        f_value = DecimalNumber(f_start, num_decimal_places=4, font_size=36)
        k_value = DecimalNumber(k_start, num_decimal_places=4, font_size=36)
        
        param_group = VGroup(
            VGroup(f_label, f_value).arrange(RIGHT, buff=0.2), 
            VGroup(k_label, k_value).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(pde_text, DOWN, buff=0.3, aligned_edge=LEFT)

        f_value.add_updater(lambda m: m.set_value(f_tracker.get_value()))
        k_value.add_updater(lambda m: m.set_value(k_tracker.get_value()))
        
        self.add(pde_text, param_group)

        # 4. --- Create the Main Visual ---
        cmap = plt.cm.plasma
        initial_gray_data = sim.get_v_channel_as_image()
        initial_color_data = (cmap(initial_gray_data / 255.0) * 255).astype(np.uint8)
        
        image = ImageMobject(initial_color_data).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        
        image.set_height(self.camera.frame_height)
        image.to_corner(UR)
        self.add(image)

        # --- FIX IS HERE ---
        # The updater now uses the .become() method, which is the correct approach.
        def update_image(mob, dt):
            # Advance the simulation
            sim.step(steps=5)
            
            # Get the new data and apply the colormap
            new_gray_data = sim.get_v_channel_as_image()
            new_color_data = (cmap(new_gray_data / 255.0) * 255).astype(np.uint8)
            
            # Create a new ImageMobject from the new data
            new_image = ImageMobject(new_color_data).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            
            # Match the size and position of the original image
            new_image.set_height(mob.get_height())
            new_image.move_to(mob)
            
            # Use .become() to transform the old image into the new one
            mob.become(new_image)
        # --- FIX ENDS HERE ---

        image.add_updater(update_image)
        
        sim.step(steps=2000)
        self.wait(1)

        # 5. --- Animate the Morph ---
        self.play(
            f_tracker.animate.set_value(f_end),
            k_tracker.animate.set_value(k_end),
            run_time=15,
            rate_func=rate_functions.smooth
        )
        
        self.wait(5)