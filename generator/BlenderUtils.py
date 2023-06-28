import bpy
from mathutils import Vector

def move_obj_to_collection(obj: bpy.types.Object, dest_coll: bpy.types.Collection):
    objs:list[obj] = [obj]
    for sub in obj.children:
        objs.append(sub)

    for obj in objs:
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
    
        dest_coll.objects.link(obj)
    
def duplicate_object(obj: bpy.types.Object):
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()
    new_obj.animation_data_clear()
    
    return new_obj

def duplicate_object_to_collection(obj: bpy.types.Object, dest_coll: bpy.types.Collection):
    newObj = duplicate_object(obj)
    move_obj_to_collection(newObj, dest_coll)
    return newObj

def scale_2D(v: list[float], s: Vector, p: Vector):
    return (p[0] + s[0]*(v[0] - p[0]), p[1] + s[1]*(v[1] - p[1]))     

def duplicate_lattice(coll: bpy.types.Collection, lattice: bpy.types.Lattice, pos: list[float], lattice_height: int = 2) -> bpy.types.Object:
    lattice = duplicate_object_to_collection(lattice, coll)
    lattice.location = (pos[0], pos[1], pos[2] + lattice_height/2)

    return lattice

def get_number_sign(val: int) -> int:
    return 1 if val >= 0 else -1

def apply_on_object(obj: bpy.types.Object, location=False, rotation=False, scale=False):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=location, rotation=rotation, scale=scale)
    bpy.ops.object.select_all(action='DESELECT')

def apply_lattice_on_object(obj: bpy.types.Object, lattice: bpy.types.Object) -> bpy.types.Object:
    mod = obj.modifiers.new("Lattice", 'LATTICE')
    mod.object = lattice

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj

    for mod in obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=mod.name)

    bpy.ops.object.select_all(action='DESELECT')

    return obj

def apply_mods_on_object(obj: bpy.types.Object) -> bpy.types.Object:
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj

    for mod in obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=mod.name)

    bpy.ops.object.select_all(action='DESELECT')

    return obj

def delete_objects(lsit: list[bpy.types.Object]):
    for obj in lsit:
        if obj is not None:
            bpy.data.objects.remove(obj, do_unlink=True)

    return []

def set_object_origin(obj: bpy.types.Object, pos: list[float]):
    bpy.context.scene.cursor.location = (pos[0]+16, pos[1]+16, pos[2])
    bpy.ops.object.select_all(action='DESELECT')
    
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')
    obj.select_set(False)

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.cursor.location = (0,0,0)

def add_lattice_side_curve_modifier(lattice: bpy.types.Object, source_curve: bpy.types.Object, name: str, lattice_height: int = 2) -> bpy.types.Curve:
    coll = lattice.users_collection[0]
    new_curve = duplicate_object_to_collection(source_curve, coll)
    new_curve.name = lattice.name.replace("_lattice", "_curve_") + name

    pos_shift_on_x = 16 if "Right" in name else -16
    pos_shift_on_y = -16
    pos_shift_on_z = (lattice_height/2)*(1 if "Top" in name else -1)

    new_curve.location = (lattice.location[0]+pos_shift_on_x, lattice.location[1]+pos_shift_on_y, lattice.location[2]+pos_shift_on_z)

    mod = lattice.modifiers.new(name+"_curve", 'CURVE')
    mod.deform_axis = "POS_Y"
    mod.object = new_curve
    mod.vertex_group = "ScriptBaseLattice"+name

    return new_curve

def add_lattice_middle_curve_modifier(lattice: bpy.types.Object, source_curve: bpy.types.Object) -> bpy.types.Curve:
    coll = lattice.users_collection[0]
    new_curve = duplicate_object_to_collection(source_curve, coll)
    new_curve.name = lattice.name.replace("_lattice", "_curve_middle") 

    new_curve.location = (
        lattice.location[0],
        lattice.location[1]-16,
        lattice.location[2],
    )

    mod = lattice.modifiers.new("middle_curve", 'CURVE')
    mod.deform_axis = "POS_Y"
    mod.object = new_curve

    return new_curve