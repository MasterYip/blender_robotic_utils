'''
Author: GitHub Copilot
Date: 2025-05-12
Description: Flow-based visualization for probabilistic robot trajectories with diffusion effects
FilePath: /blender_utils/examples/modeling/probabilistic/prob_example.py
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
    
    def __init__(self, joint_states_file=None, num_streams=30, diffusion_scale=0.05):
        """
        Initialize the flow diffusion visualizer
        
        Args:
            joint_states_file (str, optional): Path to joint states CSV
            num_streams (int, optional): Number of flow streams to create
            diffusion_scale (float, optional): Scale factor for position variations
        """
        self.joint_states_file = joint_states_file
        self.num_streams = num_streams
        self.diffusion_scale = diffusion_scale
        self.frame_rate = 30
        self.collection_name = "ProbabilisticFlows"
        
        # Load joint states if provided
        if joint_states_file:
            self.times, self.joint_states = read_csv_joint_states(joint_states_file)
    
    def add_noise_to_trajectory(self, traj_data, noise_level):
        """
        Add Gaussian noise to a trajectory to simulate diffusion
        
        Args:
            traj_data (list): Original trajectory data points
            noise_level (float): Standard deviation of the noise
            
        Returns:
            list: Trajectory with added noise
        """
        noisy_traj = []
        for point in traj_data:
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
            # Calculate diffusion level based on stream index
            # Higher indices get more diffusion
            diffusion_level = (i + 1) / self.num_streams * self.diffusion_scale
            
            # Create noisy trajectory
            noisy_trajectory = self.add_noise_to_trajectory(trajectory_points, diffusion_level)
            
            # Create curve for this flow stream
            curve_name = f"flow_stream_{i}"
            
            # Create the curve (note: create_curve doesn't return the object)
            create_curve(noisy_trajectory, curve_name, self.collection_name, bevel_depth=0.3 * (1 - diffusion_level) + 0.1)
            
            # Get the curve object we just created
            curve_obj = bpy.data.objects.get(curve_name)
            
            if curve_obj:
                # Calculate alpha based on diffusion level
                alpha = 1.0 - (i / self.num_streams) * 0.85
                
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
    
    def visualize_end_effector(self, limb_index, num_frames=100):
        """
        Visualize the end effector trajectory for a specific limb
        
        Args:
            limb_index (int): Index of the limb/leg to visualize (0-5 for hexapod)
            num_frames (int): Number of frames to visualize
        """
        # Example: If the data is from a CSV file like the swing_traj.csv
        traj_file = os.path.join(ROOT_DIR, '..', '..', 'animation', 'elspider_air_walk', 'swing_traj.csv')
        times, trajectories = read_csv_swingtraj(traj_file)
        
        # Extract the end effector trajectory for the specified limb
        # Each limb has 3 coordinates (x,y,z)
        limb_traj = []
        step = max(1, len(trajectories) // num_frames)
        
        for i in range(0, min(len(trajectories), num_frames * step), step):
            # Extract coordinates for this limb - assuming each limb has 3 coordinates in order
            x = trajectories[i][limb_index * 3]
            y = trajectories[i][limb_index * 3 + 1]
            z = trajectories[i][limb_index * 3 + 2]
            limb_traj.append([x, y, z])
        
        # Create the flow visualization
        self.generate_flow_trajectory(limb_traj)


def create_diffusion_flow(joint_states_file=None, traj_file=None, joint_index=0, limb_index=0, 
                          num_streams=30, diffusion_scale=0.08):
    """
    Create a flow-based diffusion visualization
    
    Args:
        joint_states_file (str, optional): Path to joint states CSV
        traj_file (str, optional): Path to trajectory CSV
        joint_index (int): Index of the joint to visualize
        limb_index (int): Index of the limb to visualize
        num_streams (int): Number of flow streams
        diffusion_scale (float): Scale of diffusion effect
    """
    # Create the flow visualizer
    visualizer = FlowDiffusionVisualizer(
        joint_states_file=joint_states_file,
        num_streams=num_streams,
        diffusion_scale=diffusion_scale
    )
    
    # Visualize a specific joint trajectory if joint states are provided
    if joint_states_file:
        visualizer.visualize_joint_trajectory(joint_index, start_frame=0, end_frame=100)
    
    # Visualize end effector if trajectory file exists
    if traj_file:
        visualizer.visualize_end_effector(limb_index, num_frames=100)
    
    return visualizer


if __name__ == "<run_path>":
    # Example usage - visualize end effector with diffusion
    
    # Path to trajectory file
    traj_file = os.path.join(ROOT_DIR, '..', '..', 'animation', 'elspider_air_walk', 'swing_traj.csv')
    
    # Path to joint states file (optional)
    joint_states_file = os.path.join(ROOT_DIR, '..', '..', 'animation', 'elspider_air_walk', 'joint_states.csv')
    
    # Create diffusion flow visualization
    visualizer = create_diffusion_flow(
        joint_states_file=joint_states_file,
        traj_file=traj_file,
        joint_index=0,  # First joint
        limb_index=0,   # First limb (foot)
        num_streams=40,  # Number of flow streams
        diffusion_scale=1.2  # Scale of diffusion effect
    )
    
    print("Flow-based diffusion visualization created successfully!")