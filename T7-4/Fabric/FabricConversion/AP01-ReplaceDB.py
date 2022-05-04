#0-ReplaceDB.py
#
# Replaces db with a backup.  Faster then deleting all features
# Also creates a "clean" database every time
#
#
# Database dependencies
#   Library = 'whever it is '
#    OutDb = Library +  "\\Fabric\\TownEd.gdb"
#    InDb = Library + "\\Fabric\\OrMapPFTemplatebk.gdb"
#    logfile = make sure your path is right
# 
# Dean - Spring 2021
# Dean - 8/30/21 - Updated to work on countywide dataset 

import os,arcpy,time,datetime,traceback,shutil

try:
    
    # Log File
    
    logfile = "D:\\GISLogs\\01APReplaceDB.txt"
    arcpy.Delete_management (logfile) 
    logfile = open(logfile, "w")   
    starttime =  datetime.datetime.now()
    logfile.write ('\n' + '\n' + "StartTime:" + str(starttime) + '\n' + '\n')
    print ("StartTime:" + str(starttime))

    #Library = 'P:\\ORMAProFabric\\TaxmapPolkV3.01\\'
    Library = 'P:\\ORMAProFabric\\T7-4V2.0\\'
    
    OutDb = Library +  "\\Fabric\\TownEd.gdb"
    InDb = Library + "\\Fabric\\TownEdBk.gdb"

    logfile.write ('\n'+ OutDb)

    # delete geodatabase and replace with back

    shutil.rmtree(OutDb)
    
    print ("OutDb Removed: " + OutDb)
    logfile.write ('\n' + "OutDb Removed: " + OutDb)
    
    shutil.copytree(InDb,OutDb)
    
    print ("Copy Done: " + OutDb)
    logfile.write ('\n' + "Copy Done: "+ OutDb)
        
    endtime =  datetime.datetime.now()
    timepassed = endtime - starttime 
  
    print ("Run Time: " + str(timepassed))
    print ( "Start-End Time: " + str(starttime) + "---" + str(endtime))
    logfile.write ('\n' + '\n' + "Feature Delete Succesful" + '\n' + '\n' )
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
