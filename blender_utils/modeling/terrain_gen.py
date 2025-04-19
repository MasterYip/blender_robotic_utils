'''
Author: GitHub Copilot
Date: 2025-04-12
Description: Terrain generator for legged locomotion including stairs, ramp, noise terrain
FilePath: /blender_utils/blender_utils/modeling/terrain_gen.py
'''

import math
import numpy as np
import bpy
import os
import random
# from noise import pnoise2
def pnoise2(x,y):
    """
    Placeholder for Perlin noise function.
    In actual implementation, this should be replaced with a proper Perlin noise function.
    """
    return random.uniform(-1, 1)

from .gridmap_gen import gridmap_gen


class TerrainGenerator:
    """
    Generate various types of terrains for legged locomotion testing:
    - Flat ground
    - Stairs
    - Ramps
    - Noisy terrains
    - Combined terrains
    - Square terrain patches
    """

    def __init__(self, bpy_nh):
        self.bpy_nh = bpy_nh

    def generate_flat_terrain(self, name="FlatTerrain", size=(10, 10), position=(0, 0, 0), resolution=(50, 50)):
        """Generate a flat terrain with specified dimensions"""
        heights = np.zeros((resolution[0], resolution[1]))

        bound = (
            position[0] - size[0]/2,
            position[0] + size[0]/2,
            position[1] - size[1]/2,
            position[1] + size[1]/2
        )

        gridmap_gen(self.bpy_nh, name, heights, bound)
        return heights

    def generate_stairs(self, name="Stairs", size=(10, 10), position=(0, 0, 0),
                        resolution=(50, 50), step_height=0.2, step_depth=1.0,
                        steps=5, direction='x'):
        """
        Generate stairs with specified dimensions

        Parameters:
        - name: name of the mesh
        - size: size of the terrain (x, y)
        - position: position of the center of the terrain
        - resolution: resolution of the terrain grid
        - step_height: height of each step
        - step_depth: depth of each step
        - steps: number of steps
        - direction: direction of stairs ('x' or 'y')
        """
        heights = np.zeros((resolution[0], resolution[1]))

        # Calculate step positions
        if direction == 'x':
            step_size_x = size[0] / steps
            for i in range(resolution[0]):
                x_rel = i / resolution[0]
                step_index = min(int(x_rel * steps), steps - 1)
                for j in range(resolution[1]):
                    heights[i, j] = step_index * step_height
        else:  # direction == 'y'
            step_size_y = size[1] / steps
            for j in range(resolution[1]):
                y_rel = j / resolution[1]
                step_index = min(int(y_rel * steps), steps - 1)
                for i in range(resolution[0]):
                    heights[i, j] = step_index * step_height

        bound = (
            position[0] - size[0]/2,
            position[0] + size[0]/2,
            position[1] - size[1]/2,
            position[1] + size[1]/2
        )

        gridmap_gen(self.bpy_nh, name, heights, bound)
        return heights

    def generate_ramp(self, name="Ramp", size=(10, 10), position=(0, 0, 0),
                      resolution=(50, 50), height=1.0, direction='x', slope_type='linear'):
        """
        Generate a ramp with specified dimensions

        Parameters:
        - name: name of the mesh
        - size: size of the terrain (x, y)
        - position: position of the center of the terrain
        - resolution: resolution of the terrain grid
        - height: maximum height of the ramp
        - direction: direction of ramp ('x', 'y', or 'diagonal')
        - slope_type: type of slope ('linear', 'quadratic', 'sinusoidal')
        """
        heights = np.zeros((resolution[0], resolution[1]))

        for i in range(resolution[0]):
            x_rel = i / (resolution[0] - 1)
            for j in range(resolution[1]):
                y_rel = j / (resolution[1] - 1)

                if direction == 'x':
                    progress = x_rel
                elif direction == 'y':
                    progress = y_rel
                elif direction == 'diagonal':
                    progress = (x_rel + y_rel) / 2
                else:
                    progress = 0

                if slope_type == 'linear':
                    heights[i, j] = progress * height
                elif slope_type == 'quadratic':
                    heights[i, j] = progress**2 * height
                elif slope_type == 'sinusoidal':
                    heights[i, j] = (math.sin(progress * math.pi - math.pi/2) + 1) / 2 * height
                else:
                    heights[i, j] = progress * height

        bound = (
            position[0] - size[0]/2,
            position[0] + size[0]/2,
            position[1] - size[1]/2,
            position[1] + size[1]/2
        )

        gridmap_gen(self.bpy_nh, name, heights, bound)
        return heights

    def generate_noisy_terrain(self, name="NoisyTerrain", size=(10, 10), position=(0, 0, 0),
                               resolution=(50, 50), base_height=0, noise_amplitude=0.5,
                               noise_scale=0.1, seed=None):
        """
        Generate a terrain with Perlin noise

        Parameters:
        - name: name of the mesh
        - size: size of the terrain (x, y)
        - position: position of the center of the terrain
        - resolution: resolution of the terrain grid
        - base_height: base height of the terrain
        - noise_amplitude: amplitude of the noise
        - noise_scale: scale of the noise (higher means more detailed)
        - seed: random seed for reproducibility
        """
        

        if seed is not None:
            random.seed(seed)

        heights = np.zeros((resolution[0], resolution[1]))

        for i in range(resolution[0]):
            for j in range(resolution[1]):
                x = i / resolution[0] * noise_scale * 10
                y = j / resolution[1] * noise_scale * 10
                heights[i, j] = base_height + pnoise2(x, y) * noise_amplitude

        bound = (
            position[0] - size[0]/2,
            position[0] + size[0]/2,
            position[1] - size[1]/2,
            position[1] + size[1]/2
        )

        gridmap_gen(self.bpy_nh, name, heights, bound)
        return heights

    def generate_combined_terrain(self, name="CombinedTerrain", size=(10, 10), position=(0, 0, 0),
                                  resolution=(50, 50), sections=None):
        """
        Generate a terrain with multiple sections (flat, stairs, ramp, etc.)

        Parameters:
        - name: name of the mesh
        - size: size of the terrain (x, y)
        - position: position of the center of the terrain
        - resolution: resolution of the terrain grid
        - sections: list of dictionaries defining sections of the terrain
          Each section should have:
          - 'type': 'flat', 'stairs', 'ramp', 'noise'
          - 'start_x', 'end_x', 'start_y', 'end_y': relative positions (0-1)
          - other parameters specific to the terrain type
        """
        if sections is None:
            # Default sections: flat -> stairs -> ramp -> noise
            sections = [
                {'type': 'flat', 'start_x': 0.0, 'end_x': 0.25, 'start_y': 0.0, 'end_y': 1.0},
                {'type': 'stairs', 'start_x': 0.25, 'end_x': 0.5, 'start_y': 0.0, 'end_y': 1.0,
                 'step_height': 0.2, 'steps': 5, 'direction': 'x'},
                {'type': 'ramp', 'start_x': 0.5, 'end_x': 0.75, 'start_y': 0.0, 'end_y': 1.0,
                 'height': 1.0, 'direction': 'x', 'slope_type': 'linear'},
                {'type': 'noise', 'start_x': 0.75, 'end_x': 1.0, 'start_y': 0.0, 'end_y': 1.0,
                 'base_height': 1.0, 'noise_amplitude': 0.3, 'noise_scale': 0.2}
            ]

        heights = np.zeros((resolution[0], resolution[1]))

        # Process each section
        for section in sections:
            section_type = section['type']
            start_x_idx = int(section['start_x'] * resolution[0])
            end_x_idx = int(section['end_x'] * resolution[0])
            start_y_idx = int(section['start_y'] * resolution[1])
            end_y_idx = int(section['end_y'] * resolution[1])

            # Calculate section dimensions
            section_size_x = size[0] * (section['end_x'] - section['start_x'])
            section_size_y = size[1] * (section['end_y'] - section['start_y'])
            section_resolution = (end_x_idx - start_x_idx, end_y_idx - start_y_idx)

            if section_resolution[0] <= 0 or section_resolution[1] <= 0:
                continue

            # Generate heights for this section
            section_heights = np.zeros(section_resolution)

            if section_type == 'flat':
                # Nothing to do, already zeros
                pass

            elif section_type == 'stairs':
                steps = section.get('steps', 5)
                step_height = section.get('step_height', 0.2)
                direction = section.get('direction', 'x')

                if direction == 'x':
                    for i in range(section_resolution[0]):
                        x_rel = i / section_resolution[0]
                        step_index = min(int(x_rel * steps), steps - 1)
                        for j in range(section_resolution[1]):
                            section_heights[i, j] = step_index * step_height
                else:  # direction == 'y'
                    for j in range(section_resolution[1]):
                        y_rel = j / section_resolution[1]
                        step_index = min(int(y_rel * steps), steps - 1)
                        for i in range(section_resolution[0]):
                            section_heights[i, j] = step_index * step_height

            elif section_type == 'ramp':
                height = section.get('height', 1.0)
                direction = section.get('direction', 'x')
                slope_type = section.get('slope_type', 'linear')

                for i in range(section_resolution[0]):
                    x_rel = i / max(1, section_resolution[0] - 1)
                    for j in range(section_resolution[1]):
                        y_rel = j / max(1, section_resolution[1] - 1)

                        if direction == 'x':
                            progress = x_rel
                        elif direction == 'y':
                            progress = y_rel
                        elif direction == 'diagonal':
                            progress = (x_rel + y_rel) / 2
                        else:
                            progress = 0

                        if slope_type == 'linear':
                            section_heights[i, j] = progress * height
                        elif slope_type == 'quadratic':
                            section_heights[i, j] = progress**2 * height
                        elif slope_type == 'sinusoidal':
                            section_heights[i, j] = (math.sin(progress * math.pi - math.pi/2) + 1) / 2 * height
                        else:
                            section_heights[i, j] = progress * height

            elif section_type == 'noise':
                

                base_height = section.get('base_height', 0)
                noise_amplitude = section.get('noise_amplitude', 0.5)
                noise_scale = section.get('noise_scale', 0.1)
                seed = section.get('seed', None)

                if seed is not None:
                    random.seed(seed)

                for i in range(section_resolution[0]):
                    for j in range(section_resolution[1]):
                        x = (section['start_x'] + (i / section_resolution[0]) *
                             (section['end_x'] - section['start_x'])) * noise_scale * 10
                        y = (section['start_y'] + (j / section_resolution[1]) *
                             (section['end_y'] - section['start_y'])) * noise_scale * 10
                        section_heights[i, j] = base_height + pnoise2(x, y) * noise_amplitude

            # Insert section heights into the main heights array
            heights[start_x_idx:end_x_idx, start_y_idx:end_y_idx] = section_heights

        bound = (
            position[0] - size[0]/2,
            position[0] + size[0]/2,
            position[1] - size[1]/2,
            position[1] + size[1]/2
        )

        gridmap_gen(self.bpy_nh, name, heights, bound)
        return heights

    def generate_square_terrain_patches(self, name="SquareTerrain", size=(10, 10), position=(0, 0, 0),
                                        resolution=(100, 100), num_patches=(3, 3), terrain_types=None,
                                        seed=None):
        """
        Generate a terrain with square patches of different terrain types (similar to leggedgym)

        Parameters:
        - name: name of the mesh
        - size: size of the terrain (x, y)
        - position: position of the center of the terrain
        - resolution: resolution of the terrain grid
        - num_patches: number of patches in each direction (x, y)
        - terrain_types: list of terrain type dictionaries with parameters. Available types:
          - 'flat': {'base_height': value}
          - 'stairs': {'step_height': value, 'steps': value, 'direction': 'x'/'y'/'random'}
          - 'ramp': {'height': value, 'direction': 'x'/'y'/'random', 'slope_type': type}
          - 'noise': {'base_height': value, 'noise_amplitude': value, 'noise_scale': value}
        - seed: random seed for reproducibility and terrain type selection
        """
        if seed is not None:
            random.seed(seed)
        
        # Default terrain types if none provided
        if terrain_types is None:
            terrain_types = [
                {'type': 'flat', 'base_height': 0.0},
                {'type': 'stairs', 'step_height': 0.15, 'steps': 3, 'direction': 'random'},
                {'type': 'ramp', 'height': 0.3, 'direction': 'random', 'slope_type': 'linear'},
                {'type': 'noise', 'base_height': 0.0, 'noise_amplitude': 0.2, 'noise_scale': 0.1}
            ]
        
        # Initialize heights array
        heights = np.zeros((resolution[0], resolution[1]))
        
        # Calculate patch dimensions
        patch_size_x = size[0] / num_patches[0]
        patch_size_y = size[1] / num_patches[1]
        patch_res_x = resolution[0] // num_patches[0]
        patch_res_y = resolution[1] // num_patches[1]
        
        # Generate each patch
        for i in range(num_patches[0]):
            for j in range(num_patches[1]):
                # Select a random terrain type
                terrain_type = random.choice(terrain_types)
                
                # Calculate patch bounds
                start_x = i * patch_res_x
                end_x = (i + 1) * patch_res_x
                start_y = j * patch_res_y
                end_y = (j + 1) * patch_res_y
                
                # Generate patch heights based on terrain type
                patch_heights = np.zeros((end_x - start_x, end_y - start_y))
                
                if terrain_type['type'] == 'flat':
                    base_height = terrain_type.get('base_height', 0.0)
                    patch_heights.fill(base_height)
                    
                elif terrain_type['type'] == 'stairs':
                    step_height = terrain_type.get('step_height', 0.15)
                    steps = terrain_type.get('steps', 3)
                    direction = terrain_type.get('direction', 'random')
                    
                    if direction == 'random':
                        direction = random.choice(['x', 'y'])
                    
                    if direction == 'x':
                        for x in range(patch_heights.shape[0]):
                            x_rel = x / patch_heights.shape[0]
                            step_index = min(int(x_rel * steps), steps - 1)
                            for y in range(patch_heights.shape[1]):
                                patch_heights[x, y] = step_index * step_height
                    else:  # direction == 'y'
                        for y in range(patch_heights.shape[1]):
                            y_rel = y / patch_heights.shape[1]
                            step_index = min(int(y_rel * steps), steps - 1)
                            for x in range(patch_heights.shape[0]):
                                patch_heights[x, y] = step_index * step_height
                
                elif terrain_type['type'] == 'ramp':
                    height = terrain_type.get('height', 0.3)
                    direction = terrain_type.get('direction', 'random')
                    slope_type = terrain_type.get('slope_type', 'linear')
                    
                    if direction == 'random':
                        direction = random.choice(['x', 'y', 'diagonal'])
                    
                    for x in range(patch_heights.shape[0]):
                        x_rel = x / max(1, patch_heights.shape[0] - 1)
                        for y in range(patch_heights.shape[1]):
                            y_rel = y / max(1, patch_heights.shape[1] - 1)
                            
                            if direction == 'x':
                                progress = x_rel
                            elif direction == 'y':
                                progress = y_rel
                            elif direction == 'diagonal':
                                progress = (x_rel + y_rel) / 2
                            else:
                                progress = 0
                            
                            if slope_type == 'linear':
                                patch_heights[x, y] = progress * height
                            elif slope_type == 'quadratic':
                                patch_heights[x, y] = progress**2 * height
                            elif slope_type == 'sinusoidal':
                                patch_heights[x, y] = (math.sin(progress * math.pi - math.pi/2) + 1) / 2 * height
                
                elif terrain_type['type'] == 'noise':
                    base_height = terrain_type.get('base_height', 0.0)
                    noise_amplitude = terrain_type.get('noise_amplitude', 0.2)
                    noise_scale = terrain_type.get('noise_scale', 0.1)
                    local_seed = terrain_type.get('seed', random.randint(0, 1000))
                    
                    # Save current random state
                    state = random.getstate()
                    random.seed(local_seed)
                    
                    for x in range(patch_heights.shape[0]):
                        for y in range(patch_heights.shape[1]):
                            nx = (i + x / patch_heights.shape[0]) * noise_scale * 10
                            ny = (j + y / patch_heights.shape[1]) * noise_scale * 10
                            patch_heights[x, y] = base_height + pnoise2(nx, ny) * noise_amplitude
                    
                    # Restore random state
                    random.setstate(state)
                
                # Apply this patch to the main height map
                heights[start_x:end_x, start_y:end_y] = patch_heights
        
        # Create smoothed borders between patches (optional)
        smoothed_heights = heights.copy()
        blur_radius = min(patch_res_x, patch_res_y) // 10  # Border blur radius
        
        if blur_radius > 0:
            for i in range(1, num_patches[0]):
                border_x = i * patch_res_x
                for x in range(max(0, border_x - blur_radius), min(resolution[0], border_x + blur_radius)):
                    for y in range(resolution[1]):
                        # Calculate distance from border (normalized)
                        dist = abs(x - border_x) / blur_radius
                        weight = 0.5 * (1 - math.cos(dist * math.pi))
                        
                        # Blend heights at border
                        if x < border_x:
                            left = heights[x, y]
                            right = heights[min(resolution[0]-1, border_x), y]
                            smoothed_heights[x, y] = left * weight + right * (1 - weight)
                        else:
                            left = heights[max(0, border_x - 1), y]
                            right = heights[x, y]
                            smoothed_heights[x, y] = left * (1 - weight) + right * weight
            
            for j in range(1, num_patches[1]):
                border_y = j * patch_res_y
                for y in range(max(0, border_y - blur_radius), min(resolution[1], border_y + blur_radius)):
                    for x in range(resolution[0]):
                        # Calculate distance from border (normalized)
                        dist = abs(y - border_y) / blur_radius
                        weight = 0.5 * (1 - math.cos(dist * math.pi))
                        
                        # Blend heights at border
                        if y < border_y:
                            top = heights[x, y]
                            bottom = heights[x, min(resolution[1]-1, border_y)]
                            smoothed_heights[x, y] = top * weight + bottom * (1 - weight)
                        else:
                            top = heights[x, max(0, border_y - 1)]
                            bottom = heights[x, y]
                            smoothed_heights[x, y] = top * (1 - weight) + bottom * weight
        
        # Define terrain bounds
        bound = (
            position[0] - size[0]/2,
            position[0] + size[0]/2,
            position[1] - size[1]/2,
            position[1] + size[1]/2
        )
        
        # Generate the terrain mesh
        gridmap_gen(self.bpy_nh, name, smoothed_heights, bound)
        return smoothed_heights


if __name__ == "<run_path>":
    # Test the terrain generator
    terrain_gen = TerrainGenerator(bpy)
    terrain_gen.generate_combined_terrain()
