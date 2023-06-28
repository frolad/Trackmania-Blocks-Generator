from bpy.types import Panel
from .operators import (
    VIEW3D_OT_GenerateRoadSet,
    VIEW3D_OT_LoadAssetsLib,
)
from .properties import ShapeGeneratorProperties
from .PanelUtils import (
    add_label,
)

class VIEW3D_PT_SetsMaker(Panel):
    bl_label = "Road Set Maker"
    bl_category = "TM Items Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        settings:ShapeGeneratorProperties = context.scene.tm_shape_generator

        if not settings.has_all_assets_loaded:
            row = layout.row()
            row.scale_y = 1.5
            row.operator(VIEW3D_OT_LoadAssetsLib.bl_idname, text="Load assets to blend file", icon="ADD")
            return
        
        box = layout.box()
        box.column().prop(settings, "set_road_item_start_type", text="Start road type")
        box.column().prop(settings, "set_road_item_end_type", text="End road type")
        box.separator(factor=0)

        layout.separator(factor=0)
        row = layout.row()
        row.scale_y = 1.5
        row.operator(VIEW3D_OT_GenerateRoadSet.bl_idname, text="Generate WTMT-like road set", icon="ADD")