import bpy
import math
from .Prefabs import get_curve_prefab
from .Constants import (
    SIDE_SHAPE,
    SIDE_SHAPE_BASE,
    TURN_CURVE_HANDLE_COEF,
)
from .BlenderUtils import (
    add_lattice_side_curve_modifier,
    duplicate_object_to_collection,
    get_number_sign,
    apply_on_object,
)

def get_grid_object_height(obj: bpy.types.Object) -> int:
    height = math.ceil(obj.dimensions[2])
    if height % 2 == 1:
        height = height + 1

    return height

def set_lattice_side_curves(lattice: bpy.types.Object, lattice_height: int = 2) -> dict[str, bpy.types.Curve]:
    curves:dict[str, bpy.types.Curve] = {
        "TopLeft": None,
        "TopRight": None,
        "BottomLeft": None,
        "BottomRight": None
    }

    for key in curves.keys():
        curves[key] = add_lattice_side_curve_modifier(lattice, get_curve_prefab(), key, lattice_height)

    return curves

def set_curves_y_size(curves: dict[str, bpy.types.Curve], end_shift_on_y: int) -> dict[str, bpy.types.Curve]:
    for key in curves.keys():
        curves[key].scale = (1, end_shift_on_y, 1)

    return curves

def set_curves_into_straight(curves: dict[str, bpy.types.Curve], size: int) -> dict[str, bpy.types.Curve]:
    for key in curves.keys():
        for spline in curves[key].data.splines:
            for point in spline.bezier_points:
                point.handle_left_type = "FREE"
                point.handle_right_type = "FREE"

        curves[key].data.splines[0].bezier_points[0].handle_right.y = 12
        curves[key].data.splines[0].bezier_points[1].handle_left.y = 20

    return set_curves_y_size(curves, size)


def set_curves_into_turn(curves: dict[str, bpy.types.Curve], size: int, direction: str) -> dict[str, bpy.types.Curve]:
    direction = "Left" if direction == "Left" else "Right"

    for key in curves.keys():
        curves[key] = _set_curve_into_turn(curves[key], direction)
        if direction in key:
            # 1x1 turns are tricky, stupid solution for that (probably should ignore scaling dat curves and just adjust lattice points, safer?)
            new_size = size - 1
            if new_size == 0:
                new_size = 0.00001
            curves[key].scale = (new_size, new_size, 1)
        else:
            curves[key].scale = (size, size, 1)

    return curves

def set_curves_start_banked_shape(curves: dict[str, bpy.types.Curve], start_shape: SIDE_SHAPE) -> dict[str, bpy.types.Curve]:
    shift = 8 if SIDE_SHAPE_BASE.HALFBANKED.value in start_shape.value else 16 if SIDE_SHAPE_BASE.BANKED.value in start_shape.value else 0

    for key in curves.keys():
        if ("Left" in start_shape.value and "Right" in key) or ("Right" in start_shape.value and "Left" in key):
            _shift_curve_point(curves[key].data.splines[0].bezier_points[0], "z", shift)


    return curves

def set_side_curves_end_banked_shape(curves: dict[str, bpy.types.Curve], end_shape: SIDE_SHAPE):
    shift = 8 if SIDE_SHAPE_BASE.HALFBANKED.value in end_shape.value else 16 if SIDE_SHAPE_BASE.BANKED.value in end_shape.value else 0

    for key in curves.keys():
        if ("Left" in end_shape.value and "Right" in key) or ("Right" in end_shape.value and "Left" in key):
            _shift_curve_point(curves[key].data.splines[0].bezier_points[1], "z", shift)

    return curves

def set_curves_slope_shape(curves: dict[str, bpy.types.Curve], start_shape: SIDE_SHAPE, end_shape: SIDE_SHAPE) -> dict[str, bpy.types.Curve]:
    for key in curves.keys():
        _set_curve_slope(curves[key], start_shape, end_shape)

    return curves

def set_curves_end_shift(curves: dict[str, bpy.types.Curve], end_shift_on_z: int) -> dict[str, bpy.types.Curve]:
    for key in curves.keys():
        _shift_curve_point(curves[key].data.splines[0].bezier_points[1], "z", 8*end_shift_on_z)

    return curves

