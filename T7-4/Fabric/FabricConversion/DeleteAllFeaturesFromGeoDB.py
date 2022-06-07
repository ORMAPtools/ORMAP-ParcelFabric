#0-DeleteFeatures.py
#
# Deletes all features in all feature classes in the fabric geodatabase 
# for the selected tile 
#
# Features deleted from feature class
#
# Change OutDB - to be the geodb you want features from feature classes deleted 
#          
#
# Dean - SprinG 2021 

import os,arcpy,time,datetime,traceback

try:
    
    
    starttime =  datetime.datetime.now()
    print ("StartTime:" + str(starttime))
    


    OutDb = "P:\ORMAProFabric\T7-4V2.02\Fabric\Townedbk.gdb" 
    arcpy.env.workspace = OutDb
    print (OutDb) 

    # get datasets and delete features
    
    datasets = arcpy.ListDatasets(feature_type='feature')
    datasets = [''] + datasets if datasets is not None else []

    for ds in datasets:
        for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
            print (fc)
            arcpy.management.DeleteFeatures(fc) 



    endtime =  datetime.datetime.now()
    timepassed = endtime - starttime 
    
    print ("Run Time: " + str(timepassed))
    print ( "Start-End Time: " + str(starttime) + "---" + str(endtime))
    

except:
    badness = traceback.format_exc()
    print ('\n' + '\n' + "*** BADNESS ****" + '\n' + '\n')
    print (badness)
    
    logfile.write ('\n' + '\n' + "**** BADNESS *****" + '\n' + '\n')
    logfile.write (badness)
    
    logfile.close()
