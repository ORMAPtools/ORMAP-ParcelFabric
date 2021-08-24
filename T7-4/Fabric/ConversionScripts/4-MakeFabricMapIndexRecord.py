# MakeFabric.py
#
# Sample Code  
#
# Creates a taxlot polygon feature class from the centroids of the geodb taxlots and the recenttly converted taxlotlines
# Once does the fabric create process.I used the Mapnumber just to see if it would work
#
#
# Dependencies
#   OutGDB = Path for pro geodatabase 
#   InGDB =" Path for arcmap geodatabase
#   WorgGdb = Path for pro geodatabase temp feature classes 
#
#   PFGDB = Path for pro geodatabase 
#   TaxlotLinesTMP - This is a PRO CoGo line feature class appended the ImportCoGoLines.py. This feature class is a copy
#      uses the same field definitions as the Fabric Taxlot_lines in the TaxlotFD (part of the fabric)
#
# 
# Dean - 8/7/2020 


import arcpy,os 


#  Set Paths

ScriptPath = os.getcwd()
OutGDB =  ScriptPath[:-17] + "\\OrMapPFTemplate.gdb"
WorkGDB =  ScriptPath[:-17] + "\\Default.gdb"
InGDB =  ScriptPath[:-24] + "geodb\\townedgeo.gdb"


InTaxLotsPly = InGDB + "/TaxlotsFD/Taxlot"

TaxlotPlyExp = WorkGDB  + "/TaxlotPlyExp"
TaxlotPlyTmp = WorkGDB  + "/TaxlotPlyTmp"
TaxlotPtTmp = WorkGDB  + "/TaxlotPtTmp"

TaxlotLn = OutGDB  + "/TaxlotsFD/Taxlot_Lines"
PF = OutGDB + "/TaxlotsFD/TaxlotsPF"
OutClassTxLtPly = OutGDB + "/TaxlotsFD/Taxlot"

OutClassPoints = OutGDB + "/TaxlotsFD/TaxlotsPF_Points"

# Delete Old data

arcpy.Delete_management(TaxlotPtTmp)
arcpy.Delete_management(TaxlotPlyTmp)
arcpy.Delete_management(TaxlotPlyExp)
arcpy.DeleteFeatures_management(OutClassTxLtPly)
arcpy.parcel.DisableParcelTopology(PF)
print ("prep done")

# Create the new taxlot polygon fc 

arcpy.MultipartToSinglepart_management(InTaxLotsPly,TaxlotPlyExp)
arcpy.FeatureToPoint_management(TaxlotPlyExp,TaxlotPtTmp, "INSIDE")
arcpy.FeatureToPolygon_management(TaxlotLn,TaxlotPlyTmp,"","ATTRIBUTES", TaxlotPtTmp)
print ("Polygon features made")

# Do the fabric thing...

# 1. Append polygons to fabric taxlot polygons 
arcpy.Append_management(TaxlotPlyTmp, OutClassTxLtPly, "NO_TEST")
# 2. Enable Parcel Topology 
arcpy.parcel.EnableParcelTopology(PF)
# 3. Build parcels 
arcpy.parcel.BuildParcelFabric(PF)
# 4. Create parcel records for polygons 
arcpy.parcel.CreateParcelRecords(OutClassTxLtPly, 'MapNumber')

print ("fabric Made") 
