'''
Author: GitHub Copilot
Date: 2025-05-05
Description: Examples for creating combined and complex terrains for robot testing
FilePath: /blender_utils/examples/modeling/terrain/terrain_combined.py
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

# Add parent directories to path to ensure imports work properly
parent_dir = os.path.abspath(os.path.join(ROOT_DIR, '..', '..', '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import bpy
import numpy as np
from blender_utils.modeling.terrain_gen import TerrainGenerator


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


if __name__ == "<run_path>":
    # Uncomment the example you want to run
    example_combined_terrain()
    # example_legged_robot_test_course()
    # example_square_terrain_patches()
