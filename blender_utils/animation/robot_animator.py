'''
Author: MasterYip 2205929492@qq.com
Date: 2025-01-24 15:35:33
Description: Animate robot in blender from recorded joint states
FilePath: /blender_utils/blender_utils/animation/robot_animator.py
LastEditTime: 2025-01-24 16:32:58
LastEditors: MasterYip
'''

import os
from shlex import join
import yaml
import bpy
import mathutils
import math
import csv

# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()

# def csv2dict(filename):
#     # ignore spaces
#     df = pd.read_csv(filename, sep=",", skipinitialspace=True)
#     return df.to_dict(orient="list")


def read_csv_joint_states(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        joint_states = list(reader)[1:]
        times = [float(row[0]) for row in joint_states]
        joint_states = [row[1:] for row in joint_states]
        # convert to float degree
        return times, [[math.degrees(float(i)) for i in row] for row in joint_states]


class RobotAnimatorConfig(dict):
    """Config Class"""

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
            joint.keyframe_insert(data_path="rotation_quaternion", frame=frame)
            # joint.location = new_location
            # joint.scale = new_scale
            # pose_bone.keyframe_insert(data_path="location", frame=frame)
            # pose_bone.keyframe_insert(data_path="scale", frame=frame)

    def load_animation(self, joint_states_file):
        times, joint_states = read_csv_joint_states(joint_states_file)
        for time, state in zip(times, joint_states):
            frame = int((time + self.config["time_start"]) * self.config['frame_rate'])
            self.set_keyframe(frame, state)


if __name__ == "<run_path>":

    # Load configuration
    config = RobotAnimatorConfig(os.path.join(ROOT_DIR, 'robot_animator_cfg.yaml'))
    animator = RobotAnimator(config)

    # Load joint states
    file = os.path.join(ROOT_DIR, 'joint_states.csv')

    animator.load_animation(file)
    print("Keyframes set successfully.")
