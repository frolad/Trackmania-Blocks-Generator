import bpy
import typing
from mathutils import Vector
from .utils import (
    letters_order,
    get_order_prefix,
    increment_position,
    create_collection_in,
)
from ..generator.Prefabs import get_road_prefab
from ..generator.Constants import (
    ROAD_TYPE,
    SIDE_SHAPE,
    MIDDLE_SHAPE,
    SIDE_SHAPE_BASE,
    shorten_item_type,
    shorten_shape_name,
    prepare_item_name,
    shorten_road_start_end,
    prepare_item_base_name,
)
from ..generator.ShapeGenerator import create_item

def _generate_road_item(
    start:                      typing.Tuple[ROAD_TYPE, SIDE_SHAPE],
    end:                        typing.Tuple[ROAD_TYPE, SIDE_SHAPE],
    middle_shape:               MIDDLE_SHAPE,
    shift_xyz:                  typing.Tuple[int,int,int],
    dest_collection:            bpy.types.Collection,
    position:                   list[float],
    order:                      int,
    second_order:               int = 0,
    ignore_both_ways:           bool = False,
    ignore_collection_creation: bool = False,
) -> bpy.types.Object: 
    collection_name = get_order_prefix(order, second_order)+shorten_road_start_end(start[0], end[0])+"_"+prepare_item_name(middle_shape, start[1], end[1], shift_xyz)
    item_collection = bpy.context.blend_data.collections.new(name=collection_name)
    dest_collection.children.link(item_collection)

    #is_same_both_ways = False
    #if start[0] != end[0] and shift_xyz[2] == 0:
    #    if start[1] == end[1] and start[1] == SIDE_SHAPE.FLAT:
    #        is_same_both_ways = True

    #if not is_same_both_ways and not ignore_both_ways:
    #    _generate_road_item((start[0], start[1]), (end[0], end[1]), middle_shape, shift_xyz, item_collection, position, order=1, second_order=1, ignore_both_ways=True)
    #    position = [position[0]-32*shift_xyz[1]*2+32, position[1], position[2]]
    #    _generate_road_item((end[0], start[1]), (start[0], end[1]), middle_shape, shift_xyz, item_collection, position, order=1, second_order=2, ignore_both_ways=True)
    #    return item_collection

    source_object = get_road_prefab(start, end)
    if source_object is None:
        return "no object for this shape"


    has_bottom_vertices = True if "_bottom_vertices" in source_object.vertex_groups else None
    uv_scale_factor = shift_xyz[1] if middle_shape != MIDDLE_SHAPE.TURN else shift_xyz[1] + 1

    new_item = create_item(
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
    )

    new_item.location = (position[0], position[1], position[2])
    return item_collection


def _generate_road_variants(
    start_type:      ROAD_TYPE,
    end_type:        ROAD_TYPE,
    dest_collection: bpy.types.Collection,
    position:        list[float],
    middle_shape:    MIDDLE_SHAPE,
    start_shape:     SIDE_SHAPE,
    end_shape:       SIDE_SHAPE,
    shift_on_x:      int,
    shifts_on_y:     list[int],
    shifts_on_z:     list[int],
    order:           int,
):
    shift_z_order = 1
    root_name = shorten_road_start_end(start_type, end_type)
    shape_collection_name = get_order_prefix(order)+root_name+f"_{shorten_shape_name(middle_shape)}_{shorten_shape_name(start_shape, True)}_{shorten_shape_name(end_shape, True)}"
    if shape_collection_name in dest_collection.children:
        shape_collection = dest_collection.children[shape_collection_name]
        for sub in shape_collection.children:
            shift_z_order = letters_order.index(sub.name.split("_")[0]) + 2
    else:
        shape_collection = create_collection_in(dest_collection, shape_collection_name)
        

    for shift_on_z in shifts_on_z:
        sizes_collection_name = get_order_prefix(shift_z_order)+root_name+"_"+prepare_item_base_name(middle_shape, start_shape, end_shape, (shift_on_x, 0, shift_on_z))
        sizes_collection = create_collection_in(shape_collection, sizes_collection_name)

        shift_y_index = 1
        for shift_on_y in shifts_on_y:
            if middle_shape == MIDDLE_SHAPE.TURN:
                shift_on_x = (1 if shift_on_x > 0 else -1 ) * shift_on_y

            new_item_collection = _generate_road_item(
                start                      = (start_type, start_shape),
                end                        = (end_type, end_shape),
                middle_shape               = middle_shape,
                shift_xyz                  = (shift_on_x, shift_on_y, shift_on_z),
                dest_collection            = sizes_collection,
                position                   = [position[0] + shift_y_index*32, position[1], position[2]],
                order                      = shift_y_index,
            )
            print("Created "+new_item_collection.name)

            shift_y_index = shift_y_index + 1
        
        position = increment_position(position, +0, +7)  
        shift_z_order = shift_z_order + 1

    return position



