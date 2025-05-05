'''
Author: GitHub Copilot
Date: 2025-05-05
Description: Examples for surface generation using blender_utils
FilePath: /blender_utils/examples/modeling/surface_gen_examples.py
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
import math
from mathutils import Vector
from blender_utils.modeling.surface_gen import create_nurbs_surf, eg_create_poly_surf_from_border_points


def example_nurbs_surface():
    """Example of creating a NURBS surface"""
    # Clear existing scene objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Create a NURBS surface
    create_nurbs_surf()

    print("NURBS surface created successfully.")


def example_poly_surface_from_border():
    """Example of creating a polygonal surface from border points with a height function"""
    # The function will clear the scene internally
    eg_create_poly_surf_from_border_points()

    print("Polygonal surface created successfully.")


if __name__ == "<run_path>":
    # Uncomment the example you want to run
    example_nurbs_surface()
    # example_poly_surface_from_border()
