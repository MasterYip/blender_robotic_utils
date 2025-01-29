'''
Author: MasterYip 2205929492@qq.com
Date: 2025-01-28 21:42:27
Description: file content
FilePath: /blender_utils/blender_utils/rendering/rendering.py
LastEditTime: 2025-01-29 14:58:42
LastEditors: MasterYip
'''

import bpy


def principled_bsdf_material(name="Principled_BSDF",
                             base_color=(0.8, 0.8, 0.8, 1.0),
                             roughness=0.5, metallic=0.0, ior=1.45,
                             emission_color=(0.0, 0.0, 0.0, 1.0), emission_strength=0.0):
    """
    为指定对象创建一个Principled BSDF材质
    :param obj: 要应用材质的对象
    :param base_color: 基础颜色 (R, G, B, A)
    :param roughness: 粗糙度 (0.0 到 1.0)
    :param metallic: 金属度 (0.0 到 1.0)
    :param ior: 反射率
    :return: 创建的材质
    """
    # 创建一个新的材质
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True  # 启用节点编辑

    # 清除默认节点
    nodes = material.node_tree.nodes
    nodes.clear()

    # 添加Principled BSDF节点
    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (0, 0)

    # 设置Principled BSDF参数
    # print("\n".join((bsdf_node.inputs.keys())))
    # Basic
    bsdf_node.inputs['Base Color'].default_value = base_color
    bsdf_node.inputs['Roughness'].default_value = roughness
    bsdf_node.inputs['Metallic'].default_value = metallic
    bsdf_node.inputs['IOR'].default_value = ior
    # Emission
    bsdf_node.inputs['Emission Color'].default_value = emission_color
    bsdf_node.inputs['Emission Strength'].default_value = emission_strength

    # 添加输出节点
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (400, 0)

    # 连接BSDF节点到输出节点
    links = material.node_tree.links
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

    return material


def link_material_to_obj(obj, material):
    """
    Link the material to the object
    :param obj: The object to link the material
    :param material: The material to link
    """
    if isinstance(obj, list):
        for o in obj:
            if o.data.materials:
                o.data.materials[0] = material
            else:
                o.data.materials.append(material)
    elif isinstance(obj, bpy.types.Object):
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)
    else:
        raise ValueError("obj must be a list or a bpy.types.Object")


def create_gradient_material_for_curve(curve_objs, start_color=(1, 0, 0, 1), end_color=(1, 0, 0, 0)):
    """
    为曲线对象创建从头到尾的颜色渐变材质
    :param curve_objs: 曲线对象
    :param start_color: 渐变起始颜色 (R, G, B, A)
    :param end_color: 渐变结束颜色 (R, G, B, A)
    :return: 创建的材质
    """

    # 创建一个新的材质
    material = bpy.data.materials.new(name="Gradient_Material")
    material.use_nodes = True  # 启用节点编辑

    # 获取节点和链接
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()  # 清除默认节点

    # 添加材质节点
    # 1. 添加渐变纹理节点
    gradient_node = nodes.new(type='ShaderNodeValToRGB')
    gradient_node.location = (0, 0)
    gradient_node.color_ramp.elements[1].color = start_color  # 起始颜色
    gradient_node.color_ramp.elements[0].color = end_color    # 结束颜色

    # # 2. 添加属性节点（使用曲线参数）
    # attribute_node = nodes.new(type='ShaderNodeAttribute')
    # attribute_node.location = (-200, 0)
    # attribute_node.attribute_name = 'parametric'  # 使用曲线的参数化坐标
    # 2. 添加纹理坐标节点
    texture_node = nodes.new(type='ShaderNodeTexCoord')
    # texture_node.from_instancer = True
    # separate XYZ
    separate_node = nodes.new(type='ShaderNodeSeparateXYZ')

    # 3. 添加BSDF节点
    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (200, 0)
    bsdf_node.inputs['Emission Strength'].default_value = 1.0

    # 4. 添加输出节点
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (400, 0)

    # 连接节点
    # links.new(attribute_node.outputs['Fac'], gradient_node.inputs['Fac'])
    links.new(texture_node.outputs['UV'], separate_node.inputs['Vector'])
    links.new(separate_node.outputs['X'], gradient_node.inputs['Fac'])
    links.new(gradient_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    links.new(gradient_node.outputs['Alpha'], bsdf_node.inputs['Alpha'])
    links.new(gradient_node.outputs['Color'], bsdf_node.inputs['Emission Color'])
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

    # 将材质应用到曲线对象
    if isinstance(curve_objs, bpy.types.Object):
        curve_objs = [curve_objs]
    for curve_obj in curve_objs:
        if curve_obj.data.materials:
            curve_obj.data.materials[0] = material
        else:
            curve_obj.data.materials.append(material)

    return material


if __name__ == "<run_path>":
    # if bpy.context.selected_objects:
    #     mat = principled_bsdf_material(base_color=(0.0, 0.5, 0.5, 1.0), roughness=0.3, metallic=0.8,
    #                                    emission_color=(0.0, 1.0, 0.0, 1.0), emission_strength=1)
    #     link_material_to_obj(bpy.context.selected_objects, mat)
    # else:
    #     print("请先选中一个对象")
    # 示例：为选中的曲线对象创建渐变材质

    if bpy.context.selected_objects:
        create_gradient_material_for_curve(bpy.context.selected_objects, start_color=(1, 0.0, 0, 1), end_color=(1, 0.0, 0, 0))
    else:
        print("请先选中一个(曲线)对象")