def generate_road_base_transitions(start_type: ROAD_TYPE, end_type: ROAD_TYPE):
    pos = [48, 48, 0]

    root_name = shorten_road_start_end(start_type, end_type)
    root_coll = create_collection_in(bpy.context.scene.collection, root_name)

    # STRAIGHT FLAT
    start_shape_coll = create_collection_in(root_coll, get_order_prefix(1, 1)+root_name+f"_{MIDDLE_SHAPE.STRAIGHT.value}_{SIDE_SHAPE.FLAT.value}Start")
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.FLAT, SIDE_SHAPE.FLAT,                             +0, [1,2,3,4], [+2, +1, +0], 1)
    if end_type != ROAD_TYPE.ROAD_ICE:
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.FLAT, SIDE_SHAPE.HALFBANKED_RIGHT,             +0, [1,2,3,4], [+0, -1],     2)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.FLAT, SIDE_SHAPE.HALFBANKED_LEFT,              +0, [1,2,3,4], [+0, -1],     3)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.FLAT, SIDE_SHAPE.BI_SLOPE_UP,                      +0, [2,3,4],   [+2],         4)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.FLAT, SIDE_SHAPE.BI_SLOPE_UP,                      +0, [1,2,3],   [+1],         4)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.FLAT, SIDE_SHAPE.BI_SLOPE_DOWN,                    +0, [2,3,4],   [-2],         5)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.FLAT, SIDE_SHAPE.BI_SLOPE_DOWN,                    +0, [1,2,3],   [-1],         5)

    # STRAIGHT HALF BANKED
    start_shape_coll = create_collection_in(root_coll, get_order_prefix(1, 2)+root_name+f"_{MIDDLE_SHAPE.STRAIGHT.value}_{SIDE_SHAPE_BASE.HALFBANKED.value}Start")
    if start_type != ROAD_TYPE.ROAD_ICE and end_type != ROAD_TYPE.ROAD_ICE:
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.HALFBANKED_LEFT, SIDE_SHAPE.HALFBANKED_LEFT,   +0, [1,2,3,4], [+0], 1)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.HALFBANKED_RIGHT, +0, [1,2,3,4], [+0], 2)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.HALFBANKED_LEFT,  +0, [1,2,3,4], [+0], 3)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.HALFBANKED_LEFT,  SIDE_SHAPE.HALFBANKED_RIGHT, +0, [1,2,3,4], [+0], 4)
    if start_type != ROAD_TYPE.ROAD_ICE:
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.BI_SLOPE_UP,      +0, [2,3,4],   [+3], 5)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.BI_SLOPE_UP,      +0, [1,2,3],   [+2], 5)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.HALFBANKED_LEFT,  SIDE_SHAPE.BI_SLOPE_UP,      +0, [2,3,4],   [+3], 6)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.HALFBANKED_LEFT,  SIDE_SHAPE.BI_SLOPE_UP,      +0, [1,2,3],   [+2], 6)

    # STRAIGHT BI SLOPE
    start_shape_coll = create_collection_in(root_coll, get_order_prefix(1, 3)+root_name+f"_{MIDDLE_SHAPE.STRAIGHT.value}_{SIDE_SHAPE_BASE.SLOPE.value}Start")
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.BI_SLOPE_UP, SIDE_SHAPE.BI_SLOPE_UP,               +0, [1], [+1], 1)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.BI_SLOPE_UP, SIDE_SHAPE.BI_SLOPE_UP,               +0, [2], [+2], 1)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.BI_SLOPE_UP, SIDE_SHAPE.BI_SLOPE_UP,               +0, [3], [+3], 1)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.BI_SLOPE_DOWN, SIDE_SHAPE.BI_SLOPE_DOWN,           +0, [1], [-1], 1)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.BI_SLOPE_DOWN, SIDE_SHAPE.BI_SLOPE_DOWN,           +0, [2], [-2], 1)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.BI_SLOPE_DOWN, SIDE_SHAPE.BI_SLOPE_DOWN,           +0, [3], [-3], 1)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.BI_SLOPE_UP, SIDE_SHAPE.BI_SLOPE_DOWN,             +0, [1,2,3,4], [+0], 2)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.STRAIGHT, SIDE_SHAPE.BI_SLOPE_DOWN, SIDE_SHAPE.BI_SLOPE_UP,             +0, [1,2,3,4], [+0], 3)

    pos = [48+32*10, 48, 0]

    # CHICANE FLAT
    start_shape_coll = create_collection_in(root_coll, get_order_prefix(2, 1)+root_name+f"_{MIDDLE_SHAPE.CHICANE.value}_{SIDE_SHAPE.FLAT.value}Start")
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.FLAT, SIDE_SHAPE.FLAT,                              -1, [2, 3, 4], [+1, 0], 1)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.FLAT, SIDE_SHAPE.FLAT,                              +1, [2, 3, 4], [+1, 0], 1)
    if end_type != ROAD_TYPE.ROAD_ICE:
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.FLAT, SIDE_SHAPE.HALFBANKED_RIGHT,              -1, [2, 3, 4], [+0, -1], 2)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.FLAT, SIDE_SHAPE.HALFBANKED_LEFT,               +1, [2, 3, 4], [+0, -1], 3)
    _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.FLAT, SIDE_SHAPE.BI_SLOPE_UP,                             +1, [2, 3, 4], [+2, +1], 4)
    _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.FLAT, SIDE_SHAPE.BI_SLOPE_DOWN,                           +1, [2, 3, 4], [-1, -2], 4)
    _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.FLAT, SIDE_SHAPE.BI_SLOPE_UP,                             -1, [2, 3, 4], [+2, +1], 5)
    _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.FLAT, SIDE_SHAPE.BI_SLOPE_DOWN,                           -1, [2, 3, 4], [-1, -2], 5)

    # CHICANE HALF BANKED
    start_shape_coll = create_collection_in(root_coll, get_order_prefix(2, 2)+root_name+f"_{MIDDLE_SHAPE.CHICANE.value}_{SIDE_SHAPE_BASE.HALFBANKED.value}Start")
    if start_type != ROAD_TYPE.ROAD_ICE and end_type != ROAD_TYPE.ROAD_ICE:
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.HALFBANKED_LEFT,   +1, [2, 3, 4], [+0], 1)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.HALFBANKED_LEFT,  SIDE_SHAPE.HALFBANKED_RIGHT,  -1, [2, 3, 4], [+0], 2)
    if start_type != ROAD_TYPE.ROAD_ICE:
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.BI_SLOPE_UP,       +1, [2, 3, 4], [+2], 3)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.BI_SLOPE_UP,       -1, [2, 3, 4], [+2], 4)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.HALFBANKED_LEFT,  SIDE_SHAPE.BI_SLOPE_UP,       +1, [2, 3, 4], [+2], 5)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.CHICANE, SIDE_SHAPE.HALFBANKED_LEFT,  SIDE_SHAPE.BI_SLOPE_UP,       -1, [2, 3, 4], [+2], 6)

    pos = [48+32*20, 48, 0]
    
    # TURN FLAT
    start_shape_coll = create_collection_in(root_coll, get_order_prefix(3, 1)+root_name+f"_{MIDDLE_SHAPE.TURN.value}_{SIDE_SHAPE.FLAT.value}Start")
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.FLAT,                                 +1, [2,3,4,5],   [+2, +1], 1)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.FLAT,                                 +1, [1,2,3,4,5], [+0],     1)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.FLAT,                                 -1, [2,3,4,5],   [+2, +1], 1)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.FLAT,                                 -1, [1,2,3,4,5], [+0],     1)
    if end_type != ROAD_TYPE.ROAD_ICE:
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.HALFBANKED_RIGHT,                 +1, [2,3,4,5],   [+1],     2)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.HALFBANKED_RIGHT,                 +1, [1,2,3,4,5], [+0],     2)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.HALFBANKED_RIGHT,                 +1, [2,3,4,5],   [-1, -2], 2)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.HALFBANKED_LEFT,                  -1, [2,3,4,5],   [+1],     3)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.HALFBANKED_LEFT,                  -1, [1,2,3,4,5], [+0],     3)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.HALFBANKED_LEFT,                  -1, [2,3,4,5],   [-1, -2], 3)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.BI_SLOPE_UP,                          +1, [2,3,4,5],   [+2, +1], 4)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.BI_SLOPE_DOWN,                        +1, [2,3,4,5],   [-1, -2], 4)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.BI_SLOPE_UP,                          -1, [2,3,4,5],   [+2, +1], 5)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.FLAT, SIDE_SHAPE.BI_SLOPE_DOWN,                        -1, [2,3,4,5],   [-1, -2], 5)


    # TURN HALF BANKED
    start_shape_coll = create_collection_in(root_coll, get_order_prefix(3, 2)+root_name+f"_{MIDDLE_SHAPE.TURN.value}_{SIDE_SHAPE_BASE.HALFBANKED.value}Start")
    if start_type != ROAD_TYPE.ROAD_ICE and end_type != ROAD_TYPE.ROAD_ICE:
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.HALFBANKED_RIGHT,     +1, [1,2,3,4,5], [0], 1)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_LEFT,  SIDE_SHAPE.HALFBANKED_LEFT,      -1, [1,2,3,4,5], [0], 2)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.HALFBANKED_RIGHT,     -1, [1,2,3,4,5], [0], 3)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_LEFT, SIDE_SHAPE.HALFBANKED_LEFT,       +1, [1,2,3,4,5], [0], 4)
    if start_type != ROAD_TYPE.ROAD_ICE:
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.BI_SLOPE_UP,          +1, [2,3,4,5],   [+2, +1], 5)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.BI_SLOPE_DOWN,        +1, [1],         [+0],     5)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.BI_SLOPE_DOWN,        +1, [2],         [-1],     5)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.BI_SLOPE_UP,          -1, [2],         [+2],     5)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_RIGHT, SIDE_SHAPE.BI_SLOPE_UP,          -1, [1],         [+1],     5)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_LEFT, SIDE_SHAPE.BI_SLOPE_UP,           -1, [2,3,4,5],   [+2, +1], 6)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_LEFT, SIDE_SHAPE.BI_SLOPE_DOWN,         -1, [1],         [+0],     6)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_LEFT, SIDE_SHAPE.BI_SLOPE_DOWN,         -1, [2],         [-1],     6)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_LEFT, SIDE_SHAPE.BI_SLOPE_UP,           +1, [2],         [+2],     6)
        pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.HALFBANKED_LEFT, SIDE_SHAPE.BI_SLOPE_UP,           +1, [1],         [+1],     6)

    # TURN BI SLOPE
    start_shape_coll = create_collection_in(root_coll, get_order_prefix(3, 3)+root_name+f"_{MIDDLE_SHAPE.TURN.value}_{SIDE_SHAPE_BASE.SLOPE.value}Start")
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.BI_SLOPE_DOWN, SIDE_SHAPE.BI_SLOPE_UP,                 -1, [2,3,4,5], [0], 1)
    pos = _generate_road_variants(start_type, end_type, start_shape_coll, pos, MIDDLE_SHAPE.TURN, SIDE_SHAPE.BI_SLOPE_UP,   SIDE_SHAPE.BI_SLOPE_DOWN,               -1, [2,3,4,5], [0], 2)