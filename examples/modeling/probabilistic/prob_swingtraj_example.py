'''
Author: GitHub Copilot
Date: 2025-05-12
Description: Flow-based visualization for probabilistic robot trajectories with diffusion effects
FilePath: /blender_utils/examples/modeling/probabilistic/prob_swingtraj_example.py
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
from blender_utils.animation.robot_animator import RobotAnimatorConfig, read_csv_joint_states, read_csv_swingtraj
from blender_utils.modeling.curves_gen import create_curve
from blender_utils.rendering.rendering import principled_bsdf_material, link_material_to_obj, create_gradient_material_for_curve


class FlowDiffusionVisualizer:
    """Class for creating flow-based probabilistic visualization with diffusion effects"""

    def __init__(self, joint_states_file=None, num_streams=30, diffusion_scale=0.05, diffusion_time_map=None):
        """
        Initialize the flow diffusion visualizer

        Args:
            joint_states_file (str, optional): Path to joint states CSV
            num_streams (int, optional): Number of flow streams to create
            diffusion_scale (float, optional): Base scale factor for position variations
            diffusion_time_map (callable, optional): Function that maps time progress (0 to 1) to diffusion scale
        """
        self.joint_states_file = joint_states_file
        self.num_streams = num_streams
        self.diffusion_scale = diffusion_scale
        self.frame_rate = 30
        self.collection_name = "ProbabilisticFlows"

        # Set the diffusion time mapping function
        if diffusion_time_map is None:
            # Default linear mapping - diffusion increases linearly with time
            self.diffusion_time_map = lambda t: t * self.diffusion_scale
        else:
            self.diffusion_time_map = diffusion_time_map

        # Load joint states if provided
        if joint_states_file:
            self.times, self.joint_states = read_csv_joint_states(joint_states_file)

    def add_time_based_noise_to_trajectory(self, traj_data, base_noise_level):
        """
        Add time-based Gaussian noise to a trajectory to simulate diffusion

        Args:
            traj_data (list): Original trajectory data points
            base_noise_level (float): Base level of noise

        Returns:
            list: Trajectory with added noise that increases with time
        """
        noisy_traj = []

        # Add time-based noise to each point
        for i, point in enumerate(traj_data):
            # Calculate time progress (0 at start, 1 at end)
            time_progress = i / (len(traj_data) - 1) if len(traj_data) > 1 else 0

            # Apply the diffusion time mapping function to get time-dependent noise level
            noise_level = self.diffusion_time_map(time_progress) * base_noise_level

            # Add noise to each coordinate
            noisy_point = [p + random.gauss(0, noise_level) for p in point]
            noisy_traj.append(noisy_point)

        return noisy_traj

    def generate_flow_trajectory(self, trajectory_points):
        """
        Generate a flow trajectory visualization with diffusion

        Args:
            trajectory_points (list): List of trajectory points [x, y, z]
        """
        # Make sure we have a collection for our flows
        if self.collection_name not in bpy.data.collections:
            flow_collection = bpy.data.collections.new(self.collection_name)
            bpy.context.scene.collection.children.link(flow_collection)
        else:
            flow_collection = bpy.data.collections[self.collection_name]

        # Create multiple flow streams with varying diffusion
        for i in range(self.num_streams):
            # Calculate normalized stream index (0 to 1)
            norm_index = i / (self.num_streams - 1) if self.num_streams > 1 else 0

            # Base noise level varies by stream index, but time variation is handled in add_time_based_noise
            base_noise_level = norm_index + 0.05  # Add small offset to ensure even the central path has some noise

            # Create noisy trajectory with time-based diffusion
            noisy_trajectory = self.add_time_based_noise_to_trajectory(trajectory_points, base_noise_level)

            # Create curve for this flow stream
            curve_name = f"flow_stream_{i}"

            # Adjust bevel depth based on stream index (central streams are thicker)
            bevel_depth = 0.3 * (1 - norm_index * 0.7) + 0.1

            # Create the curve
            create_curve(noisy_trajectory, curve_name, self.collection_name, bevel_depth=bevel_depth)

            # Get the curve object we just created
            curve_obj = bpy.data.objects.get(curve_name)

            if curve_obj:
                # Calculate alpha based on stream index (central streams are more opaque)
                alpha = 1.0 - norm_index * 0.85

                # Make diffused flows more transparent
                material = principled_bsdf_material(
                    name=f"Flow_Material_{i}",
                    base_color=(0.3, 0.6, 0.9, alpha),
                    metallic=0.0,
                    roughness=0.3,
                    emission_color=(0.2, 0.4, 0.8, alpha),
                    emission_strength=1.0 * alpha
                )

                # Enable transparency
                material.blend_method = 'BLEND'

                # Apply material to curve
                link_material_to_obj(curve_obj, material)
            else:
                print(f"Warning: Could not find curve object {curve_name} after creation")

    def visualize_joint_trajectory(self, joint_index, start_frame=0, end_frame=None):
        """
        Visualize the trajectory of a specific joint with diffusion

        Args:
            joint_index (int): Index of the joint to visualize
            start_frame (int, optional): Starting frame index
            end_frame (int, optional): Ending frame index
        """
        if not hasattr(self, 'joint_states'):
            print("No joint states loaded")
            return

        # Limit the end frame if necessary
        if end_frame is None:
            end_frame = len(self.joint_states) - 1
        else:
            end_frame = min(end_frame, len(self.joint_states) - 1)

        # Extract trajectory points for the specified joint
        trajectory_points = []

        # Check if we have pose data (24 values) or just joint data (18 values)
        is_pose_data = len(self.joint_states[0]) == 24

        if is_pose_data:
            # For pose data, use robot base position + joint positions
            for frame in range(start_frame, end_frame + 1):
                # Extract robot base position
                base_pos = self.joint_states[frame][:3]

                # Extract joint angle - simplified approach, assuming Z-axis rotation
                joint_angle = math.radians(self.joint_states[frame][6 + joint_index])

                # Simplified joint position calculation (adjust based on your robot model)
                joint_offset = [0.5 * math.cos(joint_angle), 0.5 * math.sin(joint_angle), 0.2]

                # Combine base position and joint position
                joint_pos = [base_pos[0] + joint_offset[0],
                             base_pos[1] + joint_offset[1],
                             base_pos[2] + joint_offset[2]]

                trajectory_points.append(joint_pos)
        else:
            # For joint-only data, create abstract visualization based on joint angles
            for frame in range(start_frame, end_frame + 1):
                # Use joint angle to create a spiral-like trajectory for visualization
                angle = math.radians(self.joint_states[frame][joint_index])
                x = frame * 0.1 * math.cos(angle)
                y = frame * 0.1 * math.sin(angle)
                z = frame * 0.05

                trajectory_points.append([x, y, z])

        # Generate the flow visualization
        self.generate_flow_trajectory(trajectory_points)

    def visualize_end_effector(self, limb_indices, time_start=0, time_end=None, num_frames=100):
        """
        Visualize the end effector trajectory for specific limbs

        Args:
            limb_indices (list or int): Index or indices of the limb/leg to visualize (0-5 for hexapod)
            time_start (float): Starting time in seconds
            time_end (float): Ending time in seconds
            num_frames (int): Number of frames to visualize
        """
        # Handle single limb index case
        if isinstance(limb_indices, int):
            limb_indices = [limb_indices]

        # Load trajectory data
        traj_file = os.path.join(ROOT_DIR, '..', '..', 'animation', 'elspider_air_walk', 'swing_traj.csv')
        times, trajectories = read_csv_swingtraj(traj_file)

        # Find start and end indices based on time
        if time_end is None:
            time_end = times[-1]

        start_idx = 0
        while start_idx < len(times) and times[start_idx] < time_start:
            start_idx += 1

        end_idx = len(times) - 1
        while end_idx >= 0 and times[end_idx] > time_end:
            end_idx -= 1

        # Make sure we have valid indices
        if start_idx >= end_idx:
            print(f"Invalid time range: {time_start} to {time_end}")
            return

        # Process each limb
        for limb_index in limb_indices:
            # Create a collection specifically for this limb
            limb_collection_name = f"ProbabilisticFlows_Limb{limb_index}"
            self.collection_name = limb_collection_name

            # Extract the end effector trajectory for the specified limb
            # Each limb has 3 coordinates (x,y,z)
            limb_traj = []

            # Calculate step size to get desired number of frames
            step = max(1, (end_idx - start_idx) // num_frames)

            for i in range(start_idx, end_idx + 1, step):
                # Extract coordinates for this limb - assuming each limb has 3 coordinates in order
                x = trajectories[i][limb_index * 3]
                y = trajectories[i][limb_index * 3 + 1]
                z = trajectories[i][limb_index * 3 + 2]
                limb_traj.append([x, y, z])

            # Create the flow visualization
            self.generate_flow_trajectory(limb_traj)


def create_diffusion_flow(joint_states_file=None, traj_file=None, joint_index=0, limb_indices=None,
                          time_start=0, time_end=None, num_streams=30, diffusion_scale=0.08,
                          diffusion_time_map=None):
    """
    Create a flow-based diffusion visualization

    Args:
        joint_states_file (str, optional): Path to joint states CSV
        traj_file (str, optional): Path to trajectory CSV
        joint_index (int): Index of the joint to visualize
        limb_indices (list or int): Index or indices of limbs to visualize
        time_start (float): Starting time in seconds
        time_end (float): Ending time in seconds
        num_streams (int): Number of flow streams
        diffusion_scale (float): Scale of diffusion effect
        diffusion_time_map (callable, optional): Function that maps time progress (0 to 1) to diffusion scale
    """
    # Default limb indices
    if limb_indices is None:
        limb_indices = [0]

    # Create the flow visualizer
    visualizer = FlowDiffusionVisualizer(
        joint_states_file=joint_states_file,
        num_streams=num_streams,
        diffusion_scale=diffusion_scale,
        diffusion_time_map=diffusion_time_map
    )

    # Visualize a specific joint trajectory if joint states are provided
    if joint_states_file:
        visualizer.visualize_joint_trajectory(joint_index,
                                              start_frame=int(time_start * visualizer.frame_rate),
                                              end_frame=int(time_end * visualizer.frame_rate) if time_end else None)

    # Visualize end effector if trajectory file exists
    if traj_file:
        visualizer.visualize_end_effector(limb_indices, time_start, time_end, num_frames=100)

    return visualizer


if __name__ == "<run_path>":
    # Example usage - visualize end effector with diffusion

    # Path to trajectory file
    traj_file = os.path.join(ROOT_DIR, '..', '..', 'animation', 'elspider_air_walk', 'swing_traj.csv')

    # Path to joint states file (optional)
    joint_states_file = os.path.join(ROOT_DIR, '..', '..', 'animation', 'elspider_air_walk', 'joint_states.csv')

    # Define custom time-based diffusion mapping functions

    # Linear growth - diffusion increases linearly with time
    def linear_time_diffusion(t):
        return t * 2.0

    # Exponential growth - diffusion grows exponentially with time
    def exponential_time_diffusion(t):
        return (math.exp(3 * t) - 1) / 5

    # Square root growth - diffusion grows quickly at first, then slower
    def sqrt_time_diffusion(t):
        return math.sqrt(t) * 2.0

    # Create diffusion flow visualization for multiple limbs
    visualizer = create_diffusion_flow(
        joint_states_file=joint_states_file,
        traj_file=traj_file,
        joint_index=0,  # First joint
        limb_indices=[0, 2, 4],   # Multiple limbs (first, third and fifth)
        time_start=5.0,  # Start at 5 seconds
        time_end=10.0,   # End at 10 seconds
        num_streams=40,  # Number of flow streams
        diffusion_scale=0.2,  # Base scale of diffusion effect
        diffusion_time_map=exponential_time_diffusion  # Use exponential time-based diffusion
    )

    print("Time-based diffusion flow visualization created successfully!")
