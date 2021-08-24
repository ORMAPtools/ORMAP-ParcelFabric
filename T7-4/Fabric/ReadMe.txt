ReadMe - Version 1.06
May 2021 

This is the sixth draft version of the ORMAP ArcPro data structure that includes Parcel Fabric 2.6.  This directory is an ArcPro workspace. The data contains a geodatabase of one township (T7-4) from Polk County.  The source data is in an ArcMap geodatabase in GEODB. 


Default.gdb - Started ESRI Database for project - contains working feature classes used in the conversion
ImportLog - Standard ESRI Log 
Index - Standard ESRI Index subdirectory 
ORMAPPFTemplate.gdp - The new database template (includes empty feature classes, fields, and domains) 
Default.tbx - contains zoom, mapupdate tools, label to annotation tool 
OtherCounties - Contins tools and samples from other counties (cancelednumbertool.tbx from Washington County)
Maps - test production map 
OrMapPF.aprx - ESRI project file - use this to look at the converted data 
ORMAPTOOLS - Python tools 


The conversion process converts the contents of the ArcMap Geodatabase in Geo to a new ArcPro Fabric Geodatabase in Fabric. 


00ImportAllPolk.bat - runs the entire conversion process for the t7-4 township

0-EnableDisableAttributeRulesOff.py - turn attribue rules off before starting (it goes faster) 
1-ImportAnno.py - this will APPEND your features into the template (ONLY works for 100,200,400,2000 anno. 
1-ImportReplaceAnno.py - This will replace your feature in the template 
2-ImportCogoLines.py - I hacked ESRI cogolines converter tool so it would run as a batch job. Too see the tool see (MigrateCOGO_toArcGIS_Pro.tbx)
                        This is annother append 
3-ImportFCs.py - Appends feature classes in the list to the new geodatabase. Converts corners to points. 
4-MakeFabricMapIndexRecord.py - creates a record for every map in the geodatabase with each taxlot part of that record. 
5-CalcMapTitle.py - calculates map title from the ORMAPNUMBER and allows you to assign values (like mapangle) for each map 
0-EnableDisableAttributeRulesOn.py - rule at the end to turn attribute rules back on. 

To Run this conversion.  Copy an Empty "OrMapPFTemplate.gdb" to the T7-4V1.06 directory and run the scripts in order as just described. 

