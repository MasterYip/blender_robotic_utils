'''
Author: GitHub Copilot
Date: 2025-05-05
Description: Basic examples for terrain generation - flat, stairs, ramps, and noise
FilePath: /blender_utils/examples/modeling/terrain/terrain_basics.py
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


if __name__ == "__main__":
    # Uncomment the example you want to run
    example_flat_terrain()
    # example_stairs()
    # example_ramp()
    # example_noisy_terrain()