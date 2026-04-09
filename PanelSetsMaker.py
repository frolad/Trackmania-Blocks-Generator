from bpy.types import Panel
from .operators import (
    VIEW3D_OT_GenerateRoadSet,
    VIEW3D_OT_LoadAssetsLib,
)
from .properties import ShapeGeneratorProperties
from .PanelUtils import (
    add_label,
    add_simple_text,
)

class VIEW3D_PT_SetsMaker(Panel):
    bl_label = "Road Set Maker"
    bl_category = "TM Set Generator"
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

        layout.row().prop(settings, "generation_source", expand=True)

        if settings.generation_source == "ROAD":
            settings.property_unset("custom_object")
            box = layout.box()
            box.column().prop(settings, "set_road_item_start_type", text="Start road type")
            box.column().prop(settings, "set_road_item_end_type", text="End road type")
            box.separator(factor=0)
        elif settings.generation_source == "PLATFORM":
            settings.property_unset("custom_object")
            box = layout.box()
            add_simple_text(box, "NOT IMPLEMENTED YET")

        elif settings.generation_source == "SHAPE":
            settings.property_unset("custom_object")
            box = layout.box()
            add_simple_text(box, "NOT IMPLEMENTED YET")

        else:
            layout.separator(factor=0)
            add_label(layout, text="Surface and shape")
            box = layout.box()
            custom_single_shape(box, settings)
            box.separator(factor=0)

        box.column().prop(settings, "set_type", text="Set type")
        layout.separator(factor=0)
        row = layout.row()
        row.scale_y = 1.5
        row.operator(VIEW3D_OT_GenerateRoadSet.bl_idname, text="Generate WTMT-like set", icon="ADD")

def custom_single_shape(box, settings):
    box.separator(factor=0)
    add_simple_text(box, "Custom object must:")
    add_simple_text(box, "1) Fit in 32x32x32 meters")
    add_simple_text(box, "2) Have origin in the x,y center")
    add_simple_text(box, "3) Have enough subdivision")
    add_simple_text(box, "4) To understand how UV scales - play and test")

    add_label(box, text="Custom object:")
    box.row().column().prop(settings, "custom_object", text="")
    box.row().column().prop(settings, "custom_should_scale_uv", text="Scale BaseMaterial UV", toggle=True)