# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 82.CheckMapNumber
#
# Compares the map numbers asscoiated with the feature with the mapnumber
# that it is spatially in.  If not match it flags it.  Also if uesr desides
# to calc the mapnumber it will. Ignores seemaps. 
#
# parameters[1] - list of features use selects
# parameters[2] - to calc (YES) or not (NO)
#
# again had issues cartographic lines - best thing to do change the
# layer name to "cartographiclines" not spaces anywhere. 
#
# if Cacmapnumber = YES then calcs mapnum, mapscale, autodate, autowho
#
# Author: Dean                                   Jan 2021 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy,os

# Get Parameters

FeaturesToCheck = []
FList = sys.argv[1]
arcpy.AddMessage ("FList: " + FList)
FeaturesToCheck = FList.split(';')
calcmapnumber = sys.argv[2]

mxd = arcpy.mapping.MapDocument("CURRENT")
mxdpath = mxd.filePath
localpath = os.path.dirname(mxdpath)
MapIndex = localpath + "\\townedgeo.gdb\\TaxlotsFD\\MapIndex"

# Work thru feature list

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
    #arcpy.AddMessage ("Q: " + QueryMapNum)
    arcpy.SelectLayerByAttribute_management(MapFlyr, "NEW_SELECTION", QueryMapNum)

# Excetion - remove seemaps

    if feature.startswith("Anno"):
        QueryClassID  = feature + ".AnnotationClassID <> 21"
        arcpy.AddMessage ("QS: " + QueryClassID)
        arcpy.SelectLayerByAttribute_management(MapFlyr, "SUBSET_SELECTION",QueryClassID)
        
    result = arcpy.GetCount_management(MapFlyr)
    count = int(result.getOutput(0))
    arcpy.AddMessage ("Layer: " + feature + " Features Found: " + str(count))

# calc values if param 1 = YES

    if calcmapnumber == "YES" and count > 0:
        calcmapscale =  "!" + feature + "Join.mapscale_1!"
        calcmapnumber = "!" + feature + "Join.mapnumber_1!" 
        arcpy.AddMessage(calcmapnumber)
        arcpy.AddMessage(calcmapscale)

# exception for Anno as it has no mapscale

        if not feature.startswith("Anno"):
            arcpy.CalculateField_management(MapFlyr, "MapScale", calcmapscale, "PYTHON")
            
        arcpy.CalculateField_management(MapFlyr, "AutoDate", "time.strftime('%m/%d/%Y')", "PYTHON")
        arcpy.CalculateField_management(MapFlyr, "AutoWho", "'FixMapNum'", "PYTHON")
        arcpy.CalculateField_management(MapFlyr, "MapNumber", calcmapnumber, "PYTHON")

# resect to originak

    arcpy.RemoveJoin_management (MapFlyr)       
    arcpy.Delete_management(MapFJoin)
    arcpy.Delete_management("MapFJoinLyr") 
