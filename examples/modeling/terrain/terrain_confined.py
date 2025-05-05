'''
Author: GitHub Copilot
Date: 2025-05-05
Description: Examples for using the ConfinedTerrainGenerator to create confined spaces with obstacles
FilePath: /blender_utils/examples/modeling/terrain/terrain_confined.py
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


def example_confined_terrain_boxes():
    """Generate a confined terrain with boxes as obstacles"""
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
        box_count=15,
        min_box_size=(0.5, 0.5, 0.3),
        max_box_size=(2.0, 2.0, 1.5)
    )

    # Adjust the camera for a better view
    camera = bpy.data.objects["Camera"]
    camera.location = (8, -10, 5)
    camera.rotation_euler = (np.radians(55), 0, np.radians(50))

    print("Confined terrain with box obstacles generated successfully.")


def example_confined_terrain_surfaces():
    """Generate a confined terrain with surface modifications"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Create a confined terrain generator
    terrain_gen = ConfinedTerrainGenerator(bpy)

    # Generate a confined terrain with surface modifications
    terrain_gen.generate_with_surface_modifications(
        name="ConfinedTerrainSurfaces",
        size=(10, 10),
        position=(0, 0, 0),  # Place next to the first terrain
        layer_distance=2.0,
        obstacle_count=15,
        min_obstacle_size=(0.5, 0.5, 0.3),
        max_obstacle_size=(2.0, 2.0, 0.8),
        resolution=(100, 100)
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
    example_confined_terrain_boxes()
    # example_confined_terrain_surfaces()
    # example_complex_confined_environment()
