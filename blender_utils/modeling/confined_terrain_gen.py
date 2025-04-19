'''
Author: GitHub Copilot
Date: 2025-04-19
Description: Generator for confined terrain with ground and ceiling plus obstacles
FilePath: /blender_utils/blender_utils/modeling/confined_terrain_gen.py
'''

import bpy
import bmesh
import os
import math
import random
import numpy as np
from .gridmap_gen import gridmap_gen


class ConfinedTerrainGenerator:
    """
    Generate a confined terrain with ground and ceiling layers, plus obstacles in between.

    The generator provides two methods:
    1. Add random boxes between the layers, creating a confined space with box obstacles
    2. Create terrain where random box spaces modify both the ground and ceiling surfaces
    """

    def __init__(self, bpy_nh):
        self.bpy_nh = bpy_nh

    def _create_box(self, name, position, size):
        """
        Create a box mesh at the given position with the specified size

        Parameters:
        - name: name of the box mesh
        - position: (x, y, z) position of the center of the box
        - size: (width, length, height) dimensions of the box

        Returns:
        - bpy.types.Object: The created box object
        """
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)

        # Scale the cube
        for v in bm.verts:
            v.co.x *= size[0]
            v.co.y *= size[1]
            v.co.z *= size[2]

            # Move to position
            v.co.x += position[0]
            v.co.y += position[1]
            v.co.z += position[2]

        # Create mesh and object
        mesh = self.bpy_nh.data.meshes.new(name)
        bm.to_mesh(mesh)
        bm.free()

        obj = self.bpy_nh.data.objects.new(name, mesh)
        self.bpy_nh.context.collection.objects.link(obj)

        return obj

    def _join_objects(self, name, objects):
        """
        Join multiple objects into a single mesh object

        Parameters:
        - name: name of the resulting joined mesh
        - objects: list of objects to join

        Returns:
        - bpy.types.Object: The joined mesh object
        """
        # Filter out None objects
        valid_objects = [obj for obj in objects if obj is not None]

        # If there are no valid objects, return a simple empty object
        if not valid_objects:
            mesh = self.bpy_nh.data.meshes.new(name)
            obj = self.bpy_nh.data.objects.new(name, mesh)
            self.bpy_nh.context.collection.objects.link(obj)
            return obj

        # If there's only one valid object, rename it and return it
        if len(valid_objects) == 1:
            valid_objects[0].name = name
            return valid_objects[0]

        # Create a new empty mesh
        mesh = self.bpy_nh.data.meshes.new(name)
        obj = self.bpy_nh.data.objects.new(name, mesh)
        self.bpy_nh.context.collection.objects.link(obj)

        # Create a bmesh to store all the geometry
        bm = bmesh.new()

        # Add all the geometry from the objects
        for ob in valid_objects:
            try:
                temp_mesh = ob.to_mesh()
                bm.from_mesh(temp_mesh)
                ob.to_mesh_clear()

                # Remove the original object
                self.bpy_nh.data.objects.remove(ob)
            except Exception as e:
                print(f"Error processing object {ob.name}: {e}")

        # Update the mesh with the bmesh data
        bm.to_mesh(mesh)
        bm.free()

        return obj

    def generate_with_boxes(self, name="ConfinedTerrain", size=(10, 10), position=(0, 0, 0),
                            layer_distance=2.0, ground_height=0.0, ceiling_height=None,
                            box_count=10, min_box_size=(0.5, 0.5, 0.5), max_box_size=(2, 2, 1.5),
                            ground_heights=None, ceiling_heights=None):
        """
        Generate a confined terrain with ground and ceiling layers, plus random box obstacles in between

        Parameters:
        - name: base name for the generated meshes
        - size: (width, length) of the terrain area
        - position: (x, y, z) position of the center of the terrain
        - layer_distance: distance between ground and ceiling
        - ground_height: base height of the ground layer (default: 0.0)
        - ceiling_height: base height of the ceiling layer (default: ground_height + layer_distance)
        - box_count: number of box obstacles to generate
        - min_box_size: minimum (width, length, height) of box obstacles
        - max_box_size: maximum (width, length, height) of box obstacles
        - ground_heights: optional 2D array of heights for the ground layer
        - ceiling_heights: optional 2D array of heights for the ceiling layer

        Returns:
        - bpy.types.Object: The combined terrain mesh
        """
        if ceiling_height is None:
            ceiling_height = ground_height + layer_distance

        # Create objects list to store all meshes before joining
        objects = []

        # Generate ground layer
        if ground_heights is None:
            # Default flat ground
            ground_heights = np.full((50, 50), ground_height)

        ground_bound = (
            position[0] - size[0]/2,
            position[0] + size[0]/2,
            position[1] - size[1]/2,
            position[1] + size[1]/2
        )
        ground_obj = self.bpy_nh.data.objects.new(f"{name}_Ground", None)
        gridmap_gen(self.bpy_nh, f"{name}_Ground", ground_heights, ground_bound)
        ground_obj = self.bpy_nh.context.scene.objects.get(f"{name}_Ground")
        objects.append(ground_obj)

        # Generate ceiling layer (inverted so normals point down)
        if ceiling_heights is None:
            # Default flat ceiling
            ceiling_heights = np.full((50, 50), ceiling_height)

        # Clone the ceiling heights but invert the normals by flipping the order
        inv_ceiling_heights = ceiling_heights[::-1, ::-1]

        ceiling_bound = (
            position[0] - size[0]/2,
            position[0] + size[0]/2,
            position[1] - size[1]/2,
            position[1] + size[1]/2
        )
        ceiling_obj = self.bpy_nh.data.objects.new(f"{name}_Ceiling", None)
        gridmap_gen(self.bpy_nh, f"{name}_Ceiling", inv_ceiling_heights, ceiling_bound)
        ceiling_obj = self.bpy_nh.context.scene.objects.get(f"{name}_Ceiling")
        objects.append(ceiling_obj)

        # Generate random boxes
        for i in range(box_count):
            # Random position within terrain bounds
            x = random.uniform(position[0] - size[0]/2 + max_box_size[0]/2,
                               position[0] + size[0]/2 - max_box_size[0]/2)
            y = random.uniform(position[1] - size[1]/2 + max_box_size[1]/2,
                               position[1] + size[1]/2 - max_box_size[1]/2)

            # Random size
            box_width = random.uniform(min_box_size[0], max_box_size[0])
            box_length = random.uniform(min_box_size[1], max_box_size[1])

            # Handle box height and position - either connect to ground or ceiling
            if random.choice([True, False]):  # Connect to ground
                box_height = random.uniform(min_box_size[2], max_box_size[2])
                # Find ground height at this position
                rel_x = (x - (position[0] - size[0]/2)) / size[0]
                rel_y = (y - (position[1] - size[1]/2)) / size[1]
                i_idx = min(int(rel_x * len(ground_heights)), len(ground_heights) - 1)
                j_idx = min(int(rel_y * len(ground_heights[0])), len(ground_heights[0]) - 1)
                local_ground_height = ground_heights[i_idx][j_idx]

                # Position box on ground
                z = local_ground_height + box_height / 2
            else:  # Connect to ceiling
                box_height = random.uniform(min_box_size[2], max_box_size[2])
                # Find ceiling height at this position
                rel_x = (x - (position[0] - size[0]/2)) / size[0]
                rel_y = (y - (position[1] - size[1]/2)) / size[1]
                i_idx = min(int(rel_x * len(ceiling_heights)), len(ceiling_heights) - 1)
                j_idx = min(int(rel_y * len(ceiling_heights[0])), len(ceiling_heights[0]) - 1)
                local_ceiling_height = ceiling_heights[i_idx][j_idx]

                # Position box on ceiling
                z = local_ceiling_height - box_height / 2

            # Create box and add to objects list
            box_obj = self._create_box(f"{name}_Box_{i}", (x, y, z), (box_width, box_length, box_height))
            objects.append(box_obj)

        # Join all objects into a single mesh
        final_obj = self._join_objects(name, objects)
        return final_obj

    def generate_with_surface_modifications(self, name="ConfinedTerrain", size=(10, 10), position=(0, 0, 0),
                                            layer_distance=2.0, ground_height=0.0, ceiling_height=None,
                                            obstacle_count=10, min_obstacle_size=(0.5, 0.5, 0.5),
                                            max_obstacle_size=(2, 2, 1.5), resolution=(50, 50)):
        """
        Generate a confined terrain where obstacles modify the ground and ceiling surfaces

        Parameters:
        - name: base name for the generated meshes
        - size: (width, length) of the terrain area
        - position: (x, y, z) position of the center of the terrain
        - layer_distance: distance between ground and ceiling
        - ground_height: base height of the ground layer (default: 0.0)
        - ceiling_height: base height of the ceiling layer (default: ground_height + layer_distance)
        - obstacle_count: number of obstacle spaces to generate
        - min_obstacle_size: minimum (width, length, height) of obstacle spaces
        - max_obstacle_size: maximum (width, length, height) of obstacle spaces
        - resolution: resolution of the terrain grid

        Returns:
        - bpy.types.Object: The combined terrain mesh
        """
        if ceiling_height is None:
            ceiling_height = ground_height + layer_distance

        # Initialize height arrays for ground and ceiling
        ground_heights = np.full(resolution, ground_height)
        ceiling_heights = np.full(resolution, ceiling_height)

        # Generate random obstacle spaces and modify ground/ceiling heights
        obstacle_locations = []

        for i in range(obstacle_count):
            # Random position within terrain bounds
            x = random.uniform(position[0] - size[0]/2 + max_obstacle_size[0]/2,
                               position[0] + size[0]/2 - max_obstacle_size[0]/2)
            y = random.uniform(position[1] - size[1]/2 + max_obstacle_size[1]/2,
                               position[1] + size[1]/2 - max_obstacle_size[1]/2)

            # Random size
            obs_width = random.uniform(min_obstacle_size[0], max_obstacle_size[0])
            obs_length = random.uniform(min_obstacle_size[1], max_obstacle_size[1])
            obs_height = random.uniform(min_obstacle_size[2], max_obstacle_size[2])

            # Determine connection (ground or ceiling)
            connect_to_ground = random.choice([True, False])

            # Calculate affected grid indices
            x_min_rel = ((x - obs_width/2) - (position[0] - size[0]/2)) / size[0]
            x_max_rel = ((x + obs_width/2) - (position[0] - size[0]/2)) / size[0]
            y_min_rel = ((y - obs_length/2) - (position[1] - size[1]/2)) / size[1]
            y_max_rel = ((y + obs_length/2) - (position[1] - size[1]/2)) / size[1]

            i_min = max(0, min(resolution[0] - 1, int(x_min_rel * resolution[0])))
            i_max = max(0, min(resolution[0] - 1, int(x_max_rel * resolution[0])))
            j_min = max(0, min(resolution[1] - 1, int(y_min_rel * resolution[1])))
            j_max = max(0, min(resolution[1] - 1, int(y_max_rel * resolution[1])))

            # Ensure valid ranges
            if i_max <= i_min:
                i_max = i_min + 1
            if j_max <= j_min:
                j_max = j_min + 1

            # Modify heights in the affected area
            if connect_to_ground:
                for i_idx in range(i_min, i_max + 1):
                    for j_idx in range(j_min, j_max + 1):
                        # Modify ground height to create an obstacle
                        ground_heights[i_idx, j_idx] = ground_height + obs_height

                # Store obstacle info for potential use
                obstacle_locations.append({
                    'position': (x, y, ground_height + obs_height/2),
                    'size': (obs_width, obs_length, obs_height),
                    'connect_to': 'ground'
                })
            else:
                for i_idx in range(i_min, i_max + 1):
                    for j_idx in range(j_min, j_max + 1):
                        # Modify ceiling height to create an obstacle
                        ceiling_heights[i_idx, j_idx] = ceiling_height - obs_height

                # Store obstacle info for potential use
                obstacle_locations.append({
                    'position': (x, y, ceiling_height - obs_height/2),
                    'size': (obs_width, obs_length, obs_height),
                    'connect_to': 'ceiling'
                })

        # Create terrain with modified height maps
        return self.generate_with_boxes(
            name=name,
            size=size,
            position=position,
            layer_distance=layer_distance,
            ground_height=ground_height,
            ceiling_height=ceiling_height,
            box_count=0,  # No additional boxes
            ground_heights=ground_heights,
            ceiling_heights=ceiling_heights
        )


if __name__ == "__main__":
    # Example usage
    terrain_gen = ConfinedTerrainGenerator(bpy)

    # Method 1: Generate terrain with random box obstacles
    terrain_gen.generate_with_boxes(
        name="ConfinedTerrain_Boxes",
        size=(10, 10),
        position=(0, 0, 0),
        layer_distance=2.0,
        box_count=15
    )

    # Method 2: Generate terrain with surface modifications
    terrain_gen.generate_with_surface_modifications(
        name="ConfinedTerrain_Surfaces",
        size=(10, 10),
        position=(15, 0, 0),  # Place next to the first terrain
        layer_distance=2.0,
        obstacle_count=15
    )
