bl_info = {
    "name": "Trackmania Blocks Generator",
    "author": "Juice",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > Sidebar > TM Blocks Generator",
    "description": "Generate road/platform blocks for trackmania 2020",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"
}

import bpy
from bpy.types import Scene
from bpy.props import PointerProperty
from bpy.app.handlers import persistent

from .operators import (
    VIEW3D_OT_GenerateItem,
    VIEW3D_OT_LoadAssetsLib,
    VIEW3D_OT_GenerateRoadSet,
)
from .PanelItemGenerator import (
    VIEW3D_PT_ShapeGeneratorPanel,
)
from .PanelSetsMaker import (
    VIEW3D_PT_SetsMaker
)
from .properties import (
    ShapeGeneratorProperties
)
from .utils import (
    has_all_assets_loaded
)

classes = [
    VIEW3D_PT_ShapeGeneratorPanel,
    VIEW3D_OT_GenerateRoadSet,
    VIEW3D_OT_LoadAssetsLib,
    VIEW3D_OT_GenerateItem,
    #VIEW3D_PT_SetsMaker,
    ShapeGeneratorProperties,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    Scene.tm_shape_generator:ShapeGeneratorProperties = PointerProperty(type=ShapeGeneratorProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del Scene.tm_shape_generator


if __name__ == "__main__":
    register()


@persistent
def check_assets_loaded(dummy):
    Scene.tm_shape_generator.has_all_assets_loaded = has_all_assets_loaded()

bpy.app.handlers.load_post.append(check_assets_loaded)