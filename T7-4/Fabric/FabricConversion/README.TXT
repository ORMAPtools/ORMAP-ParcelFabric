Fabric Conversion 

Location: T7-4\Fabric\FabricConversion

OVERVIEW 

Python Scripts 
AP01-ReplaceDB.py - Replace TownEd.gdb with clean empty copy (TownEdBK.gdb) 
AP02-ImportAnno.py - Convert annotation feature classes
AP03-ImportCogoLines.py - Convert CoGo lines for PLSS, TAXLOT_LINES, and ReferenceLines
AP04-ImportFCs.py - Import all other feature classes 
AP05-MakeFabric.py - Create the taxlot feature class and build fabric 
AP06-CalcMapTitle.py - Calculate the maptitle for MapIndex 

AP-DeleteFeatures.py - Not used in the bat file but can be useful. Deletes all features

BatFiles 
AP-00driveArcProPy.bat - runs conversion 


