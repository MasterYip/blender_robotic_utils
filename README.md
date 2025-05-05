![banner](doc/banner_elspider.jpg)

# Blender Robotic Utilities

Blender Robotic Utilities for modeling, animation, and rendering.

## Demos

### ElSpider Air Walking

<!-- Video -->
<p align="center">
    <video src="https://github.com/user-attachments/assets/462ff944-2e98-4c50-9043-d140bcd54d4a" width="200" height="100" autoplay controls muted loop playsinline></video>
</p>

### Terrain Gen

Confined 2-layer terrain generation.
![terrain_gen](doc/terrain_gen/confined_2layer.png)

## Getting Started

### Installation

Install VS code extension [Blender Development](https://marketplace.visualstudio.com/items/?itemName=JacquesLucke.blender-development) for easy development.

Install the package using pip:

```bash
<blender_python_path> -m pip install -e ./
```

### Examples



## Extensions

### [urdf_importer](https://github.com/HoangGiang93/urdf_importer)

#### Installation

**1.Setup Python Env**

Linux:

```bash
cd <blender_path>/<version>/python/bin/ # For example cd blender-3.1.2-linux-x64/3.1/python/bin/
./python3.10 -m ensurepip
./python3.10 -m pip install --upgrade pip
./python3.10 -m pip install pyyaml
./python3.10 -m pip install rospkg
./python3.10 -m pip install urdf_parser_py
```

Windows:

Note:

- If Blender is installed to i.e. C:\Program Files\, run cmd.exe as administrator!
- Define ROS_ROOT as system environment variable pointing to a folder containing your ROS packages

```cmd
cd <blender_path>/<version>/python/bin/ # For example cd blender-3.1.2-linux-x64/3.1/python/bin/
./python.exe -m ensurepip
./python.exe -m pip install --upgrade pip
./python.exe -m pip install pyyaml
./python.exe -m pip install rospkg
./python.exe -m pip install urdf_parser_py
```

**2.Install Add-on**

- Compress the folder `urdf_importer_addon` into a ZIP file named `urdf_importer_addon.zip`.
- Open a terminal, source the ROS workspace that contains the URDF model, and then start Blender by running `blender` in the terminal.
- In Blender, go to the `Edit` menu and select `Preferences`.
- Click on `Install`.
- Navigate to and select the `urdf_importer_addon.zip` file, then click `Install Add-on`.
- Enable the add-on by checking the box next to `Import-Export: Import URDF Format`.
- Verify the installation by opening `File` → `Import`. You should see `URDF (.urdf)` listed in the menu.

## Acknowledgements

- [Blender](https://www.blender.org/)
- [urdf_importer](https://github.com/HoangGiang93/urdf_importer)
