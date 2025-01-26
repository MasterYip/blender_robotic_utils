'''
Author: MasterYip 2205929492@qq.com
Date: 2024-03-11 10:26:37
Description: file content
FilePath: /blender_utils/blender_utils/modeling/gridmap_gen.py
LastEditTime: 2025-01-26 21:51:36
LastEditors: MasterYip
'''

import math

from numpy import size
import bpy
import cv2
import os

# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()


def gridmap_gen(bpy_nh, name, heights, bound=(-1, 1, -1, 1)):
    # 计算分辨率
    resolution_x = len(heights)
    resolution_y = len(heights[0])

    # 生成网格顶点
    verts = []
    for i in range(resolution_x):
        for j in range(resolution_y):
            x = bound[0] + (bound[1] - bound[0]) * i / (resolution_x - 1)
            y = bound[2] + (bound[3] - bound[2]) * j / (resolution_y - 1)
            z = heights[i][j]
            verts.append((x, y, z))

    # 生成面
    faces = []
    for i in range(resolution_x - 1):
        for j in range(resolution_y - 1):
            v1 = i * resolution_y + j
            v2 = v1 + 1
            v3 = v1 + resolution_y + 1
            v4 = v1 + resolution_y
            faces.append((v1, v2, v3, v4))

    # 创建网格对象并添加网格数据
    mesh = bpy_nh.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)

    # 创建网格对象并添加到场景
    obj = bpy_nh.data.objects.new(name, mesh)
    bpy_nh.context.collection.objects.link(obj)


def height_function_eg(x, y):
    # 这里可以是任何你想要的函数
    return math.sin(x) * math.cos(y)


def gridmap_gen_function(bpy_nh, name, height_func, resolution: tuple = (10, 10), grid_size=0.05):
    # 生成网格顶点
    verts = []
    for i in range(resolution[0] + 1):
        for j in range(resolution[1] + 1):
            x = grid_size * (i / resolution[0] - 0.5)
            y = grid_size * (j / resolution[1] - 0.5)
            z = height_func(x, y)
            verts.append((x, y, z))

    # 生成面
    faces = []
    for i in range(resolution[0]):
        for j in range(resolution[1]):
            v1 = i * (resolution[1] + 1) + j
            v2 = v1 + 1
            v3 = v1 + resolution[1] + 2
            v4 = v1 + resolution[1] + 1
            faces.append((v1, v2, v3, v4))

    # 创建网格对象并添加网格数据
    mesh = bpy_nh.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)

    # 创建网格对象并添加到场景
    obj = bpy_nh.data.objects.new(name, mesh)
    bpy_nh.context.collection.objects.link(obj)


def img2heightmat(img_path, height_bound=(0, 1)):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    heights = []
    for i in range(img.shape[0]):
        heights.append([])
        for j in range(img.shape[1]):
            heights[i].append(
                height_bound[0] + (height_bound[1] - height_bound[0]) * img[i, j] / 255)
    return heights


def gridmap_gen_from_img(bpy_nh, name, img_path, position=(0, 0),
                         resolution=0.05, height_bound=(0, 1)):
    heights = img2heightmat(img_path, height_bound)
    size_x = len(heights)
    size_y = len(heights[0])
    # centering
    bounds = (
        position[0] - resolution * size_x / 2,
        position[0] + resolution * size_x / 2,
        position[1] - resolution * size_y / 2,
        position[1] + resolution * size_y / 2
    )
    gridmap_gen(bpy_nh, name, heights, bounds)


if __name__ == "<run_path>":
    # 示例用法
    grid_length = 5
    grid_width = 5
    # heights = [
    #     [0.0, 0.1, 0.2, 0.3, 0.4],
    #     [0.1, 0.2, 0.3, 0.4, 0.5],
    #     [0.2, 0.3, 0.4, 0.5, 0.6],
    #     [0.3, 0.4, 0.5, 0.6, 0.7],
    #     [0.4, 0.5, 0.6, 0.7, 0.8]
    # ]
    # heights = img2heightmat(os.path.join(ROOT_DIR, "eg_data", "terrain_ground.png"), (0, 1))
    # gridmap_gen(bpy, "test_grid", heights)
    
    gridmap_gen_from_img(bpy, "test_grid",
                         os.path.join(ROOT_DIR, "eg_data", "terrain_ground.png"),
                         (0, 0), 0.05, (0, 1))
