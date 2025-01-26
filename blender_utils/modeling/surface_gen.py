'''
Author: MasterYip 2205929492@qq.com
Date: 2024-03-11 10:36:36
Description: Generate surface with border points
FilePath: /blender_utils/blender_utils/modeling/surface_gen.py
LastEditTime: 2025-01-26 21:29:03
LastEditors: MasterYip
'''


# context.area: VIEW_3D
import bpy
import math

# 清空场景
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# 定义函数来计算高度


def height_function(x, y):
    return math.sin(x) * math.cos(y)


# 设置网格的尺寸和分辨率
size_x = 5
size_y = 5
resolution_x = 10
resolution_y = 10

# 生成网格顶点
verts = []
for i in range(resolution_x + 1):
    for j in range(resolution_y + 1):
        x = size_x * (i / resolution_x - 0.5)
        y = size_y * (j / resolution_y - 0.5)
        z = height_function(x, y)
        verts.append((x, y, z))

# 创建网格对象并添加网格数据
mesh = bpy.data.meshes.new("Grid")
mesh.from_pydata(verts, [], [])

# 创建网格对象并添加到场景
obj = bpy.data.objects.new("Grid", mesh)
bpy.context.collection.objects.link(obj)

# 更新场景
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.edge_face_add()
bpy.ops.object.mode_set(mode='OBJECT')
