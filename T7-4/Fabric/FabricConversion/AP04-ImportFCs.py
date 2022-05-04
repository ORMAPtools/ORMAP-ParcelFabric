# ImportFCs.py
#
# Sample Code - Imports feature classes (poly and non-cogo lines)
#   "WaterLines","Water","CartographicLines","TaxlotsFD/Taxcode","TaxlotsFD/MapIndex","TaxlotsFD/TaxcodeLines"
#    Whatever is in FCClasses collection
# 
# This is just a simple append
# 
# DB Dependencies
#   Managed as variables..
#
#    Library = 'whever it is' 
#    OutGDB =  Library + "\\Fabric\\TownEd.gdb"
#    WorkGDB =  Library +  "\\Fabric\\Default.gdb"
#    InGDB =  Library + "\\geodb\\townedgeo.gdb"
#    logfile - make sure your path is rght!
# 
# Important:  The last class is CORNER as I then use the OUTCLASS to calc all the isfixed to be true as these are corner points
#  This will DIE if the CORNER featcure class is not the last one in the list. 
# 
# Dean - 8/7/2020
# Update - Dean made to work with county-wide data 8/30/2021 

import os,arcpy,time,datetime,traceback

def ImportFC(InClass,OutClass,fc):

    # Prep Data
    arcpy.management.DeleteFeatures(OutClass)
    
    # Append
    arcpy.management.Append(InClass, OutClass, "NO_TEST")

    if fc == "CartographicLines":
        arcpy.SimplifyByStraightLinesAndCircularArcs_edit(OutClass, ".1 feet") 

def ImportSourceFC(InClass,OutClass,fc,WorkGDB):

    TempFC = WorkGDB + "//TempFC"
    
    # Prep Data
    arcpy.management.Delete(TempFC)
    arcpy.management.DeleteFeatures(OutClass)
     
    # Update Source 
    arcpy.management.Copy(InClass,TempFC)
    UpdateSource(TempFC) 

     # Append
 
    arcpy.management.Append(TempFC, OutClass, "NO_TEST")

    if fc == "CartographicLines":
        arcpy.SimplifyByStraightLinesAndCircularArcs_edit(OutClass, ".1 feet")
        
def UpdateSource(SimpClass):
    
    arcpy.AlterField_management(SimpClass, 'Source', 'OldSource', 'OldSource')
    arcpy.AddField_management(SimpClass, "Source", "Text", 255)
                                
    arcpy.MakeFeatureLayer_management(SimpClass,'SimpClassLyr')

    exp = "Autowho IS NOT NULL"
    arcpy.SelectLayerByAttribute_management('SimpClassLyr',"NEW_SELECTION", exp)
    calcexp =  "!OldSource! + '--' + !AutoWho!"                              
    arcpy.management.CalculateField ('SimpClassLyr','source',calcexp)
    print ("WhoDone")
                                
    exp = "AutoDate IS NOT NULL"
    arcpy.SelectLayerByAttribute_management('SimpClassLyr',"NEW_SELECTION", exp)
    calcexp =  "!Source! + '--' + str(!AutoDate!)"  
    arcpy.management.CalculateField ('SimpClassLyr','source',calcexp)
    print ("DateDone")                            

    arcpy.Delete_management('SimpClassLyr')
    
########### Main Program ###################

try:

    # Log File
    
    logfile = "D:\\GISLogs\\04APImportFCs.txt"
    arcpy.Delete_management (logfile) 
    logfile = open(logfile, "w")   
    starttime =  datetime.datetime.now()
    logfile.write ('\n' + '\n' + "StartTime:" + str(starttime) + '\n' + '\n')
    print ("StartTime:" + str(starttime))

    #Library = 'P:\\ORMAProFabric\\TaxmapPolkV3.01\\'
    Library = 'P:\\ORMAProFabric\\T7-4V2.0\\'
        
    OutGDB =  Library +  "\\Fabric\\TownEd.gdb"
    WorkGDB =  Library +  "\\Fabric\\Default.gdb"
    InGDB =  Library + "\\geodb\\townedgeo.gdb"
    
# Features without source 

    FCClasses = ["CartographicLines","TaxlotsFD/TaxLotPoints","TaxlotsFD/MapindexLines","TaxlotsFD/TaxcodePoints","TaxlotsFD/MapIndexPoints","TaxlotsFD/Taxcode","TaxlotsFD/MapIndex","TaxlotsFD/TaxCodeLines"]

    
    for c in FCClasses:
        InClass = InGDB + "/" + c 
        OutClass = OutGDB + "/" + c
        if c == "Corner":
            OutClass = OutGDB + "/" + "TaxlotsFD/TaxlotsPF_Points"
        elif c == "TaxlotsFD/TaxCodeLines":
            OutClass = OutGDB + "/" + "TaxlotsFD/TaxCode_Lines"
        else:
            OutClass = OutGDB + "/" + c
        ImportFC(InClass,OutClass,c)
        print ("Class Done: " + c)
        logfile.write ('\n' + "Class done: "+ c)       

# Features that need source updated 

    FCClasses = ["WaterLines","Water","Corner"]

    
    for c in FCClasses:
        print ('start -' + c)
        InClass = InGDB + "/" + c 
        OutClass = OutGDB + "/" + c
        if c == "Corner":
            OutClass = OutGDB + "/" + "TaxlotsFD/TaxlotsPF_Points"
        elif c == "TaxlotsFD/TaxCodeLines":
            OutClass = OutGDB + "/" + "TaxlotsFD/TaxCode_Lines"
        else:
            OutClass = OutGDB + "/" + c
        ImportSourceFC(InClass,OutClass,c,WorkGDB)
        print ("Class Done: " + c)
        logfile.write ('\n' + "Class done: "+ c) 


    print (OutClass)
    # this only applys to last FC in list witch is corners 
    arcpy.CalculateField_management(OutClass, "IsFixed", True, "PYTHON3")
    #arcpy.CalculateField_management(OutClass, "IsFixed", True, "PYTHON3")
    
    endtime =  datetime.datetime.now()
    timepassed = endtime - starttime 
    
    print ("Run Time: " + str(timepassed))
    print ( "Start-End Time: " + str(starttime) + "---" + str(endtime))
    logfile.write ('\n' + '\n' + "FC Import Succesful" + '\n' + '\n' )
    logfile.write ('\n' + '\n' + "Run Time: " + str(timepassed) + '\n' + '\n' )
    logfile.write ('\n' + '\n' +  str(starttime) + "---" + str(endtime))
                   
    logfile.close()
    

except:
    badness = traceback.format_exc()
    print ('\n' + '\n' + "*** BADNESS ****" + '\n' + '\n')
    print (badness)
    
    logfile.write ('\n' + '\n' + "**** BADNESS *****" + '\n' + '\n')
    logfile.write (badness)
    
    logfile.close()
    
