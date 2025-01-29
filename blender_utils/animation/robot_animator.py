'''
Author: MasterYip 2205929492@qq.com
Date: 2025-01-24 15:35:33
Description: Animate robot in blender from recorded joint states
FilePath: /blender_utils/blender_utils/animation/robot_animator.py
LastEditTime: 2025-01-29 14:54:03
LastEditors: MasterYip
'''

import bpy
import os
import yaml
import mathutils
import math
import csv
from blender_utils.modeling.curves_gen import create_curve
from blender_utils.animation.curve_animator import set_curve_keyframe
from blender_utils.rendering.rendering import create_gradient_material_for_curve

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
        q = list(reader)[1:]
        times = [float(row[0]) for row in q]
        q = [row[1:] for row in q]
        if len(q[0]) == 18:
            # convert to float degree
            return times, [[math.degrees(float(i)) for i in row] for row in q]
        elif len(q[0]) == 24:
            # FIXME: Data unit conversion
            return times, [[math.degrees(float(i)) if idx > 5 else float(i)*100 for idx, i in enumerate(row)] for row in q]


def read_csv_swingtraj(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        traj = list(reader)[1:]
        times = [float(row[0]) for row in traj]
        traj = [row[1:] for row in traj]
        return times, [[float(i)*100 for i in row] for row in traj]


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
            raise ValueError(f"未找到骨架对象 '{self.config['armature_name']}' 或对象类型不是骨架。")

            # 获取骨架的动作数据
        self.action = self.armature.animation_data.action
        if self.action is None:
            raise ValueError("骨架没有动作数据。")

        # 获取特定骨骼的姿势对象
        self.joints = []
        for joint_name in self.config['joint_names']:
            pose_bone = self.armature.pose.bones.get(joint_name)
            if pose_bone is None:
                print(f"在骨架中未找到名为 '{joint_name}' 的骨骼。")
            self.joints.append(pose_bone)

    def set_interp_type(self, type='CONSTANT'):
        # FIXME: TypeError: couldn't access the py sequence
        # 设置关键帧的插值模式为'CONSTANT'
        for fcurve in self.action.fcurves:
            # if fcurve.data_path.startswith(f"pose.bones['{bone_name}']"):
            if fcurve.data_path.startswith("pose.bones"):
                fcurve.keyframe_points.foreach_set("interpolation", type)

    def set_joint_keyframe(self, frame, joint_states):
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

    def set_pose_keyframe(self, frame, pose):
        # pose:[x,y,z,r,p,y]
        # set root pose keyframe
        self.armature.location = pose[:3]
        self.armature.rotation_euler = pose[3:]
        self.armature.keyframe_insert(data_path="location", frame=frame)

    def load_animation(self, joint_states_file, decimation=10):
        times, joint_states = read_csv_joint_states(joint_states_file)
        if len(joint_states[0]) == 18:
            for time, state in zip(times[::decimation], joint_states[::decimation]):
                frame = int((time + self.config["time_start"]) * self.config['frame_rate'])
                self.set_joint_keyframe(frame, state)
        elif len(joint_states[0]) == 24:
            for time, state in zip(times[::decimation], joint_states[::decimation]):
                frame = int((time + self.config["time_start"]) * self.config['frame_rate'])
                self.set_joint_keyframe(frame, state[6:])
                self.set_pose_keyframe(frame, state[:6])


class SwingTrajAnimator(object):
    def __init__(self, traj_file) -> None:
        self.collection_name = "SwingTraj"
        self.trajname_prefix = "trajectory"
        self.traj_length = 30
        self.frame_rate = 30  # frame rate of the animation scene
        self.times, self.traj = read_csv_swingtraj(traj_file)
        self.init_swing_traj()
        self.load_animation()
        pass

    def init_swing_traj(self):
        for i in range(len(self.traj[0]) // 3):
            ctrl_points = [self.traj[0][3*i:3*(i+1)] for idx in range(self.traj_length)]
            # print(ctrl_points)
            create_curve(ctrl_points, f"{self.trajname_prefix}_{i}", self.collection_name, bevel_depth=1.0)

    def load_animation(self, decimation=10):
        time_buf = []
        traj_buf = []
        for time, traj in zip(self.times[::decimation], self.traj[::decimation]):
            time_buf.append(time)
            traj_buf.append(traj)
            if len(time_buf) < self.traj_length:
                # pad to traj_length using first traj
                time_buf = [self.times[0]] * (self.traj_length - len(time_buf)) + time_buf
                traj_buf = [self.traj[0]] * (self.traj_length - len(traj_buf)) + traj_buf
            while len(time_buf) > self.traj_length:
                time_buf.pop(0)
                traj_buf.pop(0)

            frame = int(time * self.frame_rate)
            for i in range(len(self.traj[0]) // 3):
                ctrl_points = [traj_buf[idx][3*i:3*(i+1)] for idx in range(self.traj_length)]
                curve = bpy.data.objects.get(f"{self.trajname_prefix}_{i}")
                set_curve_keyframe(curve, ctrl_points, frame)


if __name__ == "<run_path>":

    # # Load configuration
    # config = RobotAnimatorConfig(os.path.join(ROOT_DIR, 'robot_animator_cfg.yaml'))
    # animator = RobotAnimator(config)
    # # Load joint states
    # file = os.path.join(ROOT_DIR, 'joint_states.csv')
    # animator.load_animation(file)
    # print("Keyframes set successfully.")

    # Load swing trajectory
    traj_file = os.path.join(ROOT_DIR, 'swing_traj.csv')
    animator = SwingTrajAnimator(traj_file)
    print("Swing trajectory loaded successfully.")
