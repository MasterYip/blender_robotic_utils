'''
Author: GitHub Copilot
Date: 2025-05-12
Description: Example of visualizing probabilistic robot trajectories with diffusion effects
FilePath: /blender_utils/examples/modeling/probabilistic/prob_robot_example.py
'''

import os
import sys
import numpy as np
import random
import math

# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()

# Add parent directories to path to ensure imports work properly
parent_dir = os.path.abspath(os.path.join(ROOT_DIR, '..', '..', '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import bpy
import mathutils
from blender_utils.animation.robot_animator import RobotAnimator, RobotAnimatorConfig, read_csv_joint_states
from blender_utils.rendering.rendering import principled_bsdf_material, link_material_to_obj


class ProbabilisticRobotAnimator:
    """Class for creating probabilistic robot trajectory visualizations with diffusion effects"""

    def __init__(self, config_path, joint_states_file=None, num_instances=10, diffusion_scale=0.05):
        """
        Initialize the probabilistic robot animator

        Args:
            config_path (str): Path to robot animator config YAML
            joint_states_file (str, optional): Path to joint states CSV
            num_instances (int, optional): Number of robot instances to create
            diffusion_scale (float, optional): Scale factor for position/rotation variations
        """
        self.config_path = config_path
        self.joint_states_file = joint_states_file
        self.num_instances = num_instances
        self.diffusion_scale = diffusion_scale
        self.frame_to_visualize = 1  # Default frame to visualize

        # Load the original robot animator configuration
        self.config = RobotAnimatorConfig(config_path)
        self.original_armature_name = self.config['armature_name']

        # Store the created robot instances
        self.robot_instances = []

        # Store joint states if provided
        if joint_states_file:
            self.times, self.joint_states = read_csv_joint_states(joint_states_file)

    def set_visualization_frame(self, frame):
        """Set which frame to visualize from the animation"""
        self.frame_to_visualize = frame

    def duplicate_robot(self, instance_index):
        """
        Duplicate the original robot armature

        Args:
            instance_index (int): Index of the robot instance

        Returns:
            bpy.types.Object: The duplicated armature object
        """
        # Get the original armature
        original = bpy.data.objects.get(self.original_armature_name)
        if not original:
            raise ValueError(f"Original armature '{self.original_armature_name}' not found")

        # Create a duplicate of the armature without using operators
        duplicated = original.copy()
        duplicated.data = original.data.copy()
        duplicated.animation_data_clear()  # Clear animation data to avoid conflicts
        duplicated.name = f"{self.original_armature_name}_prob_{instance_index}"

        # Copy children (meshes, etc.)
        for child in original.children:
            child_copy = child.copy()
            child_copy.data = child.data.copy()
            child_copy.parent = duplicated
            child_copy.matrix_parent_inverse = child.matrix_parent_inverse.copy()
            bpy.context.scene.collection.objects.link(child_copy)

        # Link the new object to the scene collection
        bpy.context.scene.collection.objects.link(duplicated)

        return duplicated

    def apply_probabilistic_variation(self, armature, instance_index):
        """
        Apply probabilistic variation to the robot's position and rotation

        Args:
            armature (bpy.types.Object): The armature to modify
            instance_index (int): Index of the robot instance
        """
        # Calculate variation based on instance index
        # Instances further from 0 will have more variation
        variation_factor = (instance_index + 1) / self.num_instances

        # Apply random variation to position
        pos_variation = self.diffusion_scale * variation_factor
        armature.location.x += random.uniform(-pos_variation, pos_variation)
        armature.location.y += random.uniform(-pos_variation, pos_variation)
        armature.location.z += random.uniform(-pos_variation, pos_variation)

        # Apply random variation to rotation
        rot_variation = self.diffusion_scale * variation_factor * math.pi / 8  # Max ~22.5 degrees
        armature.rotation_euler.x += random.uniform(-rot_variation, rot_variation)
        armature.rotation_euler.y += random.uniform(-rot_variation, rot_variation)
        armature.rotation_euler.z += random.uniform(-rot_variation, rot_variation)

    def apply_transparency(self, armature, instance_index):
        """
        Apply transparency based on instance index

        Args:
            armature (bpy.types.Object): The armature to modify
            instance_index (int): Index of the robot instance
        """
        # Calculate transparency based on instance index
        # Higher indices will be more transparent
        alpha = 1.0 - ((instance_index + 1) / (self.num_instances + 1))

        # Go through all objects in the armature's hierarchy
        for obj in armature.children_recursive:
            if obj.type == 'MESH':
                # Create transparent material
                material = principled_bsdf_material(
                    name=f"Prob_Material_{instance_index}",
                    base_color=(0.7, 0.7, 0.8, alpha),  # Blueish color with alpha
                    metallic=0.3,
                    roughness=0.4,
                    emission_color=(0.3, 0.3, 0.5, alpha),
                    emission_strength=0.5 * alpha  # Glow fades with transparency
                )

                # Enable transparency for the material
                material.blend_method = 'BLEND'

                # Apply the material to the object
                link_material_to_obj(obj, material)

    def apply_joint_state(self, armature, joint_states):
        """
        Apply joint states to the given armature

        Args:
            armature (bpy.types.Object): The armature to modify
            joint_states (list): Joint state values
        """
        # Ensure the armature has animation data
        if not armature.animation_data:
            armature.animation_data_create()

        if not armature.animation_data.action:
            armature.animation_data.action = bpy.data.actions.new(name=f"{armature.name}_Action")

        # Create a custom config for this armature instance
        instance_config = RobotAnimatorConfig(self.config_path)
        instance_config['armature_name'] = armature.name

        # Create animator for this instance and apply the joint state
        animator = RobotAnimator(instance_config)

        # Apply joint rotation directly to the armature's pose bones
        animator.set_joint_keyframe(1, joint_states)

        # Make sure animation is updated in the viewport
        bpy.context.view_layer.update()

    def set_pose_keyframe(self, armature, pose, frame=1):
        """
        Apply pose (position and rotation) keyframes to the given armature

        Args:
            armature (bpy.types.Object): The armature to modify
            pose (list): Pose values [x, y, z, roll, pitch, yaw]
            frame (int): The frame to set the keyframe
        """
        # Ensure the armature has animation data
        if not armature.animation_data:
            armature.animation_data_create()

        if not armature.animation_data.action:
            armature.animation_data.action = bpy.data.actions.new(name=f"{armature.name}_Action")

        # Apply the position and rotation
        armature.location = pose[:3]
        armature.rotation_euler = pose[3:]

        # Set keyframes
        armature.keyframe_insert(data_path="location", frame=frame)
        armature.keyframe_insert(data_path="rotation_euler", frame=frame)

    def create_probabilistic_animation(self):
        """
        Create the probabilistic animation visualization
        """
        # Clear existing instances
        self.robot_instances = []

        # Create collection for probabilistic robots if it doesn't exist
        if "ProbabilisticRobots" not in bpy.data.collections:
            prob_collection = bpy.data.collections.new("ProbabilisticRobots")
            bpy.context.scene.collection.children.link(prob_collection)
        else:
            prob_collection = bpy.data.collections["ProbabilisticRobots"]

        # Get joint state for the frame to visualize if available
        target_joint_state = None
        target_pose = None

        if hasattr(self, 'joint_states'):
            frame_idx = min(self.frame_to_visualize, len(self.joint_states) - 1)

            # Check if we have full pose+joint data (24 values) or just joint data (18 values)
            if len(self.joint_states[frame_idx]) == 24:
                # We have both pose and joint data
                target_pose = self.joint_states[frame_idx][:6]
                target_joint_state = self.joint_states[frame_idx][6:]
            else:
                # We only have joint data
                target_joint_state = self.joint_states[frame_idx]

        # Create robot instances with increasing diffusion/transparency
        for i in range(self.num_instances):
            # Duplicate the robot
            robot_instance = self.duplicate_robot(i)

            # Apply probabilistic variation to position and rotation via set_pose_keyframe
            # if we have target pose data
            if target_pose:
                # Create varied pose based on diffusion
                varied_pose = []
                variation_factor = (i + 1) / self.num_instances * self.diffusion_scale

                # Position variation (x, y, z)
                for j in range(3):
                    # Add more variation to position (scaling by 3 to make it more visible)
                    pos_var = random.uniform(-variation_factor * 3, variation_factor * 3)
                    varied_pose.append(target_pose[j] + pos_var)

                # Rotation variation (roll, pitch, yaw)
                for j in range(3, 6):
                    # Add rotation variation in radians
                    rot_var = random.uniform(-variation_factor * 0.5, variation_factor * 0.5)
                    varied_pose.append(target_pose[j] + rot_var)

                # Apply the varied pose
                self.set_pose_keyframe(robot_instance, varied_pose)
            else:
                # If no pose data, just apply random positional variation directly
                self.apply_probabilistic_variation(robot_instance, i)

            # Apply transparency based on instance index
            self.apply_transparency(robot_instance, i)

            # Apply joint state if available
            if target_joint_state:
                # Apply some random variation to the joint state for probabilistic effect
                varied_joint_state = []
                variation_factor = (i + 1) / self.num_instances * self.diffusion_scale * 10

                for state in target_joint_state:
                    # Add random variation to joint angle
                    varied_state = state + random.uniform(-variation_factor, variation_factor)
                    varied_joint_state.append(varied_state)

                self.apply_joint_state(robot_instance, varied_joint_state)

            # Move to probabilistic robots collection - using direct collection management
            # First, unlink from any current collections
            for collection in list(robot_instance.users_collection):
                collection.objects.unlink(robot_instance)
            # Then link to our probability collection
            prob_collection.objects.link(robot_instance)

            # Also handle children objects (meshes, etc.)
            for child in robot_instance.children_recursive:
                for collection in list(child.users_collection):
                    collection.objects.unlink(child)
                prob_collection.objects.link(child)

            # Store the instance
            self.robot_instances.append(robot_instance)

        print(f"Created {self.num_instances} probabilistic robot instances")


def create_probabilistic_robot_visualization(config_file, joint_states_file=None, num_instances=15, diffusion_scale=0.1, frame=1):
    """
    Create a probabilistic robot visualization

    Args:
        config_file (str): Path to robot animator config YAML
        joint_states_file (str, optional): Path to joint states CSV
        num_instances (int): Number of robot instances to create
        diffusion_scale (float): Scale factor for position/rotation variations
        frame (int): Animation frame to visualize
    """
    # Create the probabilistic animator
    prob_animator = ProbabilisticRobotAnimator(
        config_file,
        joint_states_file=joint_states_file,
        num_instances=num_instances,
        diffusion_scale=diffusion_scale
    )

    # Set which frame to visualize
    prob_animator.set_visualization_frame(frame)

    # Create the probabilistic animation
    prob_animator.create_probabilistic_animation()

    return prob_animator


if __name__ == "<run_path>":
    # Example usage
    # This example assumes you have already imported a robot model
    # and set up the armature named in your config file

    # Path to the configuration file
    config_file = os.path.join(ROOT_DIR, '..', '..', 'animation', 'elspider_air_walk', 'robot_animator_cfg.yaml')

    # Path to joint states file (optional)
    joint_states_file = os.path.join(ROOT_DIR, '..', '..', 'animation', 'elspider_air_walk', 'joint_states.csv')

    num_frame = 50
    delta_frame = 10
    # diffusion_scales = [0.05 * i for i in range(1, num_frame)]  # Example diffusion scales
    diffusion_scales = [0] * num_frame
    diffusion_frames = [800 + delta_frame * i for i in range(1, num_frame)]  # Example frames
    # diffusion_instances = [i for i in range(1, num_frame)]  # Example number of instances
    diffusion_instances = [1] * num_frame

    for scale, frame, instances in zip(diffusion_scales, diffusion_frames, diffusion_instances):
        # Create the probabilistic robot visualization
        animator = create_probabilistic_robot_visualization(
            config_file,
            joint_states_file=joint_states_file,
            num_instances=instances,  # Number of robot instances
            diffusion_scale=scale,  # Scale factor for variations
            frame=frame  # Animation frame to visualize
        )

    # # Create the probabilistic visualization
    # animator = create_probabilistic_robot_visualization(
    #     config_file,
    #     joint_states_file=joint_states_file,
    #     num_instances=20,  # Number of robot instances
    #     diffusion_scale=0.2,  # Scale factor for variations
    #     frame=1600  # Animation frame to visualize
    # )

    print("Probabilistic robot diffusion visualization created successfully!")
