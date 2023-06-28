import bpy
import typing
from mathutils import Vector
from .BlenderUtils import (
    scale_2D,
    get_number_sign,
)

def scale_object_uv(obj: bpy.types.Object, uv_layer_name: str, scale_factor: int = 1, material_settings: dict[str, typing.Tuple[Vector, Vector]] = None):
    pivotDedfault = Vector((0, 0))
    scaleVectorX = Vector((scale_factor, 1))

    uv_layer = obj.data.uv_layers[uv_layer_name]
    ignoreGroup = obj.vertex_groups["_ignore_uv_scale"].index if "_ignore_uv_scale" in obj.vertex_groups else None

    for poly in obj.data.polygons:
        poly:bpy.types.MeshPolygon = poly

        ignoreScale = False
        for vert in poly.vertices:
            for g in obj.data.vertices[vert].groups:
                if g.group == ignoreGroup:
                    ignoreScale = True

        if not ignoreScale:
            pivot = pivotDedfault
            scaleVector = scaleVectorX
            
            mat = obj.material_slots[poly.material_index].material
            
            if material_settings and mat.name in material_settings and material_settings[mat.name][0]:
                scaleVector = material_settings[mat.name][0]

            if material_settings and mat.name in material_settings and len(material_settings[mat.name]) >= 2 and material_settings[mat.name][1]:
                pivot = material_settings[mat.name][1]

            
            for loop_index in poly.loop_indices:
                uv_layer.data[loop_index].uv = scale_2D(uv_layer.data[loop_index].uv, scaleVector, pivot)

def make_flat_bottom(obj: bpy.types.Object, end_shift_on_z: int):
    bottom_group = obj.vertex_groups["_bottom_vertices"].index if "_bottom_vertices" in obj.vertex_groups else None
    if bottom_group is None:
        return

    min_z_bottom = 0
    min_z_non_bottom = 512
    max_z_non_bottom = -512
    for vert in obj.data.vertices:
        is_bottom = False
        for g in vert.groups:
            if g.group == bottom_group:
                is_bottom = True

        z_value = round(vert.co.z, 2)
        if is_bottom:
            if z_value < min_z_bottom:
                    min_z_bottom = z_value
        else:
            if z_value < min_z_non_bottom:
                min_z_non_bottom = z_value
            if z_value > max_z_non_bottom:
                max_z_non_bottom = z_value

    safe_flat_z = min_z_bottom
    if abs(min_z_bottom)%8 > 0:
        safe_flat_z = min_z_bottom + get_number_sign(min_z_bottom)*(8-abs(min_z_bottom)%8)

    if end_shift_on_z != 0 or min_z_non_bottom != max_z_non_bottom:
        if min_z_non_bottom//8 > safe_flat_z/8:
            safe_flat_z = (min_z_non_bottom//8)*8

    _set_object_bottom_z(obj, safe_flat_z)

def _set_object_bottom_z(obj: bpy.types.Object, position_z: int):
    bottom_group = obj.vertex_groups["_bottom_vertices"].index if "_bottom_vertices" in obj.vertex_groups else None
    
    for vert in obj.data.vertices:
        for g in vert.groups:
            if g.group == bottom_group:
                vert.co.z = position_z