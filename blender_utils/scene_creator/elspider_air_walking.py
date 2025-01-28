'''
Author: MasterYip 2205929492@qq.com
Date: 2025-01-26 21:53:13
Description: file content
FilePath: /blender_utils/blender_utils/scene_creator/elspider_air_walking.py
LastEditTime: 2025-01-27 20:48:15
LastEditors: MasterYip
'''

import os
import yaml
import cv2
import bpy
from blender_utils.modeling.gridmap_gen import gridmap_gen_from_img

# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()


class RobotAnimatorConfig(dict):
    """Config Class"""

    def __init__(self, yaml_path):
        with open(yaml_path, 'r') as file:
            prime_service = yaml.safe_load(file)
            self.update(prime_service)
        pass


class ElSpiderWalkingScene(object):
    def __init__(self, bpy, scene_folder):
        self.bpy = bpy
        self.scene_folder = scene_folder
        self.ground_filename = "terrain_ground.png"
        self.ceiling_filename = "terrain_ceiling.png"
        self.gridmap_config_name = "gridmap_config.yaml"

        # Load resource
        self.img_ground_path = os.path.join(self.scene_folder, self.ground_filename)
        self.img_ceiling_path = os.path.join(self.scene_folder, self.ceiling_filename)
        self.gridmap_config = {}
        with open(os.path.join(self.scene_folder, self.gridmap_config_name), 'r') as file:
            prime_service = yaml.safe_load(file)
            self.gridmap_config.update(prime_service)

        # Load terrains
        self.load_terrains(False)

    def load_terrains(self, with_ceiling=True):
        scaling = 100
        ground_bound = (self.gridmap_config["min_height"]*scaling, self.gridmap_config["max_height"]*scaling)
        ceiling_bound = (self.gridmap_config["min_height_ceiling"]*scaling, self.gridmap_config["max_height_ceiling"]*scaling)
        resolution = self.gridmap_config["resolution"]*scaling
        position = (self.gridmap_config["map_position_x"]*scaling, self.gridmap_config["map_position_y"]*scaling)
        gridmap_gen_from_img(self.bpy, "Ground", self.img_ground_path, position, resolution,  ground_bound)
        if with_ceiling:
            gridmap_gen_from_img(self.bpy, "Ceiling", self.img_ceiling_path, position, resolution, ceiling_bound)


if __name__ == "<run_path>":
    scene = ElSpiderWalkingScene(bpy, os.path.join(ROOT_DIR, "planning_scene", "4_barrier"))
