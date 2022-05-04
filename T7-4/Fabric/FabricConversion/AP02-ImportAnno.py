# ImportAnno.py
#
# Sample Code - Imports annotation classes "Anno0100Scale", "Anno0200Scale", "Anno0400Scale", "Anno2000Scale","TaxlotNumberAnno","TaxcodeAnno"
# for a sample township from arcmap to arcpro
#
# Database Dependencies
#    Library = 'whever it is '
#    OutGDB =  Library + "\\Fabric\\TownEd.gdb"
#    WorkGDB =  Library + "\\Fabric\\Default.gdb"
#    InGDB =  Library +  "\\geodb\\townedgeo.gdb"
#   LogFile - make sure your path is right (c/d drive etc.) 
# 
# Dean - 8/7/2020
# Dean 8/30/21 - Updated to create countywide db
# 

import arcpy,os,time,datetime,traceback 

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
    
###################### Main Program ####################
try: 

    # Log File
    
    logfile = "D:\\GISLogs\\02APImportAnno.txt"
    arcpy.Delete_management (logfile) 
    logfile = open(logfile, "w")   
    starttime =  datetime.datetime.now()
    logfile.write ('\n' + '\n' + "StartTime:" + str(starttime) + '\n' + '\n')
    print ("StartTime:" + str(starttime))

    #Library = 'P:\\ORMAProFabric\\TaxmapPolkV3.01\\'
    Library = 'P:\\ORMAProFabric\\T7-4V2.0\\'
        
    OutGDB =  Library +  "\\Fabric\\TownEd.gdb"
    WorkGDB =  Library + "\\Fabric\\Default.gdb"
    InGDB =  Library + "\\geodb\\townedgeo.gdb"

    print (InGDB)
    print (WorkGDB)


    AnnoCllasses = ["Anno0100Scale", "Anno0200Scale", "Anno0400Scale", "Anno2000Scale","TaxlotsFD/TaxlotNumberAnno","TaxlotsFD/TaxcodeAnno"]

    for c in AnnoCllasses:
        TempClass = WorkGDB + "//AnnoX" 
        InClass = InGDB + "//" + c
        OutClass = OutGDB + "//" + c
        ImportAnno(InClass,TempClass,OutClass)
        print ("Class Done: " + c)
        logfile.write ('\n' + "classdone: "+ c)
        
    endtime =  datetime.datetime.now()
    timepassed = endtime - starttime 
    
    print ("Run Time: " + str(timepassed))
    print ( "Start-End Time: " + str(starttime) + "---" + str(endtime))
    logfile.write ('\n' + '\n' + "AnnImport Succesful" + '\n' + '\n' )
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
