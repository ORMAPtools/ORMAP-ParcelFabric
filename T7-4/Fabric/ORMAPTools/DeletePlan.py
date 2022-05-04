# Delete Plan
#
# Deletes the current plan and ALL related feature classes from an
# active ArcPro Sesession (THis project - Current) 
#
# Important Variables
# Plan - Plan name
# Filter - Filter used for the plan
# DeleteRecordsYesNo - Question from form to delte it or not - if false exit 
# DeleteLayers - List of related layers that will be deleted 
#
# Dean - 11/2021
#

import arcpy, sys 

# 1. Get values from parameters  ----

Plan = str(arcpy.GetParameterAsText(0))
Filter = str(arcpy.GetParameterAsText(2))
DeleteRecordYesNo = str(arcpy.GetParameterAsText(3))

if Filter.find("CreatedByRecord") < 0: 
    arcpy.AddError ("NoFilter - NoActive Record")
    sys.exit()

if DeleteRecordYesNo == 'false': 
    arcpy.AddError ("Need to say yes to delete it")
    sys.exit()
    
arcpy.AddMessage (Filter)

thisProject = arcpy.mp.ArcGISProject("CURRENT")      
Map = thisProject.activeMap 

RecordNumber = Filter.split('{')[1]
RecordNumber = RecordNumber.split('}')[0]
RecordWhereClause = "CreatedByRecord = " + "'" + RecordNumber + "'"
RecordPfQuery = "CreatedByRecord = '{" + RecordNumber + "}'"
RecordGIdQuery =  "GlobalID = '{" + RecordNumber + "}'"


#2. Delete Record
        
mapDeleteLyr = Map.listLayers("Records")[0]        
arcpy.SelectLayerByAttribute_management(mapDeleteLyr, 'NEW_SELECTION', RecordGIdQuery)
arcpy.AddMessage(mapDeleteLyr) 
arcpy.DeleteFeatures_management(mapDeleteLyr)

# 3. DeleteFabric Layers

DeleteLayers = ["Taxlot","Taxlot_Lines","Points","Connection Lines"]      

for DeleteLayer in DeleteLayers:
    if DeleteLayer == "Taxlot":
        mapDeleteLyr = Map.listLayers(DeleteLayer)[1]        
    else: 
        mapDeleteLyr = Map.listLayers(DeleteLayer)[0]
    if mapDeleteLyr.isFeatureLayer:
        arcpy.AddMessage(DeleteLayer) 
        arcpy.SelectLayerByAttribute_management(mapDeleteLyr, 'NEW_SELECTION', RecordPfQuery)
        arcpy.DeleteFeatures_management(mapDeleteLyr)
        
# 4. Delete Related Layers 

DeleteLayers = ["TaxlotNumberAnno","Anno0100Scale","Anno0200Scale","Anno0400Scale","Anno2000Scale","CartographicLines","PLSSLINES","ReferenceLines","WaterLines"]      
               
for DeleteLayer in DeleteLayers:
    mapDeleteLyr = Map.listLayers(DeleteLayer)[0]
    if mapDeleteLyr.isFeatureLayer:
        arcpy.AddMessage(DeleteLayer) 
        arcpy.SelectLayerByAttribute_management(mapDeleteLyr, 'NEW_SELECTION', RecordWhereClause)
        arcpy.DeleteFeatures_management(mapDeleteLyr)
    

