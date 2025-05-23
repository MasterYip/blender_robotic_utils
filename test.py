'''
Author: MasterYip 2205929492@qq.com
Date: 2024-03-11 10:19:39
Description: file content
FilePath: /blender_utils/test.py
LastEditTime: 2025-01-28 21:10:03
LastEditors: MasterYip
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

# ================================================================
import bpy
import numpy as np
from blender_utils.modeling.gridmap_gen import gridmap_gen
from blender_utils.scene_creator.gcs_path_search import GCSPathSearch_Scene

points = [[-1.5, 0, 0], [0, 0, 1.5], [1.5, 0, 0.7]]
resolution = (40, 40)
bound = (-3, 3, -3, 3)

# scene = GCSPathSearch_Scene(bpy)
# # scene.setup()
# scene.create_guide_surf(
#     points, bound=bound, resolution=resolution)


# gridmap_gen(bpy, "Ground", h_mat, bound)

# bpy.ops.wm.collada_import(filepath="E:\\CodeTestFile\\Github-HITSME_HexLab\\Hexapod-robot-assets\\model\\elspider_air\\meshes\\BASE.dae")


# print all objects
# for obj in bpy.data.objects:
#     print(obj.name)

# print all scene names in a list
for obj in bpy.data.collections[2].objects:
    print(obj.name)
