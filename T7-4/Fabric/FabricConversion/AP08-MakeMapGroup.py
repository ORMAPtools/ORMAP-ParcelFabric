# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 1. MakeMapGroup.py
#
# Purpose: Creates a county-wide mapgroup (tile) boundary polygon featureclass
# called
# MapGroup
# 
# Inputs:   Mapindex fc from each tile -- aigis/libraries/taxmap... 
# 
# Outputs:  MapGroup FC aigis/libraries/taxmap/county/geodb/taxmapedgeo.gdb
#
#
# Dependencies
#   Library - path where stuff is
#   log file - make sure path is right (D:\\GISLOGS)
#    tile - set to T7-4 Whatever tile you want to call it for the group 
#
# Author: Dean - Spring 2021
#
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy,os,time,datetime,traceback

# logfile
arcpy.Delete_management ("D:\\GISLogs\\08MakeMapGroupLog.txt")
logfile = open("D:\\GISLogs\\08MakeMapGroupLog.txt", "w")
logfile.write ("Make MapGroupe Log"+ '\n')

starttime =  datetime.datetime.now()
logfile.write ('\n' + '\n' + "StartTime:" + str(starttime) + '\n' + '\n')
print ("StartTime:" + str(starttime))

try: 
                
######### Main Program ####################
    
# Local variables:

    Tile = "T7-4"
    
    #Library = 'P:\\ORMAProFabric\\TaxmapPolkV3.01\\'
    Library = 'P:\\ORMAProFabric\\T7-4V2.0\\'
    
    OutGDB =  Library + "\\Fabric\\TownEd.gdb"
    WorkGDB =  Library + "\\Fabric\\Default.gdb"
    InGDB =  Library + "\\geodb\\townedgeo.gdb"

    MapGroup = OutGDB + "\\MapGroup"
    TempMapGroup = WorkGDB + "\\TempMapGroup"

    Tiles = [Tile]

   
# Create feature class

    print ("Start")
    logfile.write ("Start - Delete Temps and Old features"+ '\n')

# empty existing feature classes

    arcpy.DeleteFeatures_management(MapGroup)    
    
# collection variables to pull towned library tiles 
     
    for Tile in Tiles:
        MapIndexForTile = InGDB + "\\TaxlotsFD\\MapIndex"
        arcpy.Delete_management(TempMapGroup)
        arcpy.Dissolve_management(MapIndexForTile,TempMapGroup,"PageNumber")
                                  
        arcpy.management.AddField(TempMapGroup, "MapGroup", "Text", 255, "", "", "", "", "")
        arcpy.CalculateField_management(TempMapGroup, "MapGroup", "'" + Tile + "'", "PYTHON", "")
              
        arcpy.Append_management(TempMapGroup, MapGroup, "NO_TEST","","")
        print ("Appended Mapgroup: " + Tile)
                                                    
# Finish Up

    endtime =  datetime.datetime.now()
    timepassed = endtime - starttime 
    
    print ("Run Time: " + str(timepassed))
    print ( "Start-End Time: " + str(starttime) + "---" + str(endtime))
    logfile.write ('\n' + '\n' + "GetTileNames" + '\n' + '\n' )
    logfile.write ('\n' + '\n' + "Run Time: " + str(timepassed) + '\n' + '\n' )
    logfile.write ('\n' + '\n' +  str(starttime) + "---" + str(endtime))
                   
    logfile.close()
    
# -----------------------------------------------------------------------------------

except:
    badness = traceback.format_exc()
    print ('\n' + '\n' + "*** BADNESS ****" + '\n' + '\n')
    print (badness)
    
    logfile.write ('\n' + '\n' + "**** BADNESS *****" + '\n' + '\n')
    logfile.write (badness)
    
    logfile.close()
    

        

    
    
    
