# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 1. ImportCancelledNumbers.py
#
# Purpose: Replaces cancelled number table with table from geodb. 
# 
# Inputs:   Cancelled number table from geodb 
# 
# Outputs:  New Cancelled number table 
#
# Dependencies
#   Library - path where stuff is
#   log file - make sure path is right (D:\\GISLOGS)
#
# Author: Dean - Fall 2022
#
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy,os,time,datetime,traceback

# logfile
arcpy.Delete_management ("D:\\GISLogs\\09ImportCancelledNumbers.txt")
logfile = open("D:\\GISLogs\\09ImportCancelledNumbers", "w")
logfile.write ("Import Cancelled Numbers"+ '\n')

starttime =  datetime.datetime.now()
logfile.write ('\n' + '\n' + "StartTime:" + str(starttime) + '\n' + '\n')
print ("StartTime:" + str(starttime))

try: 
                
######### Main Program ####################
    
# Local variables:

    
    Library = 'P:\\ORMAProFabric\\T7-4V2.0\\'    
    OutGDB =  Library + "Fabric\\TownEd.gdb"
    InGDB =  Library +  "geodb\\townedgeo.gdb"

    OutCancelledNumberTable  = OutGDB + "\\CancelledNumbers"
    InCancelledNumberTable  = InGDB + "\\CancelledNumbers"

   
# Create feature class

    print ("Start")
    logfile.write ("Start - Delete Temps and Old features"+ '\n')

# Delete then copy the cancelled number table from the geodb to the newdb 

    arcpy.management.Delete(OutCancelledNumberTable)    
    arcpy.management.Copy (InCancelledNumberTable,OutCancelledNumberTable)

# Combine si and taxlot for those that have it
    
    whereclause = "S_I_Type IS NOT NULL"
    arcpy.management.MakeTableView(OutCancelledNumberTable, "CancelledNumberTble",whereclause)
    arcpy.management.CalculateField("CancelledNumberTble", "Taxlot", '!TaxLot! + !S_I_Type! + str(!S_I_Number!)', "PYTHON", "")   
                                                    
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
    

        

    
    
    
