import bpy
import typing
from mathutils import Vector
from .Prefabs import get_lattice_prefab
from .Constants import (SIDE_SHAPE, MIDDLE_SHAPE, SIDE_SHAPE_BASE)
from .BlenderUtils import (
    duplicate_object_to_collection,
    apply_lattice_on_object,
    duplicate_lattice,
    delete_objects,
)
from .TrackmaniaUtils import (
    make_flat_bottom,
    scale_object_uv,
)
from .ShapeGeneratorUtils import (
    set_lattice_center_chicane_curve,
    set_side_curves_end_banked_shape,
    set_curves_start_banked_shape,
    set_curves_into_straight,
    set_curves_chicane_shape,
    set_lattice_side_curves,
    set_curves_slope_shape,
    get_grid_object_height,
    set_curves_end_shift,
    set_curves_into_turn,
)

def create_item(
    source_object: bpy.types.Object,
    dest_collection: bpy.types.Collection,
    middle_shape: MIDDLE_SHAPE,
    start_shape: SIDE_SHAPE,
    end_shape: SIDE_SHAPE,
    shift_xyz: typing.Tuple[int,int,int],
    name: str = "new-item",
    uv_scale_factor: int = 1,
    uv_material_settings: dict[str, typing.Tuple[Vector, Vector]] = None,
    should_make_flat_bottom: bool = False,
    should_delete_shape_objects: bool = True,
) -> bpy.types.Object:
    new_object = duplicate_object_to_collection(source_object, dest_collection)
    new_object.location = (0, 0, 0)
    new_object.name = f"{name}"

    if uv_scale_factor > 1:
        scale_object_uv(
            new_object,
            "BaseMaterial",
            uv_scale_factor,
            uv_material_settings,
        )

    item_lattice, shape_objects = create_item_shape(
        source_object,
        dest_collection,
        middle_shape,
        start_shape,
        end_shape,
        shift_xyz,
        name,
    )

    # apply lattice shape on the new object
    new_object = apply_lattice_on_object(new_object, item_lattice)
    
    # clean up lattice and curves
    if should_delete_shape_objects:
        delete_objects(shape_objects)

    if should_make_flat_bottom:
        make_flat_bottom(new_object, shift_xyz[2])

    return new_object

def create_item_shape(
    source_object: bpy.types.Object,
    dest_collection: bpy.types.Collection,
    middle_shape: MIDDLE_SHAPE,
    start_shape: SIDE_SHAPE,
    end_shape: SIDE_SHAPE,
    shift_xyz: typing.Tuple[int,int,int],
    name: str = "new-item",
    source_height: int = 8,
) -> typing.Tuple[bpy.types.Object, list[bpy.types.Object]]:
    object_height = source_height if source_object is None else get_grid_object_height(source_object)
    shape_objects:list[bpy.types.Object] = []

    # prepare lattices and curves
    item_lattice = duplicate_lattice(dest_collection, get_lattice_prefab(), (0, 0, 0), object_height)
    item_lattice.name = name + "_lattice"
    item_lattice.scale = (32, 32, object_height)
    shape_objects.append(item_lattice)
    
    # add curves modifiers to the lattice
    curves = set_lattice_side_curves(item_lattice, object_height)
    shape_objects = shape_objects+list(curves.values())

    # set curves middle shape (chicane later)
    if middle_shape == MIDDLE_SHAPE.TURN:
        curves = set_curves_into_turn(curves, shift_xyz[1], "Left" if shift_xyz[0] < 0 else "Right")
    elif middle_shape == MIDDLE_SHAPE.CHICANE:
        if SIDE_SHAPE_BASE.SLOPE.value not in start_shape.value and SIDE_SHAPE_BASE.SLOPE.value not in end_shape.value and shift_xyz[0] < shift_xyz[1]:
            curves = set_curves_into_straight(curves, shift_xyz[1])
            center_curve = set_lattice_center_chicane_curve(item_lattice, shift_xyz[0], shift_xyz[1])
            shape_objects.append(center_curve)
        else:
            curves = set_curves_chicane_shape(curves, shift_xyz[0], shift_xyz[1])
    else:
        curves = set_curves_into_straight(curves, shift_xyz[1])

    if SIDE_SHAPE_BASE.BANKED.value in start_shape.value:
        curves = set_curves_start_banked_shape(curves, start_shape)

    if SIDE_SHAPE_BASE.BANKED.value in end_shape.value:
        curves = set_side_curves_end_banked_shape(curves, end_shape)

    if SIDE_SHAPE_BASE.SLOPE.value in start_shape.value or SIDE_SHAPE_BASE.SLOPE.value in end_shape.value:
        curves = set_curves_slope_shape(curves, start_shape, end_shape)

    curves = set_curves_end_shift(curves, shift_xyz[2])

    return item_lattice, shape_objects