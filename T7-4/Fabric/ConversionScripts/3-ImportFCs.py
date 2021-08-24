# ImportFCs.py
#
# Sample Code - Imports feature classes (poly and non-cogo lines)
#   "WaterLines","Water","CartographicLines","TaxlotsFD/Taxcode","TaxlotsFD/MapIndex","TaxlotsFD/TaxcodeLines"
#
# This is just a simple append
# 
# Dependencies
#   OutGDB = Path for pro geodatabase 
#   InGDB =" Path for arcmap geodatabase
#
# Important:  The last class is CORNER as I then use the OUTCLASS to calc all the isfixed to be true as these are corner points
#  This will DIE if the CORNER featcure class is not the last one in the list. 
# 
# Dean - 8/7/2020

import arcpy,os 


def ImportFC(InClass,OutClass,fc):

    # Prep Data
    arcpy.DeleteFeatures_management(OutClass)
    
    # Append
    arcpy.Append_management(InClass, OutClass, "NO_TEST")

    if fc == "CartographicLines":
        arcpy.SimplifyByStraightLinesAndCircularArcs_edit(OutClass, ".1 feet") 

######### Main Program ####################
        
# Set Paths 

ScriptPath = os.getcwd()
OutGDB =  ScriptPath[:-17] + "\\OrMapPFTemplate.gdb"
InGDB =  ScriptPath[:-24] + "geodb\\townedgeo.gdb"

# Identify feature classes to conver 

FCClasses = ["WaterLines","Water","CartographicLines","TaxlotsFD/Taxcode","TaxlotsFD/MapIndex","TaxlotsFD/TaxCodeLines","Corner"]

# for each feature class distinguish those that are the TaxlotsFD Feautre class

for c in FCClasses:
    InClass = InGDB + "/" + c 
    OutClass = OutGDB + "/" + c
    if c == "Corner":
        OutClass = OutGDB + "/" + "TaxlotsFD/TaxlotsPF_Points"
    else:
        OutClass = OutGDB + "/" + c
    ImportFC(InClass,OutClass,c)
    print ("Class Done: " + c) 

# for last feature class WHICH IS CORNERS set them to be IsFixed so they do not move in the fabric

arcpy.CalculateField_management(OutClass, "IsFixed", True, "PYTHON3")
