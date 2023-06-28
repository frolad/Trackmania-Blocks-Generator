import typing
from enum import Enum

class ROAD_TYPE(Enum):
    BLAD_ROAD_NARROW = "BlackRoadNarrow"
    ROAD_TECH        = "RoadTech"
    ROAD_BUMP        = "RoadBump"
    ROAD_DIRT        = "RoadDirt"
    ROAD_ICE         = "RoadIce"
    ROAD_GRASS       = "RoadGrass"
    ROAD_TECH_ICE    = "RoadTechIce"

class PLATFORM_TYPE(Enum):
    BLACK_ROAD       = "BlackRoad"
    PLATFORM_TECH    = "PlatformTech"
    PLATFORM_DIRT    = "PlatformDirt"
    PLATFORM_ICE     = "PlatformIce"
    PLATFORM_GRASS   = "PlatformGrass"
    PLATFORM_PLASTIC = "PlatformPlastic"

class MIDDLE_SHAPE(Enum):
    STRAIGHT = "Straight"
    CHICANE  = "Chicane"
    TURN     = "Turn"

class SIDE_SHAPE(Enum):
    FLAT             = "Flat"
    HALFBANKED_LEFT  = "HalfBankedLeft"
    HALFBANKED_RIGHT = "HalfBankedRight"
    BANKED_LEFT      = "BankedLeft"
    BANKED_RIGHT     = "BankedRight"
    BI_SLOPE_UP      = "BiSlopeUp"
    BI_SLOPE_DOWN    = "BiSlopeDown"
    SLOPE_UP         = "SlopeUp"
    SLOPE_DOWN       = "SlopeDown"

class SIDE_SHAPE_BASE(Enum):
    HALFBANKED       = "HalfBanked"
    BANKED           = "Banked"
    BI_SLOPE         = "BiSlope"
    SLOPE            = "Slope"

TURN_CURVE_HANDLE_COEF = 1.8111840615802580937287751867784

LETTERS_ORDER = ["W","V","U","T","S","R","Q","P","O","N","M","L","K","J","I","H","G","F","E","D","C","B","A","9","8","7","6","5","4","3","2","1"]

def shorten_road_type(road_type: ROAD_TYPE) -> str:
    return shorten_road_name(road_type.value)

def shorten_road_name(name: str) -> str:
    print(name)
    name = name.replace("WTMTAssets_", "")
    name = name.replace("Black", "B")
    name = name.replace("Narrow", "N")
    name = name.replace("Road", "R")
    name = name.replace("Tech", "T")
    name = name.replace("Bump", "B")
    name = name.replace("Dirt", "D")
    name = name.replace("Ice", "I")
    name = name.replace("Grass", "G")

    return name

def shorten_platform_type(platform_type: PLATFORM_TYPE) -> str:
    name = platform_type.value
    name = name.replace("WTMTAssets_", "")
    name = name.replace("Platform", "P")
    name = name.replace("Black", "B")
    name = name.replace("Tech", "T")
    name = name.replace("Dirt", "D")
    name = name.replace("Ice", "I")
    name = name.replace("Grass", "G")
    name = name.replace("Plastic", "P")

    return name

def shorten_item_type(item_type: PLATFORM_TYPE|ROAD_TYPE) -> str:
    if item_type in PLATFORM_TYPE:
        return shorten_platform_type(item_type)
    else:
        return shorten_road_type(item_type)
    
def shorten_road_start_end(start_type: ROAD_TYPE, end_type: ROAD_TYPE):
    if start_type == end_type:
        base_name = f"{shorten_road_type(start_type)}"
    else:
        base_name = f"{shorten_road_type(start_type)}-{shorten_road_type(end_type)}"

    return base_name

def shorten_shape_name(shape: MIDDLE_SHAPE | SIDE_SHAPE, ignore_bislope_direction:bool = False) -> str:
    if shape in SIDE_SHAPE:
        name = shape.value
        name = name.replace(SIDE_SHAPE_BASE.HALFBANKED.value, "HB")
        name = name.replace(SIDE_SHAPE_BASE.BANKED.value, "B")
        if ignore_bislope_direction:
            name = name.replace(SIDE_SHAPE.SLOPE_UP.value, "S")
            name = name.replace(SIDE_SHAPE.SLOPE_DOWN.value, "S")
        else:
            name = name.replace(SIDE_SHAPE.SLOPE_UP.value, "SU")
            name = name.replace(SIDE_SHAPE.SLOPE_DOWN.value, "SD")
        name = name.replace(SIDE_SHAPE_BASE.SLOPE.value, "S")
        return name
    elif shape in MIDDLE_SHAPE:
        return shape.value[0:3]

    return shape.value

def prepare_item_name(middle_shape: MIDDLE_SHAPE, start_shape: SIDE_SHAPE, end_shape: SIDE_SHAPE, shift_xyz: typing.Tuple[float, float, float]):
    collName = prepare_item_base_name(middle_shape, start_shape, end_shape, shift_xyz)
    return f"{collName}_Size{shift_xyz[1]}"

def prepare_item_base_name(middle_shape: MIDDLE_SHAPE, start_shape: str, end_shape: str, shift_xyz: typing.Tuple[float, float, float]):
    ZShape = "Even" if shift_xyz[2] == 0 else f"{'Up' if shift_xyz[2] > 0 else 'Down'}{abs(shift_xyz[2])}"
    XShape = "Center" if shift_xyz[0] == 0 else f"{'Right' if shift_xyz[0] > 0 else 'Left'}{abs(shift_xyz[0]) if middle_shape != MIDDLE_SHAPE.TURN else ''}"

    return f"{shorten_shape_name(middle_shape)}_{shorten_shape_name(start_shape)}_{shorten_shape_name(end_shape)}_{ZShape}_{XShape}"

def get_order_prefix(First: int, Second: int = 0) -> str:
    if First < 1:
        First = 1
    
    if Second < 0:
        Second =  0

    secondPrefix = LETTERS_ORDER[Second-1] if Second > 0 else ""

    return f"{LETTERS_ORDER[First-1]}{secondPrefix}_"

def enum_by_name(en:Enum, name: str):
    for enum in en:
        if enum.name == name:
            return enum
        
    return None