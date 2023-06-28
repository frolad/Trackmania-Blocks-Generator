import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    IntProperty,
    BoolProperty,
    EnumProperty,
    PointerProperty,
)
from .generator.Constants import (
    ROAD_TYPE,
    SIDE_SHAPE,
    MIDDLE_SHAPE,
    PLATFORM_TYPE,
)

ROAD_TYPES = (
    (ROAD_TYPE.BLAD_ROAD_NARROW.name, ROAD_TYPE.BLAD_ROAD_NARROW.value, ROAD_TYPE.BLAD_ROAD_NARROW.name),
    (ROAD_TYPE.ROAD_TECH.name, ROAD_TYPE.ROAD_TECH.value, ROAD_TYPE.ROAD_TECH.name),
    (ROAD_TYPE.ROAD_BUMP.name, ROAD_TYPE.ROAD_BUMP.value, ROAD_TYPE.ROAD_BUMP.name),
    (ROAD_TYPE.ROAD_DIRT.name, ROAD_TYPE.ROAD_DIRT.value, ROAD_TYPE.ROAD_DIRT.name),
    (ROAD_TYPE.ROAD_ICE.name, ROAD_TYPE.ROAD_ICE.value, ROAD_TYPE.ROAD_ICE.name),
    (ROAD_TYPE.ROAD_GRASS.name, ROAD_TYPE.ROAD_GRASS.value, ROAD_TYPE.ROAD_GRASS.name),
)

PLATFORM_TYPES = (
    (PLATFORM_TYPE.BLACK_ROAD.name, PLATFORM_TYPE.BLACK_ROAD.value, PLATFORM_TYPE.BLACK_ROAD.name),
    (PLATFORM_TYPE.PLATFORM_TECH.name, PLATFORM_TYPE.PLATFORM_TECH.value, PLATFORM_TYPE.PLATFORM_TECH.name),
    (PLATFORM_TYPE.PLATFORM_DIRT.name, PLATFORM_TYPE.PLATFORM_DIRT.value, PLATFORM_TYPE.PLATFORM_DIRT.name),
    (PLATFORM_TYPE.PLATFORM_ICE.name, PLATFORM_TYPE.PLATFORM_ICE.value, PLATFORM_TYPE.PLATFORM_ICE.name),
    (PLATFORM_TYPE.PLATFORM_GRASS.name, PLATFORM_TYPE.PLATFORM_GRASS.value, PLATFORM_TYPE.PLATFORM_GRASS.name),
    (PLATFORM_TYPE.PLATFORM_PLASTIC.name, PLATFORM_TYPE.PLATFORM_PLASTIC.value, PLATFORM_TYPE.PLATFORM_GRASS.name),
)

ALL_ITEMS_TYPES = ROAD_TYPES + PLATFORM_TYPES

SINGLE_ROAD_TYPES = ROAD_TYPES + (
    (ROAD_TYPE.ROAD_TECH_ICE.name, ROAD_TYPE.ROAD_TECH_ICE.value, ROAD_TYPE.ROAD_TECH_ICE.name),
)

ROAD_SIDE_SHAPES = (
    (SIDE_SHAPE.FLAT.name, SIDE_SHAPE.FLAT.value, SIDE_SHAPE.FLAT.name),
    (SIDE_SHAPE.HALFBANKED_LEFT.name, SIDE_SHAPE.HALFBANKED_LEFT.value, SIDE_SHAPE.HALFBANKED_LEFT.name),
    (SIDE_SHAPE.HALFBANKED_RIGHT.name, SIDE_SHAPE.HALFBANKED_RIGHT.value, SIDE_SHAPE.HALFBANKED_RIGHT.name),
    (SIDE_SHAPE.BI_SLOPE_DOWN.name, SIDE_SHAPE.BI_SLOPE_DOWN.value, SIDE_SHAPE.BI_SLOPE_DOWN.name),
    (SIDE_SHAPE.BI_SLOPE_UP.name, SIDE_SHAPE.BI_SLOPE_UP.value, SIDE_SHAPE.BI_SLOPE_DOWN.name),
)

PLATFORM_SIDE_SHAPES = ROAD_SIDE_SHAPES + (
    (SIDE_SHAPE.BANKED_LEFT.name, SIDE_SHAPE.BANKED_LEFT.value, SIDE_SHAPE.BANKED_LEFT.name),
    (SIDE_SHAPE.BANKED_RIGHT.name, SIDE_SHAPE.BANKED_RIGHT.value, SIDE_SHAPE.BANKED_RIGHT.name),
    (SIDE_SHAPE.SLOPE_UP.name, SIDE_SHAPE.SLOPE_UP.value, SIDE_SHAPE.SLOPE_UP.name),
    (SIDE_SHAPE.SLOPE_DOWN.name, SIDE_SHAPE.SLOPE_DOWN.value, SIDE_SHAPE.SLOPE_DOWN.name),
)

