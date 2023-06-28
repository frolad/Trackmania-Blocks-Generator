import bpy
import typing
from .Prefabs import get_platform_prefab
from .Constants import (
    PLATFORM_TYPE,
    SIDE_SHAPE,
    MIDDLE_SHAPE,
    shorten_platform_type,
    prepare_item_name,
)
from .ShapeGenerator import create_item

def create_platform_item(
    platform_type: PLATFORM_TYPE,
    start: SIDE_SHAPE,
    end: SIDE_SHAPE,
    middle_shape: MIDDLE_SHAPE,
    shift_xyz: typing.Tuple[int,int,int],
    dest_collection: bpy.types.Collection,
    source_object: bpy.types.Object = None,
) -> bpy.types.Collection:
    base_name = f"{shorten_platform_type(platform_type)}_"
    collection_name = base_name+prepare_item_name(middle_shape, start, end, shift_xyz)

    source_object = get_platform_prefab(platform_type)
    if source_object is None:
        return "no object for this shape"
    
    item_collection = bpy.context.blend_data.collections.new(name=collection_name)
    dest_collection.children.link(item_collection)

    has_bottom_vertices = True if "_bottom_vertices" in source_object.vertex_groups else None
    uv_scale_factor = shift_xyz[1] if middle_shape != MIDDLE_SHAPE.TURN else shift_xyz[1] + 1

    create_item(
        source_object=source_object,
        dest_collection=item_collection,
        middle_shape=middle_shape,
        start_shape=start,
        end_shape=end,
        shift_xyz=shift_xyz,
        name=collection_name,
        uv_scale_factor=uv_scale_factor,
        should_make_flat_bottom=has_bottom_vertices,
        should_delete_shape_objects=True,
    )

    