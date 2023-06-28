import os
import bpy
from pathlib import Path

def call_async(func, timeout) -> None:
    bpy.app.timers.register(func, first_interval=timeout)

def assign_assets_file():
    shouldCreate = True
    addon_path = os.path.dirname(__file__)
    for lib in bpy.context.preferences.filepaths.asset_libraries:
        if lib.path == addon_path:
            shouldCreate = False

    if shouldCreate:
        bpy.ops.preferences.asset_library_add(directory=addon_path)
        for lib in bpy.context.preferences.filepaths.asset_libraries:
            if lib.path == addon_path:
                lib.name = "WTMT Addon assets"

    # bpy.context.screen is None when accessing from another thread
    def run_from_blender() -> None:
        for screen in bpy.data.screens:
            for area in screen.areas:
                if area.type == "FILE_BROWSER":
                    for space in area.spaces:
                        if space.type == "FILE_BROWSER":
                            try:
                                space.params.asset_library_ref = "WTMT Addon assets"
                            except AttributeError:
                                pass
    call_async(run_from_blender, 1)

def has_all_assets_loaded():
    has_all = True
    with bpy.data.libraries.load(f"{os.path.dirname(__file__)}/WTMTassets.blend", assets_only=True) as (data_from, data_to):
        data_from.objects
        for obj_name in data_from.objects:
            if obj_name not in data_to.objects or obj_name not in bpy.data.objects:
                has_all = False
                break

    print(has_all)
    return has_all

def load_assets_file():
    with bpy.data.libraries.load(f"{os.path.dirname(__file__)}/WTMTassets.blend", assets_only=True) as (data_from, data_to):
        for obj_name in data_from.objects:
            if obj_name in data_from.objects and obj_name not in data_to.objects and obj_name not in bpy.data.objects:
                data_to.objects += [obj_name]