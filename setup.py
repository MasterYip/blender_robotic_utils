# setup blender utils
from distutils.core import setup

setup(
    version='0.0.0',
    # scripts=['scripts/talker.py', 'scripts/hit_spider_planner.py'],
    packages=['blender_utils'],
    # deps
    install_requires=[
        'numpy',
        'opencv-python'
    ],
    package_dir={'': '.'}
)
