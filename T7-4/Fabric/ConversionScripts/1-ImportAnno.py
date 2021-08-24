# ImportAnno.py
#
# Sample Code - Imports annotation classes "Anno0100Scale", "Anno0200Scale", "Anno0400Scale", "Anno2000Scale","TaxlotNumberAnno","TaxcodeAnno"
# for a sample township from arcmap to arcpro
#
# Dependencies
#   OutGDB = Path for pro geodatabase 
#   InGDB =" Path for arcmap geodatabase
#   WorgGdb = Path for pro geodatabase temp feature classes 
#
# Dean - 8/7/2020 


import arcpy,os 

def ImportAnno(InClass,TempClass,OutClass):

# 1. Prep Data
    print (TempClass)
    print (OutClass) 
    if arcpy.Exists(TempClass):
        arcpy.Delete_management(TempClass)
    arcpy.DeleteFeatures_management(OutClass)

    print ("Prep Done ")

# 2. Import Inclass to Templass and Upgrade

    arcpy.Copy_management(InClass, TempClass) 
    arcpy.UpgradeDataset_management(TempClass)

    print ("Import Done")

# 3. Append
    arcpy.Append_management(TempClass, OutClass, "NO_TEST")

    print ("Append Done")

### Main Program ****

# Set paths 
    
ScriptPath = os.getcwd()
OutGDB =  ScriptPath[:-17] + "\\OrMapPFTemplate.gdb"
WorkGDB =  ScriptPath[:-17] + "\\Default.gdb"
InGDB =  ScriptPath[:-24] + "geodb\\townedgeo.gdb"

print (InGDB)
print (WorkGDB)

# input Anno Classes 

AnnoCllasses = ["Anno0100Scale", "Anno0200Scale", "Anno0400Scale", "Anno2000Scale","TaxlotNumberAnno","TaxcodeAnno"]

# for each class import

for c in AnnoCllasses:
    TempClass = WorkGDB + "//AnnoX" 
    InClass = InGDB + "//" + c 
    OutClass = OutGDB + "//" + c
    ImportAnno(InClass,TempClass,OutClass)
    print ("Class Done: " + c) 
    
