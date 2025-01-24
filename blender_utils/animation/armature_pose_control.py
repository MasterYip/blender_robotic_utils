import bpy
import mathutils
import math
# 设置骨架和骨骼名称
armature_name = "root"
bone_name = "LF_HFE.revolute.bone"

joints = ["RF_HAA.revolute.bone",
          "RF_HFE.revolute.bone",
          "RF_KFE.revolute.bone",
          "RM_HAA.revolute.bone",
          "RM_HFE.revolute.bone",
          "RM_KFE.revolute.bone",
          "RB_HAA.revolute.bone",
          "RB_HFE.revolute.bone",
          "RB_KFE.revolute.bone",
          "LF_HAA.revolute.bone",
          "LF_HFE.revolute.bone",
          "LF_KFE.revolute.bone",
          "LM_HAA.revolute.bone",
          "LM_HFE.revolute.bone",
          "LM_KFE.revolute.bone",
          "LB_HAA.revolute.bone",
          "LB_HFE.revolute.bone",
          "LB_KFE.revolute.bone",]

# # 进入姿势模式
# armature = bpy.data.objects.get(armature_name)
# if armature:
#     bpy.context.view_layer.objects.active = armature
#     bpy.ops.object.mode_set(mode='POSE')

#     # 设置骨骼旋转
#     # print all bone names
#     # for bone in armature.pose.bones:
#     #     print(bone.name)
#     bone = armature.pose.bones.get(joints[3])
#     if bone:
#         bone.rotation_euler.x = math.radians(0)  # 绕 X 轴旋转 60 度
#         print(f"已设置 {bone_name} 的角度。")
#     else:
#         print(f"未找到骨骼 {bone_name}！")
# else:
#     print(f"未找到骨架 {armature_name}！")
# bpy.context.view_layer.update()


def modify_bone_transformations(armature_name, bone_name, rotation_axes, angles_degrees, new_location, new_scale, frame_start, frame_end):
    """
    修改骨架中特定骨骼的变换，包括沿不同轴的旋转、位置和缩放。
    参数:
    armature_name -- 骨架对象的名称
    bone_name -- 骨骼的名称
    rotation_axes -- 一个包含三个向量的对象，分别对应X、Y、Z轴的旋转轴
    angles_degrees -- 与rotation_axes对应的旋转角度
    new_location -- 新位置的 Vector 对象
    new_scale -- 新缩放的 Vector 对象
    frame_start -- 起始帧
    frame_end -- 结束帧
    """
    # 获取骨架对象
    armature = bpy.data.objects.get(armature_name)
    if armature is None or armature.type != 'ARMATURE':
        print(f"未找到骨架对象 '{armature_name}' 或对象类型不是骨架。")
        return

    # 获取骨架的动作数据
    action = armature.animation_data.action
    if action is None:
        print("骨架没有动作数据。")
        return

    # 获取特定骨骼的姿势对象
    pose_bone = armature.pose.bones.get(bone_name)
    if pose_bone is None:
        print(f"在骨架中未找到名为 '{bone_name}' 的骨骼。")
        return

    # 遍历指定的帧范围
    # for frame in range(frame_start, frame_end + 1):
    for frame in [frame_start, frame_end]:
        progress = (frame - frame_start) / (frame_end - frame_start)
        angle_now = [angle * progress for angle in angles_degrees]
        # 初始化总的四元数为单位四元数（无旋转）
        total_rotation_quat = mathutils.Quaternion((1, 0, 0, 0))

        # 为每个轴的旋转创建四元数并累加
        for axis, angle in zip(rotation_axes, angle_now):
            if angle != 0:
                # 将角度转换为弧度并创建四元数
                rotation_quat = mathutils.Quaternion(axis, math.radians(angle))
                # 将新旋转应用到总的四元数上
                total_rotation_quat = total_rotation_quat @ rotation_quat

        # 设置骨骼的变换
        pose_bone.rotation_quaternion = total_rotation_quat
        pose_bone.location = new_location
        pose_bone.scale = new_scale

        # 插入关键帧
        pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)
        pose_bone.keyframe_insert(data_path="location", frame=frame)
        pose_bone.keyframe_insert(data_path="scale", frame=frame)

    # 设置关键帧的插值模式为'CONSTANT'
    for fcurve in action.fcurves:
        if fcurve.data_path.startswith(f"pose.bones['{bone_name}']"):
            fcurve.keyframe_points.foreach_set("interpolation", 'CONSTANT')

    print(f"骨骼 '{bone_name}' 的变换已从帧 {frame_start} 到 {frame_end} 更新。")


# 示例使用
# armature_name = "Armature"
# bone_name = "mixamorig:Hips"
rotation_axes = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]  # 分别绕X、Y、Z轴
angles_degrees = [0, 50, 0]  # 分别对应上面的轴的旋转角度
new_location = mathutils.Vector((0, 0, 0))
new_scale = mathutils.Vector((1, 1, 1))
frame_start = 1
frame_end = 60

# 调用函数修改骨骼的变换
modify_bone_transformations(armature_name, bone_name,
                            rotation_axes, angles_degrees,
                            new_location, new_scale, frame_start, frame_end)

# 提示用户检查Blender中的更改
print("请检查Blender查看更改。")
