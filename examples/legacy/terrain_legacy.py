'''
Author: GitHub Copilot
Date: 2025-04-19
Description: Example demonstrating terrain generation for legged locomotion
FilePath: /blender_utils/examples/legacy/terrain_legacy.py
'''

import os
import sys
# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Check if we have noise dependencies
try:
    from noise import pnoise2
    print("noise module is available - Perlin noise will be used for terrain generation")
    NOISE_MODULE = "noise"
except ImportError:
    try:
        import opensimplex
        print("opensimplex module is available - OpenSimplex noise will be used for terrain generation")
        NOISE_MODULE = "opensimplex"
    except ImportError:
        print("Warning: Neither noise nor opensimplex modules are available.")
        print("Using simple random noise fallback - terrain quality will be reduced.")
        print("To install noise module, run examples/install_noise_for_blender.py from Blender's script editor")
        NOISE_MODULE = "fallback"

import bpy
import numpy as np
from blender_utils.modeling.terrain_gen import TerrainGenerator
from blender_utils.modeling.confined_terrain_gen import ConfinedTerrainGenerator


def clear_scene():
    """Clear all objects in the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Also remove all meshes from memory
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)


def setup_lighting():
    """Set up basic lighting for better visualization"""
    # Create a sun light
    light_data = bpy.data.lights.new(name="Sun", type='SUN')
    light_data.energy = 2.0
    light_object = bpy.data.objects.new(name="Sun", object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    light_object.location = (0, 0, 10)
    light_object.rotation_euler = (np.radians(45), 0, np.radians(45))

    # Create ambient light
    light_data = bpy.data.lights.new(name="Ambient", type='AREA')
    light_data.energy = 1.0
    light_object = bpy.data.objects.new(name="Ambient", object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    light_object.location = (0, 0, 5)
    light_object.scale = (10, 10, 1)


def setup_camera():
    """Set up a camera for a nice view of the terrain"""
    # Create camera
    camera_data = bpy.data.cameras.new(name="Camera")
    camera_object = bpy.data.objects.new(name="Camera", object_data=camera_data)
    bpy.context.collection.objects.link(camera_object)
    camera_object.location = (7, -7, 5)
    camera_object.rotation_euler = (np.radians(60), 0, np.radians(45))

    # Set as active camera
    bpy.context.scene.camera = camera_object


def example_flat_terrain():
    """Example of generating a flat terrain"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Create a terrain generator
    terrain_gen = TerrainGenerator(bpy)

    # Generate a flat terrain
    terrain_gen.generate_flat_terrain(
        name="FlatGround",
        size=(10, 10),
        position=(0, 0, 0),
        resolution=(50, 50)
    )

    print("Flat terrain generated successfully.")


def example_stairs():
    """Example of generating stairs"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Create a terrain generator
    terrain_gen = TerrainGenerator(bpy)

    # Generate stairs
    terrain_gen.generate_stairs(
        name="Stairs",
        size=(10, 10),
        position=(0, 0, 0),
        resolution=(50, 50),
        step_height=0.2,
        step_depth=1.0,
        steps=10,
        direction='x'
    )

    print("Stairs generated successfully.")


def example_ramp():
    """Example of generating a ramp"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Create a terrain generator
    terrain_gen = TerrainGenerator(bpy)

    # Generate a ramp
    terrain_gen.generate_ramp(
        name="Ramp",
        size=(10, 10),
        position=(0, 0, 0),
        resolution=(50, 50),
        height=2.0,
        direction='x',
        slope_type='linear'
    )

    print("Ramp generated successfully.")


def example_noisy_terrain():
    """Example of generating a noisy terrain"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Create a terrain generator
    terrain_gen = TerrainGenerator(bpy)

    # Generate a noisy terrain
    terrain_gen.generate_noisy_terrain(
        name="NoisyTerrain",
        size=(10, 10),
        position=(0, 0, 0),
        resolution=(100, 100),
        base_height=0,
        noise_amplitude=0.5,
        noise_scale=0.2,
        seed=42
    )

    print("Noisy terrain generated successfully.")


def example_combined_terrain():
    """Example of generating a combined terrain with multiple sections"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Create a terrain generator
    terrain_gen = TerrainGenerator(bpy)

    # Define sections for the combined terrain
    sections = [
        # Flat section
        {'type': 'flat', 'start_x': 0.0, 'end_x': 0.2, 'start_y': 0.0, 'end_y': 1.0},

        # Stairs section
        {'type': 'stairs', 'start_x': 0.2, 'end_x': 0.4, 'start_y': 0.0, 'end_y': 1.0,
         'step_height': 0.25, 'steps': 5, 'direction': 'x'},

        # Ramp section
        {'type': 'ramp', 'start_x': 0.4, 'end_x': 0.6, 'start_y': 0.0, 'end_y': 1.0,
         'height': 1.5, 'direction': 'x', 'slope_type': 'linear'},

        # Flat section at elevated height
        {'type': 'flat', 'start_x': 0.6, 'end_x': 0.8, 'start_y': 0.0, 'end_y': 1.0,
         'base_height': 1.5},

        # Noisy section
        {'type': 'noise', 'start_x': 0.8, 'end_x': 1.0, 'start_y': 0.0, 'end_y': 1.0,
         'base_height': 1.5, 'noise_amplitude': 0.3, 'noise_scale': 0.1}
    ]

    # Generate a combined terrain
    terrain_gen.generate_combined_terrain(
        name="CombinedTerrain",
        size=(20, 10),
        position=(0, 0, 0),
        resolution=(200, 100),
        sections=sections
    )

    # Adjust the camera for a better view
    camera = bpy.data.objects["Camera"]
    camera.location = (10, -15, 8)
    camera.rotation_euler = (np.radians(55), 0, np.radians(60))

    print("Combined terrain generated successfully.")


