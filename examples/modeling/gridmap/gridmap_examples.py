'''
Author: GitHub Copilot
Date: 2025-05-05
Description: Examples for using gridmap generation functions to create terrain meshes
FilePath: /blender_utils/examples/modeling/gridmap/gridmap_examples.py
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
from blender_utils.modeling.gridmap_gen import gridmap_gen, gridmap_gen_from_img


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
    """Set up a camera for a nice view of the gridmap"""
    # Create camera
    camera_data = bpy.data.cameras.new(name="Camera")
    camera_object = bpy.data.objects.new(name="Camera", object_data=camera_data)
    bpy.context.collection.objects.link(camera_object)
    camera_object.location = (7, -7, 5)
    camera_object.rotation_euler = (np.radians(60), 0, np.radians(45))

    # Set as active camera
    bpy.context.scene.camera = camera_object


def example_sine_wave_gridmap():
    """Example of generating a gridmap with a sine wave pattern"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Define the grid resolution
    resolution = (50, 50)

    # Create a sine wave height map
    h_mat = np.zeros(resolution)
    for i in range(resolution[0]):
        for j in range(resolution[1]):
            x = i / resolution[0] * 4 * np.pi
            y = j / resolution[1] * 4 * np.pi
            h_mat[i, j] = 0.5 * np.sin(x) * np.sin(y)

    # Define the bounds of the gridmap (xmin, xmax, ymin, ymax)
    bound = (-5, 5, -5, 5)

    # Generate the gridmap mesh
    gridmap_gen(bpy, "SineWaveGridmap", h_mat, bound)

    print("Sine wave gridmap generated successfully.")


def example_checkerboard_gridmap():
    """Example of generating a gridmap with a checkerboard pattern"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Define the grid resolution
    resolution = (20, 20)

    # Create a checkerboard height map
    h_mat = np.zeros(resolution)
    checker_size = 4  # Size of each checker square

    for i in range(resolution[0]):
        for j in range(resolution[1]):
            if ((i // checker_size) % 2 == 0) != ((j // checker_size) % 2 == 0):
                h_mat[i, j] = 0.5

    # Define the bounds of the gridmap (xmin, xmax, ymin, ymax)
    bound = (-5, 5, -5, 5)

    # Generate the gridmap mesh
    gridmap_gen(bpy, "CheckerboardGridmap", h_mat, bound)

    print("Checkerboard gridmap generated successfully.")


def example_crater_gridmap():
    """Example of generating a gridmap with a crater-like pattern"""
    clear_scene()
    setup_lighting()
    setup_camera()

    # Define the grid resolution
    resolution = (100, 100)

    # Create a crater-like height map
    h_mat = np.zeros(resolution)
    center_x, center_y = resolution[0] / 2, resolution[1] / 2
    crater_radius = min(resolution) / 3
    rim_height = 1.0

    for i in range(resolution[0]):
        for j in range(resolution[1]):
            # Calculate distance from center
            dx = (i - center_x) / resolution[0]
            dy = (j - center_y) / resolution[1]
            distance = np.sqrt(dx**2 + dy**2) * 10

            # Create crater profile
            if distance < crater_radius:
                # Inside crater
                crater_depth = 0.5 * (1 - distance / crater_radius)
                h_mat[i, j] = -crater_depth
            else:
                # Crater rim and surroundings
                rim_falloff = max(0, 1 - (distance - crater_radius))
                h_mat[i, j] = rim_height * rim_falloff * 0.5

    # Define the bounds of the gridmap (xmin, xmax, ymin, ymax)
    bound = (-5, 5, -5, 5)

    # Generate the gridmap mesh
    gridmap_gen(bpy, "CraterGridmap", h_mat, bound)

    print("Crater gridmap generated successfully.")


def example_image_gridmap():
    gridmap_gen_from_img(bpy, "test_grid",
                         os.path.join(ROOT_DIR, "terrain", "terrain_ground.png"),
                         (0, 0), 0.5, (0, 3))
    print("Gridmap generated from image successfully.")


if __name__ == "<run_path>":
    # Uncomment the example you want to run
    # example_sine_wave_gridmap()
    # example_checkerboard_gridmap()
    # example_crater_gridmap()
    example_image_gridmap()
