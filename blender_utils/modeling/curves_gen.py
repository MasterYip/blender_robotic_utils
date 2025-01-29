'''
Author: MasterYip 2205929492@qq.com
Date: 2025-01-28 15:41:04
Description: file content
FilePath: /blender_utils/blender_utils/modeling/curves_gen.py
LastEditTime: 2025-01-28 21:26:50
LastEditors: MasterYip
'''

import bpy
from blender_utils.utils.utils import link_obj_to_collection


def create_curve(ctrl_pts, name="DefaultCurve", collection_name="Curves",
                 type='NURBS', order=4, bevel_depth=0.1):
    crv = bpy.data.curves.new('curve', 'CURVE')
    crv.bevel_depth = bevel_depth
    crv.use_fill_caps = True
    crv.dimensions = '3D'
    spline = crv.splines.new(type=type)
    spline.points.add(len(ctrl_pts) - 1)
    for p, new_co in zip(spline.points, ctrl_pts):
        p.co = (list(new_co) + [1.0])
    spline.use_endpoint_u = True
    spline.use_endpoint_v = True
    spline.order_u = order

    # set the directroy of the curve
    obj = bpy.data.objects.new(name, crv)
    link_obj_to_collection(obj, collection_name)
    # bpy.context.collection.objects.link(obj)


if __name__ == "<run_path>":

    # 示例输入
    control_points = [(0, 0, 0), (1, 2, 0), (2, 0, 0), (3, 2, 0)]  # 控制点
    # 创建NURBS曲线
    create_curve(control_points, "saldf")
