'''
Author: MasterYip 2205929492@qq.com
Date: 2025-01-28 21:11:22
Description: file content
FilePath: /blender_utils/blender_utils/utils/utils.py
LastEditTime: 2025-01-28 21:21:16
LastEditors: MasterYip
'''
import bpy
from typing import Optional
from typing import Union


def link_obj_to_collection(obj, collection: Optional[Union[str, bpy.types.Collection]] = None):
    """ Link the object to the collection """
    if collection is None:
        collection = bpy.context.collection
    elif isinstance(collection, str):
        collection = bpy.data.collections.get(collection)
        if collection is None:
            collection = bpy.data.collections.new(collection)
            bpy.context.scene.collection.children.link(collection)
    # elif isinstance(collection, bpy.types.Collection):
    collection.objects.link(obj)
    return collection
