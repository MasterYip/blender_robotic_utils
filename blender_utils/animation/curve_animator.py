'''
Author: MasterYip 2205929492@qq.com
Date: 2025-01-28 22:42:24
Description: file content
FilePath: /blender_utils/blender_utils/animation/curve_animator.py
LastEditTime: 2025-01-29 11:52:44
LastEditors: MasterYip
'''

from deprecated import deprecated
import bpy
from math import sin, cos


@deprecated("Please use 'set_curve_keyframe' instead")
def add_keyframes_to_curve(curve_obj, frame_start=1, frame_end=100):
    """
    为曲线的控制点添加关键帧
    :param curve_obj: 曲线对象
    :param frame_start: 起始帧
    :param frame_end: 结束帧
    """
    if curve_obj.type != 'CURVE':
        print("选中的对象不是曲线")
        return

    # 进入编辑模式并选择所有控制点
    bpy.context.view_layer.objects.active = curve_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.curve.select_all(action='SELECT')  # 选择所有控制点
    bpy.ops.object.mode_set(mode='OBJECT')  # 返回对象模式

    # 获取曲线的控制点
    spline = curve_obj.data.splines[0]  # 假设曲线只有一个样条线
    control_points = spline.points

    # 在第一帧设置初始位置
    bpy.context.scene.frame_set(frame_start)
    for point in control_points:
        point.keyframe_insert(data_path="co", index=-1)  # 插入位置关键帧

    # 在最后一帧调整控制点位置并插入关键帧
    bpy.context.scene.frame_set(frame_end)
    for point in control_points[2:]:
        point.co.x += 2.0  # 示例：沿X轴移动2个单位
        point.co.y += 1.0  # 示例：沿Y轴移动1个单位
        point.keyframe_insert(data_path="co", index=-1)  # 插入位置关键帧

    print(f"已为曲线 {curve_obj.name} 的控制点添加关键帧")


def set_curve_keyframe(curve, ctrl_points, frame):
    """
    为曲线的控制点设置关键帧
    :param curve: 曲线对象
    :param ctrl_points: 控制点坐标列表
    :param frame: 帧数
    """
    # 进入编辑模式并选择所有控制点
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.curve.select_all(action='SELECT')  # 选择所有控制点
    bpy.ops.object.mode_set(mode='OBJECT')  # 返回对象模式

    # 获取曲线的控制点
    spline = curve.data.splines[0]  # 假设曲线只有一个样条线
    control_points = spline.points

    # 在指定帧设置控制点位置
    bpy.context.scene.frame_set(frame)
    for point, new_co in zip(control_points, ctrl_points):
        point.co.x, point.co.y, point.co.z = new_co
        point.keyframe_insert(data_path="co", index=-1)  # 插入位置关键帧


if __name__ == "<run_path>":
    # 示例：为选中的曲线对象添加关键帧
    print("示例：为选中的曲线对象添加关键帧")
    if bpy.context.selected_objects:
        selected_obj = bpy.context.selected_objects[0]  # 获取选中的第一个对象
        # add_keyframes_to_curve(selected_obj, frame_start=1, frame_end=100)
        for frame in [10*i for i in range(1, 10)]:
            set_curve_keyframe(selected_obj, [(sin(0.1 * frame+i), cos(0.1 * frame+i), i) for i in range(4)], frame)
    else:
        print("请先选中一个曲线对象")
