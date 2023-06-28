import bpy
import typing
from mathutils import Vector
from .Prefabs import get_road_prefab
from .Constants import (
    ROAD_TYPE,
    SIDE_SHAPE,
    MIDDLE_SHAPE,
    prepare_item_name,
    shorten_road_start_end,
)
from .ShapeGenerator import create_item

def create_road_item(
    start: typing.Tuple[ROAD_TYPE, SIDE_SHAPE],
    end: typing.Tuple[ROAD_TYPE, SIDE_SHAPE],
    middle_shape: MIDDLE_SHAPE,
    shift_xyz: typing.Tuple[int,int,int],
    dest_collection: bpy.types.Collection,
) -> bpy.types.Object:
    base_name = shorten_road_start_end(start[0], end[0])+"_"
    collection_name = base_name+prepare_item_name(middle_shape, start[1], end[1], shift_xyz)

    source_object = get_road_prefab(start, end)
    if source_object is None:
        return "no object for this shape"
    
    item_collection = bpy.context.blend_data.collections.new(name=collection_name)
    dest_collection.children.link(item_collection)

    has_bottom_vertices = True if "_bottom_vertices" in source_object.vertex_groups else None
    uv_scale_factor = shift_xyz[1] if middle_shape != MIDDLE_SHAPE.TURN else shift_xyz[1] + 1

    return create_item(
        source_object=source_object,
        dest_collection=item_collection,
        middle_shape=middle_shape,
        start_shape=start[1],
        end_shape=end[1],
        shift_xyz=shift_xyz,
        name=collection_name,
        uv_scale_factor=uv_scale_factor,
        uv_material_settings = {
            "TM_PlatformGrass_PlatformTech_asset": [Vector((1, uv_scale_factor))],
            "TM_DecalMarks_asset":                 [None, Vector((0.1, 0))],
        },
        should_make_flat_bottom=has_bottom_vertices,
        should_delete_shape_objects=True,
    ), item_collection

    