def set_lattice_center_chicane_curve(lattice: bpy.types.Object, end_shift_on_x: int, end_shift_on_y: int) -> bpy.types.Curve:
    center_curve = duplicate_object_to_collection(get_curve_prefab(), lattice.users_collection[0])
    center_curve.location = (lattice.location[0], lattice.location[1]-lattice.dimensions[1]/2, lattice.location[2])
    center_curve.name = lattice.name.replace("_lattice", "_curve_center")

    for spline in center_curve.data.splines:
        for point in spline.bezier_points:
            point.tilt = 1.5708 # 90 deg
            point.handle_left_type = "FREE"
            point.handle_right_type = "FREE"

    start_point = center_curve.data.splines[0].bezier_points[0]
    end_point = center_curve.data.splines[0].bezier_points[1]

    start_point.co = (0,0, start_point.co.z)
    start_point.handle_left = (start_point.co.x, start_point.co.y, start_point.co.z)
    start_point.handle_right = (start_point.co.x, start_point.co.y, start_point.co.z)
    start_point.handle_right.y = 10

    end_point.co = (get_number_sign(end_shift_on_x)*abs(end_shift_on_x)*32, 32, end_point.co.z)
    end_point.handle_left = (end_point.co.x, end_point.co.y, end_point.co.z)
    end_point.handle_right = (end_point.co.x, end_point.co.y, end_point.co.z)
    end_point.handle_left.y = 22
    
    center_curve.scale = (1, end_shift_on_y, 1)

    apply_on_object(center_curve, scale=True)

    mod = lattice.modifiers.new("Center_curve", 'CURVE')
    mod.deform_axis = "POS_Y"
    mod.object = center_curve

    return center_curve

    
def set_curves_chicane_shape(curves: dict[str, bpy.types.Curve], end_shift_on_x: int, end_shift_on_y: int) -> dict[str, bpy.types.Curve]:
    for key in curves.keys():
        for spline in curves[key].data.splines:
            for point in spline.bezier_points:
                point.handle_left_type = "FREE"
                point.handle_right_type = "FREE"

        start_point = curves[key].data.splines[0].bezier_points[0]
        end_point = curves[key].data.splines[0].bezier_points[1]

        if end_shift_on_x > 0:
            if "Left" in key:
                start_point.handle_right.y = 13
            else:
                start_point.handle_right.y = 6
        else:
            if "Left" in key:
                start_point.handle_right.y = 6
            else:
                start_point.handle_right.y = 13

        end_point.co = (get_number_sign(end_shift_on_x)*abs(end_shift_on_x)*32, 32, end_point.co.z)
        end_point.handle_left = (end_point.co.x, end_point.co.y, end_point.co.z)
        end_point.handle_right = (end_point.co.x, end_point.co.y, end_point.co.z)
        if end_shift_on_x > 0:
            if "Left" in key:
                end_point.handle_left.y = 32 - 6
            else:
                end_point.handle_left.y = 32 - 13
        else:
            if "Left" in key:
                end_point.handle_left.y = 32 - 13
            else:
                end_point.handle_left.y = 32 - 6


    set_curves_y_size(curves, end_shift_on_y)

    return curves

def _set_curve_into_turn(curve: bpy.types.Curve, direction: str) -> bpy.types.Curve:
    direction = -1 if direction == "Left" else 1

    for spline in curve.data.splines:
        for point in spline.bezier_points:
            point.handle_left_type = "FREE"
            point.handle_right_type = "FREE"


    start_point = curve.data.splines[0].bezier_points[0]
    end_point = curve.data.splines[0].bezier_points[1]

    start_point.co = (0, 0, start_point.co.z)
    start_point.handle_left = (start_point.co.x, start_point.co.y, start_point.co.z)
    start_point.handle_right = (start_point.co.x, start_point.co.y, start_point.co.z)
    start_point.handle_right.y = 32/TURN_CURVE_HANDLE_COEF

    end_point.co = (direction*32, 32, end_point.co.z)
    end_point.handle_left = (end_point.co.x, end_point.co.y, end_point.co.z)
    end_point.handle_right = (end_point.co.x, end_point.co.y, end_point.co.z)
    end_point.handle_left.x = direction*32 - direction*32/TURN_CURVE_HANDLE_COEF

    return curve

def _set_curve_slope(curve: bpy.types.Curve, start_shape: SIDE_SHAPE, end_shape: SIDE_SHAPE):
    apply_on_object(curve, scale=True)

    if curve.dimensions.y == 0:
        return

    startPoint:bpy.types.BezierSplinePoint = curve.data.splines[0].bezier_points[0]
    endPoint:bpy.types.BezierSplinePoint = curve.data.splines[0].bezier_points[1]

    startDir = 1 if "Up" in start_shape.value else -1
    endDir = 1 if "Down" in end_shape.value else -1

    startPoint.handle_right.z = startPoint.handle_right.z + startDir*_get_slope_z(startPoint, start_shape, True)
    endPoint.handle_left.z = endPoint.handle_left.z + endDir*_get_slope_z(endPoint, end_shape, False)

def _get_slope_z(point: bpy.types.BezierSplinePoint, shape: SIDE_SHAPE, is_start: bool) -> int:
    if "Slope" not in shape.value:
        return 0

    if is_start:
        return (point.co - point.handle_right).length * math.tan(math.radians(14.03624 if "BiSlope" in shape.value else 26.56505))
    else:
        return (point.co - point.handle_left).length * math.tan(math.radians(14.03624 if "BiSlope" in shape.value else 26.56505))

def _shift_curve_point(point: bpy.types.BezierSplinePoint, on: str, val: int):
    point.handle_left_type = "FREE"
    point.handle_right_type = "FREE"

    onInt = 0 if on == "x" else 1 if on == "y" else 2

    point.co[onInt] += val
    point.handle_left[onInt] += val
    point.handle_right[onInt] += val