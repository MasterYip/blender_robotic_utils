'''
Author: MasterYip 2205929492@qq.com
Date: 2024-03-11 10:19:39
Description: file content
FilePath: /blender_learning/test.py
LastEditTime: 2024-03-11 12:36:59
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
from blender_utils.scene_creator.gcs_path_search import GCSPathSearch_Scene

scene = GCSPathSearch_Scene(bpy)
scene.setup()
