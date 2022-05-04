#0-DeleteFeatures.py
#
# Deletes all features in all feature classes in the fabric geodatabase 
# for the selected tile 
#
# Outputs - Deleted Log File (OutDB - p:\aigis\libraries\county\fabric\towned.gdb
#           D:\GISLOGS\countydeletefeatures.txt
#          
#
# Dean - SprinG 2021 

import os,arcpy,time,datetime,traceback

try:
    
    Tile = 'T7-4'
    print (Tile) 
    # Log File
    
    logfile = "D:\\GISLogs\\" + Tile + "0deletefeatures.txt"
    arcpy.Delete_management (logfile) 
    logfile = open(logfile, "w")   
    starttime =  datetime.datetime.now()
    logfile.write ('\n' + '\n' + "StartTime:" + str(starttime) + '\n' + '\n')
    print ("StartTime:" + str(starttime))
    

    Library = 'D:\\FabricTest30\\'
    #Library = '\\\\earth\\vol1\\gis\\AIGIS\\libraries\\taxmap\\'
    OutDb = Library + Tile + "\\Fabric\\TownEd.gdb"
    arcpy.env.workspace = OutDb
    print (OutDb) 
    logfile.write ('\n'+ OutDb)

    # get datasets and delete features
    
    datasets = arcpy.ListDatasets(feature_type='feature')
    datasets = [''] + datasets if datasets is not None else []

    for ds in datasets:
        for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
            print (fc)
            logfile.write ('\n'+ fc)
            arcpy.management.DeleteFeatures(fc) 
            logfile.write ('\n'+ fc + ' Done')


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