def example_legged_robot_test_course():
    """Create a comprehensive test course for legged robot locomotion"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Create a terrain generator
    terrain_gen = TerrainGenerator(bpy)

    # Define sections for the combined terrain
    sections = [
        # Starting flat section
        {'type': 'flat', 'start_x': 0.0, 'end_x': 0.15, 'start_y': 0.0, 'end_y': 1.0},

        # Low stairs section
        {'type': 'stairs', 'start_x': 0.15, 'end_x': 0.3, 'start_y': 0.0, 'end_y': 1.0,
         'step_height': 0.1, 'steps': 5, 'direction': 'x'},

        # Flat section after stairs
        {'type': 'flat', 'start_x': 0.3, 'end_x': 0.35, 'start_y': 0.0, 'end_y': 1.0,
         'base_height': 0.5},

        # Gentle ramp down
        {'type': 'ramp', 'start_x': 0.35, 'end_x': 0.45, 'start_y': 0.0, 'end_y': 1.0,
         'height': -0.5, 'direction': 'x', 'slope_type': 'linear'},

        # Gentle noisy terrain
        {'type': 'noise', 'start_x': 0.45, 'end_x': 0.6, 'start_y': 0.0, 'end_y': 1.0,
         'base_height': 0.0, 'noise_amplitude': 0.15, 'noise_scale': 0.1},

        # Steep ramp up
        {'type': 'ramp', 'start_x': 0.6, 'end_x': 0.65, 'start_y': 0.0, 'end_y': 1.0,
         'height': 1.0, 'direction': 'x', 'slope_type': 'linear'},

        # High flat section
        {'type': 'flat', 'start_x': 0.65, 'end_x': 0.7, 'start_y': 0.0, 'end_y': 1.0,
         'base_height': 1.0},

        # Steep stairs down
        {'type': 'stairs', 'start_x': 0.7, 'end_x': 0.85, 'start_y': 0.0, 'end_y': 1.0,
         'step_height': -0.2, 'steps': 5, 'direction': 'x'},

        # Final challenging noise section
        {'type': 'noise', 'start_x': 0.85, 'end_x': 1.0, 'start_y': 0.0, 'end_y': 1.0,
         'base_height': 0.0, 'noise_amplitude': 0.3, 'noise_scale': 0.05}
    ]

    # Generate a combined terrain
    terrain_gen.generate_combined_terrain(
        name="LeggaedRobotTestCourse",
        size=(30, 10),
        position=(0, 0, 0),
        resolution=(300, 100),
        sections=sections
    )

    # Adjust the camera for a better view
    camera = bpy.data.objects["Camera"]
    camera.location = (15, -20, 10)
    camera.rotation_euler = (np.radians(60), 0, np.radians(65))

    print("Legged robot test course generated successfully.")


def example_square_terrain_patches():
    """Example of generating a terrain with square patches (like leggedgym)"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Create a terrain generator
    terrain_gen = TerrainGenerator(bpy)

    # Define custom terrain types
    terrain_types = [
        # Flat ground
        {'type': 'flat', 'base_height': 0.0},
        # Low-height stairs
        {'type': 'stairs', 'step_height': 0.12, 'steps': 4, 'direction': 'random'},
        # Medium-height stairs
        {'type': 'stairs', 'step_height': 0.18, 'steps': 3, 'direction': 'random'},
        # Gentle slope ramp
        {'type': 'ramp', 'height': 0.3, 'direction': 'random', 'slope_type': 'linear'},
        # Steeper ramp
        {'type': 'ramp', 'height': 0.5, 'direction': 'random', 'slope_type': 'linear'},
        # Sinusoidal ramp
        {'type': 'ramp', 'height': 0.4, 'direction': 'random', 'slope_type': 'sinusoidal'},
        # Low noise terrain
        {'type': 'noise', 'base_height': 0.0, 'noise_amplitude': 0.1, 'noise_scale': 0.15},
        # Medium noise terrain
        {'type': 'noise', 'base_height': 0.0, 'noise_amplitude': 0.2, 'noise_scale': 0.1},
    ]

    # Generate square patches terrain with improved padding and transitions
    terrain_gen.generate_square_terrain_patches(
        name="SquareTerrain",
        size=(30, 30),           # Make it large enough for robot testing
        position=(0, 0, 0),
        resolution=(300, 300),   # Higher resolution for smoother transitions
        num_patches=(5, 5),      # 5×5 grid of different terrains
        terrain_types=terrain_types,
        padding_ratio=0.15,      # Use 15% of patch size as padding between patches
        transition_smoothness=0.7,  # Higher values make transitions smoother
        max_height_diff=0.8,     # Limit height differences between adjacent patches
        seed=42                  # For reproducible results
    )

    # Position the camera for a better view of the square patches
    camera = bpy.data.objects["Camera"]
    camera.location = (15, -15, 20)
    camera.rotation_euler = (np.radians(60), 0, np.radians(45))

    print("Square terrain patches generated successfully.")


