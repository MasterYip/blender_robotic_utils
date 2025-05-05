'''
Author: GitHub Copilot
Date: 2025-05-05
Description: Examples for using utility functions from blender_utils
FilePath: /blender_utils/examples/utils/utils_examples.py
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
from blender_utils.utils.utils import link_obj_to_collection


def clear_scene():
    """Clear all objects in the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Also remove all meshes from memory
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)


def example_collection_organization():
    """Example of organizing objects into collections"""
    clear_scene()

    # Create a few test objects
    cube = bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    cube_obj = bpy.context.active_object
    cube_obj.name = "TestCube"

    sphere = bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(2, 0, 0))
    sphere_obj = bpy.context.active_object
    sphere_obj.name = "TestSphere"

    cylinder = bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2, location=(-2, 0, 0))
    cylinder_obj = bpy.context.active_object
    cylinder_obj.name = "TestCylinder"

    # Create new collections
    robots_collection = bpy.data.collections.new("Robots")
    obstacles_collection = bpy.data.collections.new("Obstacles")
    terrain_collection = bpy.data.collections.new("Terrain")

    # Link collections to the scene
    bpy.context.scene.collection.children.link(robots_collection)
    bpy.context.scene.collection.children.link(obstacles_collection)
    bpy.context.scene.collection.children.link(terrain_collection)

    # Use the utility function to link objects to collections
    link_obj_to_collection(cube_obj, robots_collection)
    link_obj_to_collection(sphere_obj, obstacles_collection)
    link_obj_to_collection(cylinder_obj, terrain_collection)

    print("Objects organized into collections successfully.")
    print(f"Cube linked to: {cube_obj.users_collection[0].name}")
    print(f"Sphere linked to: {sphere_obj.users_collection[0].name}")
    print(f"Cylinder linked to: {cylinder_obj.users_collection[0].name}")


def example_collection_creation():
    """Example of creating collections using the utility function"""
    clear_scene()

    # Create a few test objects
    cube = bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    cube_obj = bpy.context.active_object
    cube_obj.name = "TestCube"

    sphere = bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(2, 0, 0))
    sphere_obj = bpy.context.active_object
    sphere_obj.name = "TestSphere"

    # Create collections and link objects using the utility function
    # Collection will be created if it doesn't exist
    link_obj_to_collection(cube_obj, "RoboticParts")
    link_obj_to_collection(sphere_obj, "Sensors")

    print("Collections created and objects linked successfully.")
    print(f"Created collections: {[c.name for c in bpy.data.collections if c.name in ['RoboticParts', 'Sensors']]}")


if __name__ == "<run_path>":
    # Uncomment the example you want to run
    example_collection_organization()
    # example_collection_creation()
