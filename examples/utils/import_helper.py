import bpy
import os
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator


class OT_TestOpenFilebrowser(Operator, ImportHelper):
    """Custom file browser operator for image files"""
    bl_idname = "test.open_filebrowser"
    bl_label = "Open the file browser (yay)"

    # Filter for image file extensions
    filter_glob: StringProperty(
        default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp',
        options={'HIDDEN'}
    )

    # Custom boolean property
    some_boolean: BoolProperty(
        name='Do a thing',
        description='Do a thing with the file you\'ve selected',
        default=True,
    )

    def execute(self, context):
        """Handle file selection and processing"""
        filename, extension = os.path.splitext(self.filepath)
        print('Selected file:', self.filepath)
        print('File name:', filename)
        print('File extension:', extension)
        print('Some Boolean:', self.some_boolean)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OT_TestOpenFilebrowser)


def unregister():
    bpy.utils.unregister_class(OT_TestOpenFilebrowser)


if __name__ == "<run_path>":
    register()
    # Immediately invoke the operator when run as a script
    bpy.ops.test.open_filebrowser('INVOKE_DEFAULT')
