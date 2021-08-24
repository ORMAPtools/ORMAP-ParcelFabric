# ImportReplaceAnno.py
#
# Sample Code - Imports annotation classes "Anno0100Scale", "Anno0200Scale", "Anno0400Scale", "Anno2000Scale","TaxlotNumberAnno","TaxcodeAnno"
# for a sample township from arcmap to arcpro
#
# THIS REPLACES THE ANNOTATION THAT IS IN THE Template GeoDatabase 
#
# Dependencies
#   OutGDB = Path for pro geodatabase 
#   InGDB =" Path for arcmap geodatabase
#   WorgGdb = Path for pro geodatabase temp feature classes 
#
# Dean - 1/7/2021 


import arcpy,os 

def ImportAnno(InClass,TempClass,OutClass):

# 1. Prep Data
    print (OutClass) 
    if arcpy.Exists(TempClass):
        arcpy.Delete_management(OutClass)


    print ("Prep Done ")

# 2. Import Inclass to Templass and Upgrade

    arcpy.Copy_management(InClass, OutClass) 
    arcpy.UpgradeDataset_management(OutClass)

    print ("Import Done")

# 3 Update attribute rule

    arcpy.EnableEditorTracking_management(OutClass,"created_user","created_date","last_edited_user","last_edited_date","ADD_FIELDS","UTC")
    arcpy.management.AddGlobalIDs(OutClass)


ScriptPath = os.getcwd()
OutGDB =  ScriptPath[:-14] + "\\OrMapPFTemplate.gdb"
WorkGDB =  ScriptPath[:-14] + "\\Default.gdb"
InGDB =  ScriptPath[:-20] + "geodb\\townedgeo.gdb"

#OutGDB = "C://Taxmap//T7-4/fabric//OrMapPFTemplate.gdb"
#InGDB ="C://Taxmap//T7-4//geodb//townedgeo.gdb"
#WorkGDB = "C://Taxmap/T7-4//fabric//Default.gdb"

AnnoCllasses = ["Anno0100Scale", "Anno0200Scale", "Anno0400Scale", "Anno2000Scale","TaxlotNumberAnno","TaxcodeAnno"]

for c in AnnoCllasses:
    TempClass = WorkGDB + "//AnnoX" 
    InClass = InGDB + "//" + c 
    OutClass = OutGDB + "//" + c
    ImportAnno(InClass,TempClass,OutClass)
    print ("Class Done: " + c) 
    