ALL_SIDE_SHAPES = PLATFORM_SIDE_SHAPES

MIDDLE_SHAPES = (
    (MIDDLE_SHAPE.STRAIGHT.name, MIDDLE_SHAPE.STRAIGHT.value, MIDDLE_SHAPE.STRAIGHT.name),
    (MIDDLE_SHAPE.CHICANE.name, MIDDLE_SHAPE.CHICANE.value, MIDDLE_SHAPE.CHICANE.name),
    (MIDDLE_SHAPE.TURN.name, MIDDLE_SHAPE.TURN.value, MIDDLE_SHAPE.TURN.name),
)

class ShapeGeneratorProperties(PropertyGroup):
    generation_source: EnumProperty(
        items=(
            ("ROAD", "Road", "Generate road item"),
            ("PLATFORM", "Platform", "Generate platform item"),
            ("SHAPE", "Shape", "Generate shape only"),
            ("CUSTOM", "Custom", "Generate shape from custom object"),
        ),
        name="Type of object",
        default="ROAD",
    )
    generation_road_source: EnumProperty(
        items=(
            ("SINGLE", "Single surface", "Only one surface"),
            ("TRANSITION", "Surface transition", "Different start and end surface"),
        ),
        name="Single or transitional road surface",
        default="TRANSITION",
    )
    middle_shape: EnumProperty(
        items=MIDDLE_SHAPES,
        name="Middle shape",
        default=MIDDLE_SHAPE.STRAIGHT.name,
    )
    turn_direction: EnumProperty(
        items=(
            ("RIGHT", "Right", "Right turn"),
            ("LEFT", "Left", "Left turn"),
        ),
        name="Turn durection",
        default="RIGHT",
    )
    # ROAD
    road_single_type: EnumProperty(
        items=SINGLE_ROAD_TYPES,
        name="Road type",
        default=ROAD_TYPE.ROAD_TECH.name,
    )
    road_start_type: EnumProperty(
        items=ROAD_TYPES,
        name="Start road type",
        default=ROAD_TYPE.ROAD_TECH.name,
    )
    road_start_shape: EnumProperty(
        items=ROAD_SIDE_SHAPES,
        name="Start road shape",
        default=SIDE_SHAPE.FLAT.name,
    )
    road_end_type: EnumProperty(
        items=ROAD_TYPES,
        name="End road type",
        default=ROAD_TYPE.ROAD_TECH.name,
    )
    road_end_shape: EnumProperty(
        items=ROAD_SIDE_SHAPES,
        name="End road shape",
        default=SIDE_SHAPE.FLAT.name,
    )
    # PLATFORM
    platform_single_type: EnumProperty(
        items=PLATFORM_TYPES,
        name="Platform type",
        default=PLATFORM_TYPE.PLATFORM_TECH.name,
    )
    platform_start_shape: EnumProperty(
        items=PLATFORM_SIDE_SHAPES,
        name="Start road shape",
        default=SIDE_SHAPE.FLAT.name,
    )
    platform_end_shape: EnumProperty(
        items=PLATFORM_SIDE_SHAPES,
        name="End road shape",
        default=SIDE_SHAPE.FLAT.name,
    )
    # CUSTOM
    custom_object: PointerProperty(type=bpy.types.Object)
    custom_start_shape: EnumProperty(
        items=ALL_SIDE_SHAPES,
        name="Start custom shape",
        default=SIDE_SHAPE.FLAT.name,
    )
    custom_end_shape: EnumProperty(
        items=ALL_SIDE_SHAPES,
        name="End custom shape",
        default=SIDE_SHAPE.FLAT.name,
    )
    custom_shape_height: IntProperty(default=1, min=1)
    custom_should_scale_uv: BoolProperty(default=True, name="Scale UVs")
    # sets
    set_road_item_start_type: EnumProperty(
        items=ROAD_TYPES,
        name="Set item type",
        default=ROAD_TYPE.ROAD_TECH.name,
    )
    set_road_item_end_type: EnumProperty(
        items=ROAD_TYPES,
        name="Set item type",
        default=ROAD_TYPE.ROAD_TECH.name,
    )
    # REST
    shift_on_x: IntProperty(default=0)
    shift_on_y: IntProperty(default=1, min=1)
    shift_on_z: IntProperty(default=0)
    # global
    has_all_assets_loaded: BoolProperty(default=False, name="Has all needed assets loaded")