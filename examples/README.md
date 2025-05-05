# Blender Robotic Utilities - Examples

This directory contains examples demonstrating the usage of various components of the `blender_utils` package for robotics-related tasks in Blender.

## Directory Structure

The examples are organized into the following categories:

### Modeling

Examples related to creating and manipulating 3D models and terrain.

#### Terrain Generation

- **[terrain_basics.py](modeling/terrain/terrain_basics.py)**: Basic terrain generation examples (flat terrain, stairs, ramps, and noise)
- **[terrain_combined.py](modeling/terrain/terrain_combined.py)**: Advanced terrain combinations for robotics testing
- **[terrain_confined.py](modeling/terrain/terrain_confined.py)**: Confined environments with ceilings and obstacles
- **[terrain_legacy.py](modeling/terrain/terrain_legacy.py)**: Original terrain generation examples

#### Gridmap Generation

- **[gridmap_examples.py](modeling/gridmap/gridmap_examples.py)**: Examples of creating height-based terrains using gridmaps

### Animation

Examples for animating robots and trajectories.

- **[robot_animator_examples.py](animation/robot_animator_examples.py)**: Examples of animating robots using joint states and visualizing trajectories

### Scene Creation

Examples for creating complete scenes for robotics simulation and visualization.

- **[gcs_path_search_examples.py](scene_creator/gcs_path_search_examples.py)**: Examples of creating scenes for path planning with guide surfaces

## Usage

To run these examples, you'll need Blender with the `blender_utils` package installed.

Most examples can be run directly from Blender's text editor or via the command line with:

```bash
blender --background --python examples/path/to/example.py
```

Or by running them through the Blender Text Editor after opening Blender:

1. Open Blender
2. Navigate to the Text Editor view
3. Open the example file
4. Run the script (Alt+P or Run Script button)

## Helper Modules

- **[import_helper.py](utils/import_helper.py)**: Utilities for managing imports in the examples

## Dependencies

Some examples require additional dependencies:

- For terrain examples using noise: `pip install noise` or `pip install opensimplex`
- For animation examples: CSV files containing joint states or trajectory data