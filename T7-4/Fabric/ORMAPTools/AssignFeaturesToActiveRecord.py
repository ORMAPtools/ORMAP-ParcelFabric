# AssignFeatureToActiveRecord
#
# For the active record this walks through selected Non-PF features in the CalcLayers List and assigns
# them to the active record.  This assumes you have an active record selected and that you have features
# selected to assign to them.
# 
#
# Called from script: AssignFeaturesToActiveRecord - The validation process will tell you if you have an active record 
#
# 1 Get variables and build calc statements
# 2 Assign calclayers 
# 3 walk thru calc layers and assign (or unassign) - if unassign is true it will calc whatever is there to null 
#
# Important Variables
# Plan - Plan name
# Filter - Filter used for the plan
# UnAssign - If true it will make createdby record = none if false it will calc it correctly
# Calc Layers - Layers that will be impacted 
#
# Called from: AssignFeatureToActiveRecord Arcpro tool/script 
# 
# To customize - change layer names CalcLayers
#
# Dean - 12/2021
#

import arcpy, datetime, sys

# 1  Get values from parameters  ----

Plan = str(arcpy.GetParameterAsText(0))
Filter = str(arcpy.GetParameterAsText(2))
Unassign = str(arcpy.GetParameterAsText(3))

arcpy.AddMessage ("Plan: " + Plan)
arcpy.AddMessage ("Filter: " + Filter)
arcpy.AddMessage ("Unassign: " + Unassign)              


if Filter.find("CreatedByRecord") < 0: 
    arcpy.AddError ("NoFilter - NoActive Record")
    sys.exit()

RecordNumber = Filter.split('{')[1]
RecordNumber = RecordNumber.split('}')[0]
CalcRecord = "'" + RecordNumber + "'"
UnCalcRecord = "None" 
thisProject = arcpy.mp.ArcGISProject("CURRENT")      
Map = thisProject.activeMap

#2 Assign calclayers

CalcLayers = ["TaxlotNumberAnno","Anno0100Scale","Anno0200Scale","Anno0400Scale","Anno2000Scale","CartographicLines","PLSSLINES","ReferenceLines","WaterLines"]      

#3 walk thru calc layers and assign (or unassign)

for CalcLayer in CalcLayers:
    mapCalcLyr = Map.listLayers(CalcLayer)[0]
    if mapCalcLyr.isFeatureLayer:
        arcpy.AddMessage (CalcLayer)
        desc = arcpy.Describe(mapCalcLyr)
        if desc.FIDSet != '':
            arcpy.AddMessage("--Selected features: {}".format(len(desc.FIDSet.split(";"))))
            if Unassign == 'true':
                arcpy.CalculateField_management(mapCalcLyr, "CreatedByRecord",'None', "PYTHON", "")
            else:
                arcpy.CalculateField_management(mapCalcLyr, "CreatedByRecord",CalcRecord, "PYTHON", "")
    
