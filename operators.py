from bpy.types import Operator
from .properties import ShapeGeneratorProperties
from .utils import (
    assign_assets_file,
    load_assets_file,
)
from .GeneratorItem import (
    generate_road_item,
    generate_platform_item,
    generate_shape_item,
    generate_custom_item,
)
from .GeneratorSet import (
    generate_default_road_set,
)
from .GeneratorSet import (
    generate_default_road_set,
)
from .generator.Constants import (
    MIDDLE_SHAPE,
)


class VIEW3D_OT_GenerateItem(Operator):
    bl_idname = "object.tmgen_generate_trackmania_item"
    bl_label = "Generate item"

    def execute(self, context):
        settings:ShapeGeneratorProperties = context.scene.tm_shape_generator
        response = None

        if settings.middle_shape == MIDDLE_SHAPE.TURN.name:
            settings.shift_on_x = settings.shift_on_y*(-1 if settings.turn_direction == "LEFT" else 1)

        if settings.generation_source == "ROAD":
            response = generate_road_item(settings)
        elif settings.generation_source == "PLATFORM":
            response = generate_platform_item(settings)
        elif settings.generation_source == "SHAPE":
            response = generate_shape_item(settings)
        elif settings.generation_source == "CUSTOM":
            response = generate_custom_item(settings)
            
        if type(response) is str:
            self.report({"ERROR"}, response)

        return {'FINISHED'}
    
class VIEW3D_OT_LoadAssetsLib(Operator):
    bl_idname = "object.tmgen_add_assets_lib"
    bl_label = "Load required assets"

    def execute(self, context):
        assign_assets_file()
        load_assets_file()
        context.scene.tm_shape_generator.has_all_assets_loaded = True

        return {'FINISHED'}
    
class VIEW3D_OT_GenerateRoadSet(Operator):
    bl_idname = "object.tmgen_generate_road_set"
    bl_label = "Generate WTMT like road set"

    def execute(self, context):
        settings:ShapeGeneratorProperties = context.scene.tm_shape_generator
        response = generate_default_road_set(settings)

        if type(response) is str:
            self.report({"ERROR"}, response)

        return {'FINISHED'}