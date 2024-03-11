'''
Author: MasterYip 2205929492@qq.com
Date: 2024-03-11 11:18:56
Description: file content
FilePath: /blender_learning/blender_utils/modeling/polygon_gen.py
LastEditTime: 2024-03-11 13:02:04
LastEditors: MasterYip
'''

import bmesh
import numpy as np
from math import pi, sin, cos


def ellipsoid_gen(bpy, name="Ellipsoid", axes=(1.0, 1.0, 1.0), segments=32, pos=(0, 0, 0)):

    # 创建一个空的Mesh对象和一个空的Object对象
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)

    # 设置位置并添加到场景中
    # obj.location = bpy.context.scene.cursor.location
    obj.location = pos
    bpy.context.collection.objects.link(obj)

    # 生成椭球的顶点
    bm = bmesh.new()
    for u in range(segments + 1):
        theta = u / segments * 2 * pi
        for v in range(segments // 2 + 1):
            phi = v / (segments // 2) * pi
            x = axes[0] * sin(phi) * cos(theta)
            y = axes[1] * sin(phi) * sin(theta)
            z = axes[2] * cos(phi)
            bm.verts.new((x, y, z))

    # 创建椭球的面
    for u in range(segments):
        for v in range(segments // 2):
            v1 = u * (segments // 2 + 1) + v
            v2 = v1 + 1
            v3 = (u + 1) * (segments // 2 + 1) + v + 1
            v4 = v3 - 1
            bm.faces.new(bm.verts[v1:v1+1] + bm.verts[v2:v2+1] +
                         bm.verts[v3:v3+1] + bm.verts[v4:v4+1])


    # 更新网格
    bm.to_mesh(mesh)
    bm.free()
