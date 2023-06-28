from .properties import ShapeGeneratorProperties
from .sets.GenerateRoadSet import (
    generate_road_base_transitions,
)
from .generator.Constants import (
    ROAD_TYPE,
    enum_by_name,
)

def generate_default_road_set(settings: ShapeGeneratorProperties):
    start_type = enum_by_name(ROAD_TYPE, settings.set_road_item_start_type)
    end_type = enum_by_name(ROAD_TYPE, settings.set_road_item_end_type)
    generate_road_base_transitions(start_type, end_type)