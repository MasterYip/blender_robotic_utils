'''
Author: GitHub Copilot
Date: 2025-05-05
Description: Examples for using the RobotAnimator to animate robots in Blender
FilePath: /blender_utils/examples/animation/robot_animator_examples.py
'''

import os
import sys
# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()

# Add parent directories to path to ensure imports work properly
parent_dir = os.path.abspath(os.path.join(ROOT_DIR, '..', '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import bpy
import yaml
import math
import csv
from blender_utils.animation.robot_animator import RobotAnimator, RobotAnimatorConfig, SwingTrajAnimator
from blender_utils.animation.robot_animator import read_csv_joint_states, read_csv_swingtraj


def example_robot_joint_animation():
    """Example of animating a robot using joint states from a CSV file"""
    # This example assumes you have a robot armature already loaded in the scene
    
    # Load configuration
    config_file = os.path.join(ROOT_DIR, '..', 'blender_utils', 'animation', 'robot_animator_cfg.yaml')
    config = RobotAnimatorConfig(config_file)
    
    # Create the robot animator
    animator = RobotAnimator(config)
    
    # Load joint states from CSV file
    joint_states_file = os.path.join(ROOT_DIR, '..', 'blender_utils', 'animation', 'joint_states.csv')
    animator.load_animation(joint_states_file)
    
    print("Robot joint animation loaded successfully.")


def example_robot_pose_and_joint_animation():
    """Example of animating both robot pose and joint states"""
    # This example assumes you have a robot armature already loaded in the scene
    
    # Load configuration
    config_file = os.path.join(ROOT_DIR, '..', 'blender_utils', 'animation', 'robot_animator_cfg.yaml')
    config = RobotAnimatorConfig(config_file)
    
    # Create the robot animator
    animator = RobotAnimator(config)
    
    # Set the interpolation type (optional)
    animator.set_interp_type('LINEAR')  # Options: 'CONSTANT', 'LINEAR', 'BEZIER'
    
    # Load joint states from CSV file with pose data (requires 24 columns in CSV)
    joint_states_file = os.path.join(ROOT_DIR, '..', 'blender_utils', 'animation', 'data', 'joint_states_flt_pose_joint.csv')
    animator.load_animation(joint_states_file)
    
    print("Robot pose and joint animation loaded successfully.")


def example_swing_trajectory_animation():
    """Example of visualizing swing trajectories"""
    # This example visualizes trajectories as animated curves
    
    # Load swing trajectory from CSV file
    traj_file = os.path.join(ROOT_DIR, '..', 'blender_utils', 'animation', 'swing_traj.csv')
    
    # Create the swing trajectory animator
    animator = SwingTrajAnimator(traj_file)
    
    print("Swing trajectory animation loaded successfully.")


def read_and_process_joint_states_example():
    """Example of reading and processing joint states from a CSV file directly"""
    # Load joint states from CSV file
    joint_states_file = os.path.join(ROOT_DIR, '..', 'blender_utils', 'animation', 'joint_states.csv')
    times, joint_states = read_csv_joint_states(joint_states_file)
    
    # Process the joint states (print first few entries)
    print(f"Loaded {len(times)} frames of joint data")
    print(f"Time range: {min(times)} to {max(times)} seconds")
    print(f"First frame joint values: {joint_states[0]}")


def read_and_process_swing_trajectory_example():
    """Example of reading and processing swing trajectories from a CSV file directly"""
    # Load swing trajectory from CSV file
    traj_file = os.path.join(ROOT_DIR, '..', 'blender_utils', 'animation', 'swing_traj.csv')
    times, trajectories = read_csv_swingtraj(traj_file)
    
    # Process the trajectory data (print first few entries)
    print(f"Loaded {len(times)} frames of trajectory data")
    print(f"Time range: {min(times)} to {max(times)} seconds")
    print(f"First trajectory point coordinates: {trajectories[0]}")


if __name__ == "__main__":
    # Uncomment the example you want to run
    
    # Note: These examples require a robot armature to be already loaded in the scene
    # example_robot_joint_animation()
    # example_robot_pose_and_joint_animation()
    
    # This example creates visualization curves in the scene
    example_swing_trajectory_animation()
    
    # These examples just read and process the data without modifying the scene
    # read_and_process_joint_states_example()
    # read_and_process_swing_trajectory_example()