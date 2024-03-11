'''
Author: MasterYip 2205929492@qq.com
Date: 2024-03-11 11:28:58
Description: file content
FilePath: /blender_learning/blender_utils/scene_creator/gcs_path_search.py
LastEditTime: 2024-03-11 12:57:48
LastEditors: MasterYip
'''

from ..modeling.gridmap_gen import gridmap_gen_function, gridmap_gen
from ..modeling.polygon_gen import ellipsoid_gen
import numpy as np


class HarmonicGuideSurf:
    def __init__(self, key_points: list, weight_order=1):
        self.key_points = key_points
        self.key_points_mat = np.array(key_points)
        self.weights = np.ones(len(key_points))
        self.weight_order = weight_order
        self.key_points_num = len(self.weights)

    def get_height(self, p):
        num = 0.0
        den = 0.0
        p_vec = p
        dists = np.linalg.norm(self.key_points_mat[:, :2] - p_vec, axis=1)
        for i in range(self.key_points_num):
            if dists[i] < 1e-6:
                return self.key_points_mat[i, 2]
            if self.weight_order == 1:
                num += self.weights[i] / dists[i] * self.key_points_mat[i, 2]
                den += self.weights[i] / dists[i]
            else:
                num += self.weights[i] / (dists[i] **
                                          self.weight_order) * self.key_points_mat[i, 2]
                den += self.weights[i] / (dists[i] ** self.weight_order)
        return num / den


class GCSPathSearch_Scene:
    def __init__(self, bpy):
        self.bpy = bpy
        # self.scene = bpy.context.scene
        # self.collection = bpy.context.collection
        # self.objects = bpy.context.collection.objects
        # self.meshes = bpy.data.meshes
        # self.materials = bpy.data.materials
        # self.textures = bpy.data.textures
        self.points = [[-3, 0, 2], [3, 0, 0]]
        self.resolution = (40, 40)
        self.bound = (-4, 4, -4, 4)

    def setup(self):
        ellipsoid_gen(self.bpy, "Ellipsoid", (3.7, 2.8, 3.0), 64, (0, 0, 1))
        self.create_guide_surf(
            self.points, bound=self.bound, resolution=self.resolution)
        self.create_ground(self.bound, resolution=self.resolution)

    def create_ground(self, bound, resolution=(10, 10)):
        h_mat = np.zeros(resolution)
        h_mat[resolution[0]//3:resolution[0]//3*2, :] = 1
        h_mat[0:resolution[0]//3, :] = 2
        gridmap_gen(self.bpy, "Ground", h_mat, bound)

    def create_guide_surf(self, points, bound=(-1, 1, -1, 1), resolution=(10, 10)):
        """Create Guide Surf

        Args:
            points (_type_): _description_
            bound (tuple, optional): _description_. Defaults to (-1, 1, -1, 1).
            resolution (tuple, optional): FIXME: Should be the same temporarily. Defaults to (10, 10).
        """
        guide_surf = HarmonicGuideSurf(points)
        h_mat = np.zeros((resolution[0]+1, resolution[1]+1))
        for i in range(resolution[0]+1):
            for j in range(resolution[1]+1):
                x = bound[0] + (bound[1]-bound[0])*i/resolution[0]
                y = bound[2] + (bound[3]-bound[2])*j/resolution[1]
                h_mat[i, j] = guide_surf.get_height(np.array([x, y]))
        gridmap_gen(self.bpy, "GuideSurf", h_mat, bound)
