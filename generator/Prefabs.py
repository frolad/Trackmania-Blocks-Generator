import bpy
import typing
from .Constants import (ROAD_TYPE, PLATFORM_TYPE, SIDE_SHAPE, SIDE_SHAPE_BASE)

def get_lattice_prefab() -> bpy.types.Object:
    return bpy.data.objects["WTMTAssets_Lattice"]

def get_curve_prefab() -> bpy.types.Object:
    return bpy.data.objects["WTMTAssets_Curve"]

def get_road_prefab(
    start: typing.Tuple[ROAD_TYPE, SIDE_SHAPE],
    end: typing.Tuple[ROAD_TYPE, SIDE_SHAPE],
) -> bpy.types.Object:
    name = "WTMTAssets_"
    start_name = start[0].value
    end_name = end[0].value

    if start_name != end_name:
        start_name = start_name.replace("Narrow", "")
        end_name = end_name.replace("Narrow", "")

    if (start[0] == ROAD_TYPE.ROAD_DIRT or start[0] == ROAD_TYPE.ROAD_GRASS) and SIDE_SHAPE_BASE.HALFBANKED.value in start[1].value:
        start_name = f"{start_name}HB"

    if (end[0] == ROAD_TYPE.ROAD_DIRT or end[0] == ROAD_TYPE.ROAD_GRASS) and SIDE_SHAPE_BASE.HALFBANKED.value in end[1].value:
        end_name = f"{end_name}HB"


    if start_name == end_name:
        name += start_name
    else:
        name += f"{start_name}To{end_name}"

    print(name)
    if name in bpy.data.objects:
        return bpy.data.objects[name]
    
    return None

def get_platform_prefab(platform_type: PLATFORM_TYPE) -> bpy.types.Object:
    name = "WTMTAssets_"+platform_type.value
    if name in bpy.data.objects:
        return bpy.data.objects[name]