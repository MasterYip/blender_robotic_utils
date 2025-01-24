'''
Author: MasterYip 2205929492@qq.com
Date: 2025-01-24 15:35:33
Description: Animate robot in blender from recorded joint states
FilePath: /blender_utils/blender_utils/animation/robot_animator.py
LastEditTime: 2025-01-24 16:02:29
LastEditors: MasterYip
'''

import os
import yaml
import bpy
import mathutils
import math

# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()

# Config Class


class RobotAnimatorConfig(dict):
    def __init__(self, yaml_path):
        with open(yaml_path, 'r') as file:
            prime_service = yaml.safe_load(file)
            self.update(prime_service)
        pass


class RobotAnimator(object):
    def __init__(self, config: RobotAnimatorConfig):
        self.config = config

        # 获取骨架对象
        self.armature = bpy.data.objects.get(self.config['armature_name'])
        if self.armature is None or self.armature.type != 'ARMATURE':
            print(f"未找到骨架对象 '{self.config['armature_name']}' 或对象类型不是骨架。")

        # 获取骨架的动作数据
        action = self.armature.animation_data.action
        if action is None:
            print("骨架没有动作数据。")

        # 获取特定骨骼的姿势对象
        self.joints = []
        for joint_name in self.config['joint_names']:
            pose_bone = self.armature.pose.bones.get(joint_name)
            if pose_bone is None:
                print(f"在骨架中未找到名为 '{joint_name}' 的骨骼。")
            self.joints.append(pose_bone)

    def set_keyframe(self, frame, joint_states):
        for joint, state in zip(self.joints, joint_states):
            # Euler
            # state = [0, 0, state]
            # joint.rotation_euler = mathutils.Euler(state)
            # joint.keyframe_insert(data_path='rotation_euler', frame=frame)

            # Quat
            total_rotation_quat = mathutils.Quaternion((1, 0, 0, 0))
            rotation_axes = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]  # 分别绕X、Y、Z轴
            angles = [0, state, 0]  # 分别对应上面的轴的旋转角度
            for axis, angle in zip(rotation_axes, angles):
                if angle != 0:
                    # 将角度转换为弧度并创建四元数
                    rotation_quat = mathutils.Quaternion(axis, math.radians(angle))
                    # 将新旋转应用到总的四元数上
                    total_rotation_quat = total_rotation_quat @ rotation_quat
            joint.rotation_quaternion = total_rotation_quat
            # joint.location = new_location
            # joint.scale = new_scale
            joint.keyframe_insert(data_path="rotation_quaternion", frame=frame)
            # pose_bone.keyframe_insert(data_path="location", frame=frame)
            # pose_bone.keyframe_insert(data_path="scale", frame=frame)

if __name__ == "<run_path>":

    # Load configuration
    config = RobotAnimatorConfig(os.path.join(ROOT_DIR, 'robot_animator_cfg.yaml'))
    animator = RobotAnimator(config)

    joint_states = [[i for _ in range(18)] for i in range(40)]

    # Set keyframes
    animator.set_keyframe(10, joint_states[0])
    animator.set_keyframe(50, joint_states[-1])
    print("Keyframes set successfully.")
