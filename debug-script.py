import imp
import os
import sys
import bpy

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)


import Runner
import generator.Prefabs
import generator.Constants as Constants
import generator.BlenderUtils
import generator.ShapeGenerator
import generator.TrackmaniaUtils
import generator.RoadItemGenerator as RoadItemGenerator
import generator.ShapeGeneratorUtils

import imp
imp.reload(Runner)
imp.reload(generator.Prefabs)
imp.reload(generator.Constants)
imp.reload(generator.BlenderUtils)
imp.reload(generator.ShapeGenerator)
imp.reload(generator.TrackmaniaUtils)
imp.reload(generator.RoadItemGenerator)
imp.reload(generator.ShapeGeneratorUtils)

def execute():
    RoadItemGenerator.create_road_item(
        start=(Constants.ROAD_TYPE.BLAD_ROAD_NARROW, Constants.SIDE_SHAPE.HALFBANKED_RIGHT),
        end=(Constants.ROAD_TYPE.ROAD_DIRT, Constants.SIDE_SHAPE.FLAT),
        middle_shape=Constants.MIDDLE_SHAPE.TURN,
        shift_xyz=(3,3,-3),
        dest_collection=bpy.data.collections["TEST"]
    )

execute()