# AddDimAnno.py
#
# Creates dimension annotation from new TaxlotLine Labels
#
# Uses TiledLabelsToAnnotation command which is strange
#
#
# Dean - Fall 2018 

import arcpy, os

AnnoStyle = arcpy.GetParameterAsText(0)
TaxlotLinesSelected = arcpy.GetParameterAsText(1)
MapIndexCount = arcpy.GetParameterAsText(2)
MapNumber = arcpy.GetParameterAsText(3)
MapScale = arcpy.GetParameterAsText(4)
LabelClass = arcpy.GetParameterAsText(5)
AnnoLayer = arcpy.GetParameterAsText(6)
TaxlotLinesLayer = arcpy.GetParameterAsText(7)
MapIndexLayer = arcpy.GetParameterAsText(8)

# ---Setup Get Paths ------------------------

thisProject = arcpy.mp.ArcGISProject("CURRENT")
Map = thisProject.activeMap
MapIndexLyr = Map.listLayers(MapIndexLayer)[0]
TaxlotLineLyr = Map.listLayers(TaxlotLinesLayer)[0]
AnnoLyr = Map.listLayers(AnnoLayer)[0]

ScriptPath = os.getcwd()

OutGDB =  ScriptPath[:-10] + "\\OrMapPFTemplate.gdb"
WorkGDB =  ScriptPath[:-10] + "\\Default.gdb"

arcpy.AddMessage (ScriptPath)
arcpy.AddMessage (WorkGDB)

# -------- Set Temporary anno layers 

AnnoF = "Anno" + str(MapScale)
GroupAnno = "GroupAnno"
AnnoFPth = WorkGDB + "\\Taxlot_lines" +  AnnoF 
AnnoFLyr =  "Taxlot_lines" + AnnoF 
annoID = 9 

arcpy.AddMessage ("AnnoF: " + AnnoF)
    
# delete Temp layers 

arcpy.Delete_management (GroupAnno)
arcpy.Delete_management (AnnoFLyr)
arcpy.Delete_management(AnnoFPth)

# Make Anno and append to label class

arcpy.cartography.ConvertLabelsToAnnotation('Map', 1200, WorkGDB, AnnoF, 'default', 'ONLY_PLACED', 'NO_REQUIRE_ID', 'STANDARD', '', '', GroupAnno, 'SINGLE_LAYER', TaxlotLineLyr, '', '')

arcpy.CalculateField_management(AnnoFPth, "SymbolID",0, "PYTHON3")

arcpy.Append_management(AnnoFLyr, AnnoLyr, "NO_TEST")

arcpy.AddMessage ("TempMade: " + AnnoFLyr)

# select and update newly added anno 

arcpy.SelectLayerByAttribute_management(AnnoLyr, "NEW_SELECTION", "SymbolID = 0")

arcpy.CalculateField_management(AnnoLyr, "SymbolID",annoID, "PYTHON3")
arcpy.CalculateField_management(AnnoLyr, "AnnotationClassID",annoID, "PYTHON3")
arcpy.CalculateField_management(AnnoLyr, "MapNumber","'" + MapNumber + "'", "PYTHON3")


# End stuff - unselect stuff 

#arcpy.SelectLayerByAttribute_management(AnnoLyr, "CLEAR_SELECTION")
#arcpy.SelectLayerByAttribute_management(TaxlotLineLyr, "CLEAR_SELECTION")
#arcpy.SelectLayerByAttribute_management(MapIndexLyr, "CLEAR_SELECTION")

arcpy.Delete_management (GroupAnno)
arcpy.Delete_management (AnnoFLyr)
arcpy.Delete_management(AnnoFPth)










        

