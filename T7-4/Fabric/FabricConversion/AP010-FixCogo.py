# FixCogo 
#
# Ensures COGO Attributes are correct 
#
# Inputs: OutGDB - New ORMAP Geodatabase
#         COGO Feature Classes (PLSSLines, Taxlot_Lines, ReferenceLines)
#
# Rules - If No Value set to Null (appears to be done) 
#       - If Distance is Null and arclenght is null then all are null 
#       - Round Off Direction = round(!Direction!,4)
#
# Outputs: Cogo Attributes set to correct values 
#
#
# Dependencies
#   Library - path where stuff is
#   log file - make sure path is right (D:\\GISLOGS)
#
# For this to Work the Attribute Rules each layer that involve mapindex must be temporarily disabled - done in this app 
#
# Note: Tried to use cursor but curses hate nulls. 
#
# Dean 12/2021 


import os,arcpy,time,datetime,traceback
     

def FixCogo(FeatureClass):

    
    # make direction null when no distance 
    whereclause = "Direction IS NOT NULL And Distance IS NULL And ArcLength IS NULL"
    arcpy.MakeFeatureLayer_management(FeatureClass, "FixBadDirection_lyr",whereclause)
    arcpy.CalculateField_management("FixBadDirection_lyr", "Direction", 'None', "PYTHON", "")
    print ("Direction Fixed")
    logfile.write ('\n' + "Direction Fixed")
    arcpy.Delete_management("FixBadDirection_lyr")
    
    # round off direction to 4 sig digits following decimal  
    whereclause = "Direction IS NOT NULL"
    arcpy.MakeFeatureLayer_management(FeatureClass, "RoundDirection_lyr",whereclause)
    arcpy.CalculateField_management("RoundDirection_lyr", "Direction", 'round(!Direction!,4)', "PYTHON", "")        
    print ("Direction Rounded Off")
    logfile.write ('\n' + "Direction Rounded")
    arcpy.Delete_management("RoundDirection_lyr")
    
    
try:

    logfile = "D:\\GISLogs\\10FixCogo.txt"
    arcpy.Delete_management (logfile) 
    logfile = open(logfile, "w")   
    starttime =  datetime.datetime.now()
    logfile.write ('\n' + '\n' + "StartTime:" + str(starttime) + '\n' + '\n')
    print ("StartTime:" + str(starttime))

    #Library = 'C:\\TaxmapPolkV3.01\\'
    Library = 'P:\\ORMAProFabric\\T7-4V2.0\\' 

    OutGDB =  Library +  "\\Fabric\\TownEd.gdb"


    FeatureClasses = ["PLSSLines","ReferenceLines","TaxlotsFD/TaxlotLines"]
    #FeatureClasses = ["ReferenceLines"]

    for c in FeatureClasses:
        print (c)
        logfile.write ('\n' + c)
        if c == "TaxlotsFD/TaxlotLines":
            OutClass = OutGDB + "\\" + "TaxlotsFD/Taxlot_Lines"
            FixCogo(OutClass)
        else:
            OutClass = OutGDB + "\\" + c
            
            arcpy.DisableAttributeRules_management(OutClass, 'GetMapNumber')
            arcpy.DisableAttributeRules_management(OutClass, 'GetMapScale')
            FixCogo(OutClass)           
            arcpy.EnableAttributeRules_management(OutClass, 'GetMapNumber')
            arcpy.EnableAttributeRules_management(OutClass, 'GetMapScale')
            
    endtime =  datetime.datetime.now()
    timepassed = endtime - starttime 
    
    print ("Run Time: " + str(timepassed))
    print ( "Start-End Time: " + str(starttime) + "---" + str(endtime))
    logfile.write ('\n' + '\n' + "Fix Cogo Succesfull" + '\n' + '\n' )
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
