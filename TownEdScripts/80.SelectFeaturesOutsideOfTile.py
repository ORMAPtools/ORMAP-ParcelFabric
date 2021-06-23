# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 22CheckOutsideMapBoundary 
#
# Selects all features on a map that are outside the map/tile boundary but
# still inside the county This does not include annolayers for 58 and 62 (Seemaps
# and Adjacent Counties). These features should be deleted.
#
# For each feature class in list it selects them and leaves them selected. 
#
# uses countywide Mapindex27 as input
#
# Note: In some mxd's the Cartographic Lines layer has a blank at the end
# this causes problems so need to remove it in the table of contents. 
#
# Author: Dean                                   jan 2021 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy,os

# get parameters and set paths

FeaturesToCheck = []
FList = sys.argv[1]
arcpy.AddMessage ("FList: " + FList)

FeaturesToCheck = FList.split(';')
mxd = arcpy.mapping.MapDocument("CURRENT")
mxdpath = mxd.filePath
localpath = os.path.dirname(mxdpath)
MapIndex = localpath + "\\townedgeo.gdb\\TaxlotsFD\\MapIndex"
TileBoundary = localpath + "\\townedgeo.gdb\\TileBoundary"
MapIndex27 = "C:\\TaxWebGeoDBFrmORCATS\\TaxmapWeb.gdb\\Mapindex27" 
CountyBoundary = localpath + "\\townedgeo.gdb\\CountyBoundary"

# Dissolve layers for Mapindex Tile and County Boundary 

arcpy.Delete_management("TileBoundary_lyr")
arcpy.Delete_management(TileBoundary)
arcpy.Delete_management(CountyBoundary)
arcpy.Dissolve_management(MapIndex,TileBoundary,"PageNumber")
arcpy.Dissolve_management(MapIndex27,CountyBoundary,"PageNumber")

# For each feature do the selection and print out how many found 

for feature in FeaturesToCheck:
    feature = feature.strip("'")
    arcpy.AddMessage ("Checking: " + feature)
    MapF = arcpy.mapping.ListLayers(mxd, feature)[0]
    arcpy.SelectLayerByAttribute_management(MapF, "CLEAR_SELECTION")
    arcpy.SelectLayerByLocation_management (MapF, "WITHIN_CLEMENTINI", TileBoundary)
    arcpy.SelectLayerByAttribute_management(MapF, "SWITCH_SELECTION")
    arcpy.SelectLayerByLocation_management (MapF, "COMPLETELY_WITHIN", CountyBoundary,"","SUBSET_SELECTION")    
    if feature.startswith("Anno"): 
        arcpy.SelectLayerByAttribute_management(MapF, "SUBSET_SELECTION",'"AnnotationClassID" <> 21 and "AnnotationClassID" <> 20')    
    result = arcpy.GetCount_management(feature)
    count = int(result.getOutput(0))
    arcpy.AddMessage ("Layer: " + feature + " Features Found: " + str(count))



