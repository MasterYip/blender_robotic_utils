'''
Author: MasterYip 2205929492@qq.com
Date: 2024-03-11 10:26:37
Description: file content
FilePath: /blender_learning/modeling/gridmap_gen.py
LastEditTime: 2024-03-11 10:44:52
LastEditors: MasterYip
'''

import math


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


if __name__ == "__main__":
    # 示例用法
    grid_length = 5
    grid_width = 5
    heights = [
        [0.0, 0.1, 0.2, 0.3, 0.4],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.2, 0.3, 0.4, 0.5, 0.6],
        [0.3, 0.4, 0.5, 0.6, 0.7],
        [0.4, 0.5, 0.6, 0.7, 0.8]
    ]

    gridmap_gen(heights)
