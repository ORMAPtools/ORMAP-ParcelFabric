# ExportPlans
#
# This program will be used to export a selected plan an ALL related feature classes. The application
# is built around the AppendParcels program 
#
# If a plan does not have lines/points associated with it (Just polygons) once appended the associated
# points/lines will be assigned to the plan (definedbyrecord = guid of plan)
# 
#
#Important Variables: 
# Plan - Plan name - GetParameterAsText(0) 
# Filter - Filter used for the plan - GetParameterAsText(2)
# TurnFCFiltersOFF - If this is true it will turn off an plan specific filters at end of app for related feature classes
# TargetGDB - Database where plan will be exported to (comes from GetParameterAsText(4)
# TargetFD - Feature data set where Parcel fabric is (TaxlotsFD) 
# TargetFabric - Name of target fabrid (TaxlotsFD) 
#
# Assumptions:  GUID's are unique between databases - so far that appears to be true and is how append parcel works.
#               Related features will be copied to the new database within 1-3 seconds of the original plan
#
# This app converts between ESRI time (from cursor) and uses a python script to add 3 seconds and then turns that back to a query.
#    It all works fine unless ESRI changes time based fields at some point in the future. Lines 82-87 
# 
# Called from:  ArcPro ExportPlan tool/script 
#
# Dean - 11/2021
#

import arcpy, datetime, sys

# 1. Get values from parameters  ----

Plan = str(arcpy.GetParameterAsText(0))
Filter = str(arcpy.GetParameterAsText(2))
TurnFCFiltersOFF = str(arcpy.GetParameterAsText(3))
TargetGDB = str(arcpy.GetParameterAsText(4))

arcpy.AddMessage ("Plan: " + Plan)
arcpy.AddMessage ("Filter: " + Filter)
arcpy.AddMessage ("TurnOffFCFilter: " + TurnFCFiltersOFF)

if Filter.find("CreatedByRecord") < 0: 
    arcpy.AddError ("NoFilter - NoActive Record")
    sys.exit()
  
#TargetGDB= "C://TaxmapPolkV3.01//PlansInProcess//PlansInProcess.gdb"
  
TargetFD = TargetGDB + "//TaxlotsFD"
TargetFabric = TargetFD + "//TaxlotsPF"

# check if plan exists in export database If so qiut

RecordNumber = Filter.split('{')[1]
RecordNumber = RecordNumber.split('}')[0]
RecordWhereClause = "CreatedByRecord = " + "'" + RecordNumber + "'"
CalcRecord = "'{" + RecordNumber + "}'"

RecordsFc = TargetFD  + "//TaxlotsPF_Records"
PFRecordWhereClause = "GlobalID = '{"  + RecordNumber + "}'"

arcpy.MakeFeatureLayer_management(RecordsFc, "RecordsChecklyr",PFRecordWhereClause)

RecordCount = int(arcpy.GetCount_management("RecordsChecklyr").getOutput(0))
arcpy.AddMessage ("Matching Record Count In Target DB: " + str(RecordCount))

if RecordCount >= 1: 
    arcpy.AddError("This plan/record exists in the export database")
    sys.exit()

thisProject = arcpy.mp.ArcGISProject("CURRENT")      
Map = thisProject.activeMap 


#2. Append Parcels

TaxlotWhereClause = "CreatedByRecord = " + "'{" + RecordNumber + "}'"
TaxlotLyr =  Map.listLayers("Taxlot")[1]
arcpy.management.SelectLayerByAttribute(TaxlotLyr,"NEW_SELECTION",TaxlotWhereClause)
arcpy.parcel.AppendParcels('TaxlotsPF', TargetFabric)

# calc associated features to be part of the plan (boundary lines and points do get copied so this calcs them to be part of a plan) 


with arcpy.da.SearchCursor(RecordsFc,['GlobalID','created_date'],PFRecordWhereClause) as cursor:
    for row in cursor:
        CreateDate = row[1]
NextDate = CreateDate + datetime.timedelta(0,3) 
CreateDateWhereClause = "created_Date >= timestamp '" + str(CreateDate) + "' and created_Date < timestamp '" + str(NextDate) + "'and CreatedByRecord IS NULL" 
arcpy.AddMessage (CreateDateWhereClause)

ParcelFCs = ['Taxlot_Lines','TaxlotsPF_Points']

arcpy.AddMessage (CalcRecord)

for ParcelFC in ParcelFCs:
    arcpy.AddMessage (ParcelFC)
    OutParcelFC = TargetGDB + "//TaxlotsFD//" + ParcelFC
    arcpy.MakeFeatureLayer_management(OutParcelFC, "FixFeaturelyr",CreateDateWhereClause)
    arcpy.CalculateField_management("FixFeaturelyr", "CreatedByRecord",CalcRecord, "PYTHON", "")
    arcpy.management.Delete("FixFeaturelyr")

#3. Append Other Features

FilterLayers = ["TaxlotNumberAnno","Anno0100Scale","Anno0200Scale","Anno0400Scale","Anno2000Scale","CartographicLines","PLSSLINES","ReferenceLines","WaterLines"]      

for FilterLayer in FilterLayers:
    if FilterLayer =="TaxlotNumberAnno":
        OutClass = TargetGDB + "//TaxlotsFD//" + FilterLayer
    else: 
        OutClass = TargetGDB + "//" + FilterLayer
    mapFilterLyr = Map.listLayers(FilterLayer)[0]
    if mapFilterLyr.isFeatureLayer:
        arcpy.AddMessage (FilterLayer)
        if TurnFCFiltersOFF == "true":
            arcpy.AddMessage ("Filter None") 
            mapFilterLyr.definitionQuery = None  
        arcpy.management.SelectLayerByAttribute(mapFilterLyr,"NEW_SELECTION",RecordWhereClause)
        arcpy.management.Append(mapFilterLyr, OutClass, "NO_TEST")