def example_confined_terrain_boxes():
    """Example of generating a confined terrain with boxes as obstacles"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Create a confined terrain generator
    terrain_gen = ConfinedTerrainGenerator(bpy)

    # Generate a confined terrain with random box obstacles
    terrain_gen.generate_with_boxes(
        name="ConfinedTerrainBoxes",
        size=(10, 10),
        position=(0, 0, 0),
        layer_distance=2.0,
        ground_height=0.0,
        box_count=20,
        min_box_size=(0.5, 0.5, 0.3),
        max_box_size=(2.0, 2.0, 1.5)
    )

    # Adjust the camera for a better view
    camera = bpy.data.objects["Camera"]
    camera.location = (8, -10, 5)
    camera.rotation_euler = (np.radians(55), 0, np.radians(50))

    print("Confined terrain with box obstacles generated successfully.")


def example_confined_terrain_surfaces():
    """Example of generating a confined terrain with surface modifications"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Create a confined terrain generator
    terrain_gen = ConfinedTerrainGenerator(bpy)

    # Generate a confined terrain with surface modifications
    terrain_gen.generate_with_surface_modifications(
        name="ConfinedTerrainSurfaces",
        size=(50, 50),
        position=(0, 0, 0),
        layer_distance=2.0,
        ground_height=0.0,
        ceiling_height=2.0,
        obstacle_count=500,
        min_obstacle_size=(0.1, 0.1, 0.02),
        max_obstacle_size=(5.0, 5.0, 1.0),
        resolution=(500, 500)
    )

    # Adjust the camera for a better view
    camera = bpy.data.objects["Camera"]
    camera.location = (8, -10, 5)
    camera.rotation_euler = (np.radians(55), 0, np.radians(50))

    print("Confined terrain with surface modifications generated successfully.")


def example_complex_confined_environment():
    """Create a complex confined environment with varying ceiling height"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Create a terrain generator and confined terrain generator
    terrain_gen = TerrainGenerator(bpy)
    confined_gen = ConfinedTerrainGenerator(bpy)

    # Generate a noisy ground layer
    ground_heights = terrain_gen.generate_noisy_terrain(
        name="NoisyGround",
        size=(15, 15),
        position=(0, 0, 0),
        resolution=(80, 80),
        base_height=0.0,
        noise_amplitude=0.3,
        noise_scale=0.15,
        seed=42
    )

    # Generate a ceiling with complementary pattern but inverted
    # Creating a cave-like environment where low ground has higher ceiling
    ceiling_heights = np.zeros_like(ground_heights)
    for i in range(ceiling_heights.shape[0]):
        for j in range(ceiling_heights.shape[1]):
            # Make ceiling height inversely related to ground height
            # Base ceiling is at 3.0, lower where ground is higher
            ceiling_heights[i, j] = 3.0 - ground_heights[i, j] * 0.5

    # Delete the temporary ground mesh
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['NoisyGround'].select_set(True)
    bpy.ops.object.delete()

    # Now generate the confined terrain with these height maps
    confined_gen.generate_with_boxes(
        name="ComplexConfinedEnvironment",
        size=(15, 15),
        position=(0, 0, 0),
        ground_heights=ground_heights,
        ceiling_heights=ceiling_heights,
        box_count=25,
        min_box_size=(0.8, 0.8, 0.5),
        max_box_size=(2.5, 2.5, 1.8)
    )

    # Adjust the camera for a better view
    camera = bpy.data.objects["Camera"]
    camera.location = (10, -12, 6)
    camera.rotation_euler = (np.radians(55), 0, np.radians(55))

    print("Complex confined environment generated successfully.")


if __name__ == "<run_path>":
    # Uncomment the example you want to run

    # === IsaacGym Style Terrain === #
    # example_flat_terrain()
    # example_stairs()
    # example_ramp()
    # example_noisy_terrain()
    # example_combined_terrain()
    # example_legged_robot_test_course()
    # example_square_terrain_patches()

    # === Confined Environment === #
    """ Boxes + Planes """
    # example_confined_terrain_boxes()
    # example_complex_confined_environment()
    """ Surfaces """
    example_confined_terrain_surfaces()
