from bpy.types import Panel
from .generator.Constants import (
    MIDDLE_SHAPE,
)
from .operators import (
    VIEW3D_OT_GenerateItem,
    VIEW3D_OT_LoadAssetsLib,
)
from .properties import ShapeGeneratorProperties
from .PanelUtils import (
    add_label,
    add_simple_text,
)

class VIEW3D_PT_ShapeGeneratorPanel(Panel):
    bl_label = "Generate block"
    bl_category = "TM Blocks Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        settings:ShapeGeneratorProperties = context.scene.tm_shape_generator

        if not settings.has_all_assets_loaded:
            row = layout.row()
            row.scale_y = 1.5
            row.operator(VIEW3D_OT_LoadAssetsLib.bl_idname, text="Load assets to blend file", icon="ADD")
            return

        add_label(layout, text="Type of block")
        layout.row().prop(settings, "generation_source", expand=True)

        if settings.generation_source == "ROAD":
            add_label(layout, text="Road surface")
            layout.row().prop(settings, "generation_road_source", expand=True)

            layout.separator(factor=0)
            add_label(layout, text="Surface and shape")
            box = layout.box()
        
            if settings.generation_road_source == "SINGLE":
                road_single_shape(box, settings)
            else:
                road_multi_shape(box, settings)
            
            box.separator(factor=0)
            
        elif settings.generation_source == "PLATFORM":
            layout.separator(factor=0)
            add_label(layout, text="Surface and shape")
            box = layout.box()
            platform_single_shape(box, settings)
            box.separator(factor=0)
        elif settings.generation_source == "SHAPE":
            layout.separator(factor=0)
            add_label(layout, text="Shape")
            box = layout.box()
            only_shape(box, settings)
            box.separator(factor=0)
        else:
            layout.separator(factor=0)
            add_label(layout, text="Surface and shape")
            box = layout.box()
            custom_single_shape(box, settings)
            box.separator(factor=0)

        # 
        #layout.row().prop(settings, "dest_collection", text="Where to save")
        layout.separator(factor=0)
        add_label(layout, text="Size and shift:")
        box = layout.box()
        shift_settings(box, settings)
        box.separator(factor=0)

        layout.separator(factor=0)
        
        row = layout.row()
        row.scale_y = 1.5
        row.operator(VIEW3D_OT_GenerateItem.bl_idname, text="Generate block", icon="ADD")


def road_single_shape(box, settings):
    box.column().prop(settings, "road_single_type", expand=True)
    box.row().prop(settings, "road_start_shape", text="Start")
    box.row().prop(settings, "middle_shape", text="Middle")
    box.row().prop(settings, "road_end_shape", text="End")

def road_multi_shape(box, settings):
    add_label(box, text="Start type and shape:")
    row = box.row()
    row.column().prop(settings, "road_start_type", text="")
    row.column().prop(settings, "road_start_shape", text="")
    
    add_label(box, text="Middle shape:")
    box.row().prop(settings, "middle_shape", text="")
    
    add_label(box, text="End type and shape:")
    row = box.row()
    row.column().prop(settings, "road_end_type", text="")
    row.column().prop(settings, "road_end_shape", text="")

def platform_single_shape(box, settings):
    box.column().prop(settings, "platform_single_type", expand=True)
    box.row().prop(settings, "platform_start_shape", text="Start")
    box.row().prop(settings, "middle_shape", text="Middle")
    box.row().prop(settings, "platform_end_shape", text="End")

def only_shape(box, settings):
    box.row().prop(settings, "custom_start_shape", text="Start")
    box.row().prop(settings, "middle_shape", text="Middle")
    box.row().prop(settings, "custom_end_shape", text="End")
    box.row().prop(settings, "custom_shape_height", text=f"Height (8m step)")

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
    box.row().column().prop(settings, "custom_start_shape", text="Start")
    box.row().column().prop(settings, "middle_shape", text="Middle")
    box.row().column().prop(settings, "custom_end_shape", text="End")

def shift_settings(box, settings):
    box.separator(factor=0)
    if settings.middle_shape == MIDDLE_SHAPE.CHICANE.name:
        box.row().column().prop(settings, "shift_on_x", text=f"Left/Rigth Offset (32m step)")
    if settings.middle_shape == MIDDLE_SHAPE.TURN.name:
        box.row().column().prop(settings, "turn_direction", text=f"Turn direction")
    
    box.row().column().prop(settings, "shift_on_y", text=f"Item size (32m step)")
    
    box.row().column().prop(settings, "shift_on_z", text=f"Elevation (8m step)")

