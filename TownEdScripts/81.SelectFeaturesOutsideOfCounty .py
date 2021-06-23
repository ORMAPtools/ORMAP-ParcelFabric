# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 81.SelectFeaturesOutsideOfCounty 
#
# Selects all features on a map that are outside the County boundary
# Allow user to assign features mapscale and mapnumber to nearest map.  This does not
# include annolayers for 62 (Seemaps as ut should be assigned to a map)
#
# If CalcNear = Yes it assigns mapnumber and mapscale to nearest map
# also calcus date to be today and autowho to "CntyFix"
#
# Using Mapindex27 county-wide for the county border (check path) 
# 
# Parameter1 = list of features to review
# Parameter2 = Y/N - assign to nearest features
#
# Note: because this uses Near it adds then removes two fields from the feature selected
# Note2: Does a little strange stuff for annoclasses as they do not support near 
# 
# Author: Dean                       January 2021 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy,os

# Get varlables and paths

FeaturesToCheck = []
FList = sys.argv[1]
arcpy.AddMessage ("FList: " + FList)
CalcNear = sys.argv[2]

FeaturesToCheck = FList.split(';')
 
mxd = arcpy.mapping.MapDocument("CURRENT")
mxdpath = mxd.filePath
localpath = os.path.dirname(mxdpath)
MapIndex27 = "C:\\TaxWebGeoDBFrmORCATS\\TaxmapWeb.gdb\\Mapindex27" 
CountyBoundary = localpath + "\\townedgeo.gdb\\CountyBoundary"

# Get county boundary from mapindex and disoolve 

arcpy.Delete_management(CountyBoundary)
arcpy.Dissolve_management(MapIndex27,CountyBoundary,"PageNumber")

# process for each feature on list 

for feature in FeaturesToCheck:
    feature = feature.strip("'")
    arcpy.AddMessage ("Checking: " + feature)
    MapF = arcpy.mapping.ListLayers(mxd, feature)[0]
    arcpy.SelectLayerByAttribute_management(MapF, "CLEAR_SELECTION")
    arcpy.SelectLayerByLocation_management (MapF, "WITHIN_CLEMENTINI",CountyBoundary)
    arcpy.SelectLayerByAttribute_management(MapF, "SWITCH_SELECTION")
    if feature.startswith("Anno"): 
        arcpy.SelectLayerByAttribute_management(MapF, "SUBSET_SELECTION",'"AnnotationClassID" <> 21')        
    result = arcpy.GetCount_management(feature)
    count = int(result.getOutput(0))
    arcpy.AddMessage ("Layer: " + feature + " Features Found: " + str(count))
    
# if feature is near and parameter is YES find nearest map and assign mapnumber, mapscale and todays date

    if CalcNear == "YES" and count > 0:
        arcpy.AddMessage (" ---- Calculate MapNum and Mapscale to nearest Map") 
        MapIndex = arcpy.mapping.ListLayers(mxd, "MapIndex")[0]
        if not feature.startswith("Anno"): 
            arcpy.Near_analysis(MapF, MapIndex)
            arcpy.AddJoin_management( MapF, "Near_FID", MapIndex, "OBJECTID")
            arcpy.CalculateField_management(MapF, "MapScale","!Mapindex.MapScale!","PYTHON")
        else:
            MapFPT = localpath + "\\townedgeo.gdb\\" + feature + "PT"
            arcpy.Delete_management(MapFPT)
            arcpy.Delete_management("MapFPTLyr")
            arcpy.FeatureToPoint_management(MapF,MapFPT) 
            arcpy.Near_analysis(MapFPT, MapIndex)
            arcpy.MakeFeatureLayer_management(MapFPT,"MapFPTLyr")
            arcpy.AddJoin_management( MapF, "OBJECTID", "MapFPTLyr", "ORIG_FID")
            JoinField = feature + "PT.near_FID"
            arcpy.AddJoin_management( MapF, JoinField, MapIndex, "OBJECTID")                             
        Date = time.strftime("%d/%m/%Y")
        arcpy.CalculateField_management(MapF, "MapNumber", "!Mapindex.MapNumber!","PYTHON")
        arcpy.CalculateField_management(MapF, "AutoDate","time.strftime('%m/%d/%Y')","PYTHON")
        arcpy.CalculateField_management(MapF, "AutoWho","'CntyFix'","PYTHON") 
        arcpy.RemoveJoin_management (MapF)
        if not feature.startswith("Anno"):
            arcpy.DeleteField_management (MapF,"NEAR_FID")
            arcpy.DeleteField_management (MapF,"NEAR_DIST")
            arcpy.CalculateField_management(MapF, "MapScale","!MapScale!","PYTHON")
        else:
            arcpy.Delete_management(MapFPT)
        arcpy.CalculateField_management(MapF, "MapNumber", "!MapNumber!","PYTHON")

