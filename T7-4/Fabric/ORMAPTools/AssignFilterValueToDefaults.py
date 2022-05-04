# AssignFilterToDefaults
#
# Descodes the filter from ActiveRecord to get the correct GlobalId.
# Assign the globalID to CreatedByRecord field in each feature classe that is
# identified in FilterLayers.
#
# Called from AssignFilterToDefaults tool in default toolbox.
#
# Filter - this is the filter from the tool
# DoIt - this tels the application to either assign or unassign filter values as
# default.  DoIt = "true" and it assigns else it unassigns
#
# Uses arcpy.da.ListSubtypes - to get subtypes (or not) from each layer
# if len stcodes is one it has no subtypes. Or use stcodes to assign to each subtype
# 
# Uses AssignDefaultToField_management to assign or unassign default values
#
# FilterLayers - List of layers that will participate
# thisProject - current project that script is called from
# Map - active map
#
# ISSUE - For some reason ReferenceLines thinks it has subtypes. It Does Not!
#         no sure what is wrong so this layer is managed as an exception.  
#
# Dean - 11/2021
#

import arcpy 

# 1. Get values from parameters  ----

RecordName = str(arcpy.GetParameterAsText(0))
Filter = str(arcpy.GetParameterAsText(1))
DoIt = arcpy.GetParameterAsText(2)

arcpy.AddMessage (RecordName)
arcpy.AddMessage (Filter)
arcpy.AddMessage (DoIt)

thisProject = arcpy.mp.ArcGISProject("CURRENT")      
Map = thisProject.activeMap 

FilterLayers = ["TaxlotNumberAnno","Anno0100Scale","Anno0200Scale","Anno0400Scale","Anno2000Scale","CartographicLines","ReferenceLines"]      
#FilterLayers = ["ReferenceLines","CartographicLines","WaterLines"]
#FilterLayers = ["cartographiclines","ReferenceLines","TaxlotNumberAnno"] 

                
if DoIt == 'true':
    RecordNumber = Filter.split('{')[1]
    RecordNumber = RecordNumber.split('}')[0]
    arcpy.AddMessage (RecordNumber)
    
    for FilterLayer in FilterLayers: 
        mapFilterLyr = Map.listLayers(FilterLayer)[0]
        if mapFilterLyr.isFeatureLayer:
            arcpy.AddMessage (FilterLayer)
            # get subtypes if they exist 
            SubsToDefault = [] 
            subtypes = arcpy.da.ListSubtypes(mapFilterLyr)
            for stcode, stdict in list(subtypes.items()):
                SubsToDefault.append(str(stcode))
            arcpy.AddMessage(len(SubsToDefault))
            # Assign default codes  
            if len(SubsToDefault) == 1 or FilterLayer == "ReferenceLines":
                arcpy.AssignDefaultToField_management(mapFilterLyr,"CreatedByRecord", RecordNumber)
            else:
                arcpy.AssignDefaultToField_management(mapFilterLyr,"CreatedByRecord", RecordNumber,SubsToDefault)
else:
    arcpy.AddMessage ("clear")   
    for FilterLayer in FilterLayers:
        mapFilterLyr = Map.listLayers(FilterLayer)[0]
        if mapFilterLyr.isFeatureLayer:
            arcpy.AddMessage (FilterLayer)
            # get subtypes if they exist 
            SubsToDefault = [] 
            subtypes = arcpy.da.ListSubtypes(mapFilterLyr)
            
            for stcode, stdict in list(subtypes.items()):
                SubsToDefault.append(str(stcode))
            arcpy.AddMessage(len(SubsToDefault))
            # clear default codes 
            if len(SubsToDefault) == 1 or FilterLayer == "ReferenceLines":
                arcpy.AssignDefaultToField_management(mapFilterLyr,"CreatedByRecord","","",'CLEAR_VALUE') 
            else:
                arcpy.AssignDefaultToField_management(mapFilterLyr,"CreatedByRecord","",SubsToDefault,'CLEAR_VALUE')

