import bpy
from ..generator.Constants import (
    ROAD_TYPE,
    PLATFORM_TYPE,
    shorten_item_type,
)

MATERIALS_ORDER = {
    ROAD_TYPE.ROAD_TECH:            1,
    ROAD_TYPE.ROAD_DIRT:            2,
    ROAD_TYPE.ROAD_BUMP:            3,
    ROAD_TYPE.ROAD_ICE:             4,
    ROAD_TYPE.ROAD_TECH_ICE:        5,
    PLATFORM_TYPE.PLATFORM_TECH:    10,
    PLATFORM_TYPE.PLATFORM_DIRT:    11,
    PLATFORM_TYPE.PLATFORM_ICE:     12,
    PLATFORM_TYPE.PLATFORM_GRASS:   13,
    PLATFORM_TYPE.PLATFORM_PLASTIC: 14,
    ROAD_TYPE.BLAD_ROAD_NARROW:     20,
    PLATFORM_TYPE.BLACK_ROAD:       21,
}

letters_order = ["W","V","U","T","S","R","Q","P","O","N","M","L","K","J","I","H","G","F","E","D","C","B","A","9","8","7","6","5","4","3","2","1"]

def get_order_prefix(first: int, second: int = 0) -> str:
    if first < 1:
        first = 1
    
    if second < 0:
        second =  0

    second_prefix = letters_order[second-1] if second > 0 else ""

    return f"{letters_order[first-1]}{second_prefix}_"

def get_item_type_collection_name(item_type: ROAD_TYPE | PLATFORM_TYPE):
    return get_order_prefix(MATERIALS_ORDER[item_type])+shorten_item_type(item_type)

def create_item_type_collection(item_type: ROAD_TYPE | PLATFORM_TYPE) -> bpy.types.Collection:
    collection_name = get_item_type_collection_name(item_type)
    if collection_name in bpy.data.collections:
        return bpy.data.collections[collection_name]
    
    item_type_collection = create_collection_in(bpy.context.scene.collection, collection_name)

    return item_type_collection

def create_collection_in(dest_collection: bpy.types.Collection, name: str) -> bpy.types.Collection:
    coll = bpy.context.blend_data.collections.new(name=name)
    dest_collection.children.link(coll)
    return coll

def increment_position(pos: list[float], on_x: int = 0, on_y: int = 0) -> list[float]:
    if on_x != 0:
        pos[0] = pos[0] + 32*on_x
    if on_y != 0:
        pos[1] = pos[1] + 32*on_y
    
    return pos