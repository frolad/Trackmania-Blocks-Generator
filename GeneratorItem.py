import bpy
from .properties import ShapeGeneratorProperties
from .generator.BlenderUtils import apply_mods_on_object
from .generator.ShapeGenerator import create_item, create_item_shape
from .generator.RoadItemGenerator import create_road_item
from .generator.PlatformItemGenerator import create_platform_item
from .generator.Constants import (
    ROAD_TYPE,
    SIDE_SHAPE,
    MIDDLE_SHAPE,
    enum_by_name,
    PLATFORM_TYPE,
    prepare_item_name,
)

def generate_road_item(settings: ShapeGeneratorProperties):
    road_start_type = None
    road_end_type = None
    if settings.generation_road_source == "SINGLE":
        road_start_type = enum_by_name(ROAD_TYPE, settings.road_single_type)
        road_end_type = enum_by_name(ROAD_TYPE, settings.road_single_type)
    else:
        road_start_type = enum_by_name(ROAD_TYPE, settings.road_start_type)
        road_end_type = enum_by_name(ROAD_TYPE, settings.road_end_type)

    return create_road_item(
        start=(
            road_start_type,
            enum_by_name(SIDE_SHAPE, settings.road_start_shape),
        ),
        end=(
            road_end_type,
            enum_by_name(SIDE_SHAPE, settings.road_end_shape),
        ),
        middle_shape=enum_by_name(MIDDLE_SHAPE, settings.middle_shape),
        shift_xyz=(settings.shift_on_x, settings.shift_on_y, settings.shift_on_z),
        dest_collection=bpy.context.scene.collection,
    )

def generate_platform_item(settings: ShapeGeneratorProperties):
    return create_platform_item(
        platform_type=enum_by_name(PLATFORM_TYPE, settings.platform_single_type),
        start=enum_by_name(SIDE_SHAPE, settings.platform_start_shape),
        end=enum_by_name(SIDE_SHAPE, settings.platform_end_shape),
        middle_shape=enum_by_name(MIDDLE_SHAPE, settings.middle_shape),
        shift_xyz=(settings.shift_on_x, settings.shift_on_y, settings.shift_on_z),
        dest_collection=bpy.context.scene.collection,
    )

def generate_shape_item(settings: ShapeGeneratorProperties):
    start_shape=enum_by_name(SIDE_SHAPE, settings.custom_start_shape)
    end_shape=enum_by_name(SIDE_SHAPE, settings.custom_end_shape)
    middle_shape=enum_by_name(MIDDLE_SHAPE, settings.middle_shape)
    shift_xyz=(settings.shift_on_x, settings.shift_on_y, settings.shift_on_z)
    name = "generated_"+prepare_item_name(middle_shape, start_shape, end_shape, shift_xyz)
    
    item_collection = bpy.context.blend_data.collections.new(name=name)
    bpy.context.scene.collection.children.link(item_collection)
    
    item_lattice, shape_objects = create_item_shape(
        source_object=None,
        middle_shape=middle_shape,
        start_shape=start_shape,
        end_shape=end_shape,
        shift_xyz=shift_xyz,
        name=name,
        dest_collection=item_collection,
        source_height=settings.custom_shape_height,
    )
    
    # apply curves
    apply_mods_on_object(item_lattice)
    
    # delete curves
    for obj in shape_objects:
        if obj != item_lattice:
            bpy.data.objects.remove(obj, do_unlink=True)
    return item_lattice

def generate_custom_item(settings: ShapeGeneratorProperties):
    if settings.custom_object is None:
        return "Select object first"
    else:
        start_shape=enum_by_name(SIDE_SHAPE, settings.custom_start_shape)
        end_shape=enum_by_name(SIDE_SHAPE, settings.custom_end_shape)
        middle_shape=enum_by_name(MIDDLE_SHAPE, settings.middle_shape)
        shift_xyz=(settings.shift_on_x, settings.shift_on_y, settings.shift_on_z)
        name = settings.custom_object.name+"_"+prepare_item_name(middle_shape, start_shape, end_shape, shift_xyz)
        
        has_bottom_vertices = True if "_bottom_vertices" in settings.custom_object.vertex_groups else None
        uv_scale_factor = 1
        if settings.custom_should_scale_uv:
            uv_scale_factor = settings.shift_on_y if middle_shape != MIDDLE_SHAPE.TURN else settings.shift_on_y + 1
        
        item_collection = bpy.context.blend_data.collections.new(name=name)
        bpy.context.scene.collection.children.link(item_collection)

        return create_item(
            source_object=settings.custom_object,
            dest_collection=item_collection,
            middle_shape=middle_shape,
            start_shape=start_shape,
            end_shape=end_shape,
            shift_xyz=shift_xyz,
            name=name,
            uv_scale_factor=uv_scale_factor,
            should_make_flat_bottom=has_bottom_vertices,
            should_delete_shape_objects=True,
        )