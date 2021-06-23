# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 82.CheckMapNumber
#
# Selects all features on a map that are outside the map/tile boundary but
# still inside the county
#
# This does not include annolayers for 58 and 62 (Seemaps and Adjacent Counties)
#
# Author: Dean                                   Jan 2021 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy,os

FeaturesToCheck = []
FList = sys.argv[1]
arcpy.AddMessage ("FList: " + FList)
FeaturesToCheck = FList.split(';')
calcmapnumber = sys.argv[2]

mxd = arcpy.mapping.MapDocument("CURRENT")
mxdpath = mxd.filePath
localpath = os.path.dirname(mxdpath)
MapIndex = localpath + "\\townedgeo.gdb\\TaxlotsFD\\MapIndex"
    
for feature in FeaturesToCheck:
    feature = feature.strip("'")
    arcpy.AddMessage ("Checking: " + feature)
    MapFlyr = arcpy.mapping.ListLayers(mxd, feature)[0]
    MapF = MapFlyr.dataSource
    #arcpy.AddMessage ("S: " + MapF) 
    MapFJoin = MapF + "Join"
    #arcpy.AddMessage ("J: " + MapFJoin) 
    arcpy.Delete_management(MapFJoin)
    arcpy.Delete_management("MapFJoinLyr")
    
    arcpy.SpatialJoin_analysis(MapF, MapIndex, MapFJoin,"#","#","#","WITHIN_CLEMENTINI")    
    arcpy.MakeFeatureLayer_management(MapFJoin,"MapFJoinLyr",'"MapNumber" <> "MapNumber_1"')
    arcpy.AddJoin_management( MapFlyr, "OBJECTID", MapFJoin, "TARGET_FID")
    QueryMapNum = feature + ".mapnumber <> " + feature + "Join.mapnumber_1"
    arcpy.AddMessage ("Q: " + QueryMapNum)
    arcpy.SelectLayerByAttribute_management(MapFlyr, "NEW_SELECTION", QueryMapNum)

    if feature.startswith("Anno"):
        QueryClassID  = feature + ".AnnotationClassID <> 21"
        arcpy.AddMessage ("QS: " + QueryClassID)
        arcpy.SelectLayerByAttribute_management(MapFlyr, "SUBSET_SELECTION",QueryClassID)
        
    result = arcpy.GetCount_management(MapFlyr)
    count = int(result.getOutput(0))
    arcpy.AddMessage ("Layer: " + feature + " Features Found: " + str(count))
        
    #arcpy.RemoveJoin_management (MapFlyr)       
    #arcpy.Delete_management(MapFJoin)
    #arcpy.Delete_management("MapFJoinLyr") 
