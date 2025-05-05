'''
Author: GitHub Copilot
Date: 2025-05-05
Description: Examples for using GCSPathSearch for scene creation and path planning
FilePath: /blender_utils/examples/scene_creator/gcs_path_search_examples.py
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
parent_dir = os.path.abspath(os.path.join(ROOT_DIR, '..', '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import bpy
import numpy as np
from blender_utils.scene_creator.gcs_path_search import GCSPathSearch_Scene
from blender_utils.modeling.polygon_gen import ellipsoid_gen


def setup_default_scene():
    """
    Sets up a default scene for GCS path search examples
    """
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Set up lighting
    light_data = bpy.data.lights.new(name="Sun", type='SUN')
    light_object = bpy.data.objects.new(name="Sun", object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    light_object.location = (0, 0, 10)
    light_object.rotation_euler = (np.radians(60), 0, np.radians(30))


def example_basic_gcs_scene():
    """Example of creating a basic scene with guide surface and ground"""
    setup_default_scene()
    
    # Create a GCSPathSearch_Scene object
    scene = GCSPathSearch_Scene(bpy)
    
    # Define waypoints for the guide surface
    points = [[-20, 0, 0], [0, 0, 20], [20, 0, 0]]
    
    # Set up the scene
    scene.setup()
    
    print("Basic GCS scene created successfully.")


def example_custom_gcs_scene():
    """Example of creating a custom GCS scene with specified parameters"""
    setup_default_scene()
    
    # Create a GCSPathSearch_Scene object
    scene = GCSPathSearch_Scene(bpy)
    
    # Define waypoints for the guide surface
    points = [[-3, 0, 2], [3, 0, 0]]
    bound = (-4, 4, -4, 4)
    resolution = (40, 40)
    
    # Create an obstacle (ellipsoid)
    ellipsoid_gen(bpy, "Ellipsoid", (3.7, 2.8, 3.0), 64, (0, 0, 1))
    
    # Create guide surface and ground
    scene.create_guide_surf(points, bound=bound, resolution=resolution)
    scene.create_ground(bound, resolution=resolution)
    
    print("Custom GCS scene created successfully.")


if __name__ == "<run_path>":
    # Uncomment the example you want to run
    # example_basic_gcs_scene()
    example_custom_gcs_scene()