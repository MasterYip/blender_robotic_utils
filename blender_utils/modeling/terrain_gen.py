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


if __name__ == "<run_path>":
    # Test the terrain generator
    terrain_gen = TerrainGenerator(bpy)
    terrain_gen.generate_combined_terrain()
