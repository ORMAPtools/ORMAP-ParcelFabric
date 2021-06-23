# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 82.CheckMapScale
#
# Selects all features that do not have the correct scale given the map number they are in 
#
# This does not include annolayers for 58 and 62 (Seemaps and Adjacent Counties)
#
# Note: Cartographic Lines in some maps have a blank on the end. It messes stuff
# up so remove it. 
#
# Author: Dean                          Jan 2021 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy,os

FeaturesToCheck = []
FList = sys.argv[1]
arcpy.AddMessage ("FList: " + FList)
FeaturesToCheck = FList.split(';')

mxd = arcpy.mapping.MapDocument("CURRENT")
mxdpath = mxd.filePath
localpath = os.path.dirname(mxdpath)

Q100 = "( MAPNUMBER LIKE '%AA' OR MAPNUMBER LIKE '%AB' OR MAPNUMBER LIKE '%AC' OR MAPNUMBER LIKE '%AD' OR \
MAPNUMBER LIKE '%BA' OR MAPNUMBER LIKE '%BB' OR MAPNUMBER LIKE '%BC' OR MAPNUMBER LIKE '%BD' OR \
MAPNUMBER LIKE '%CA' OR MAPNUMBER LIKE '%CB' OR MAPNUMBER LIKE '%CC' OR MAPNUMBER LIKE '%CD' OR \
MAPNUMBER LIKE '%DA' OR MAPNUMBER LIKE '%DB' OR MAPNUMBER LIKE '%DC' OR MAPNUMBER LIKE '%DD' ) "

Q200 = "( MAPNUMBER NOT LIKE '%AA' AND MAPNUMBER NOT LIKE '%AB' AND MAPNUMBER NOT LIKE '%AC' AND MAPNUMBER NOT LIKE '%AD' AND \
MAPNUMBER NOT LIKE '%BA' AND MAPNUMBER NOT LIKE '%BB' AND MAPNUMBER NOT LIKE '%BC' AND MAPNUMBER NOT LIKE '%BD' AND \
MAPNUMBER NOT LIKE '%CA' AND MAPNUMBER NOT LIKE '%CB' AND MAPNUMBER NOT LIKE '%CC' AND MAPNUMBER NOT LIKE '%CD' AND \
MAPNUMBER NOT LIKE '%DA' AND MAPNUMBER NOT LIKE '%DB' AND MAPNUMBER NOT LIKE '%DC' AND MAPNUMBER NOT LIKE '%DD' ) AND \
(MAPNUMBER LIKE '%A' OR MAPNUMBER LIKE '%B' OR MAPNUMBER LIKE '%C' OR MAPNUMBER LIKE '%D')"

Q400 = "POSITION('A' in MapNumber) = 0 and POSITION('B' in MapNumber) = 0 and POSITION('C' in MapNumber) = 0 \
and POSITION('D' in MapNumber) = 0 AND CHAR_LENGTH(MAPNUMBER) > 4"

Q2000 = "CHAR_LENGTH(MAPNUMBER) < 5"

Queries = [Q100,Q200,Q400,Q2000]
Scales = ["1200","2400","4800","24000"]
    
for feature in FeaturesToCheck:
    feature = feature.strip("'")
    arcpy.AddMessage ("Checking: " + feature)
    MapF = arcpy.mapping.ListLayers(mxd, feature)[0]
    if feature.startswith("Anno"):
        if feature.endswith("0100Scale"):
            arcpy.SelectLayerByAttribute_management(MapF, "NEW_SELECTION", Q100)
        if feature.endswith("0200Scale"):
             arcpy.SelectLayerByAttribute_management(MapF, "NEW_SELECTION", Q200)           
        if feature.endswith("0400Scale"):
             arcpy.SelectLayerByAttribute_management(MapF, "NEW_SELECTION", Q400)           
        if feature.endswith("2000Sclae"):
             arcpy.SelectLayerByAttribute_management(MapF, "NEW_SELECTION", Q2000)           
        arcpy.SelectLayerByAttribute_management(MapF, "SWITCH_SELECTION")            
        arcpy.SelectLayerByAttribute_management(MapF, "SUBSET_SELECTION",'"AnnotationClassID" <> 21 and "AnnotationClassID" <> 16')       
    else:
        i = 0 
        for Q in Queries:
            Query = Q + ' and mapscale <> ' + Scales[i]
            #arcpy.AddMessage ("Checking: " + Query)
            if i == 0:
                arcpy.SelectLayerByAttribute_management(MapF, "NEW_SELECTION", Query)
            else:
                arcpy.SelectLayerByAttribute_management(MapF, "ADD_TO_SELECTION", Query)
            i = i + 1     
        
    result = arcpy.GetCount_management(MapF)
    count = int(result.getOutput(0))
    arcpy.AddMessage ("Layer: " + feature + " Features Found: " + str(count))

