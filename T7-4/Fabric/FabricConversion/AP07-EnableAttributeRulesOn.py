#0-EnableDisableAttributeRules.py
#
# Rules set to "On" will enable attribute rules. 
#
# Inputs: All feature classes in Geodatabase
#
# Outputs: All feature class in Geodatabase with attribute rules either turned on or off
#
#   Dependencies
#   Library - path where stuff is
#   log file - make sure path is right (D:\\GISLOGS)
#
# Dean - 11/2020

import os,arcpy,time,datetime,traceback,shutil


def DisableRules(FC,ruletypes):
    desc = arcpy.Describe(fc).attributeRules
    for rule in desc:
        for rtype in ruletypes:
            rtypeesri = "esriART" + rtype
            print (rtypeesri)
            if rule.isEnabled == True and rule.type == rtypeesri:
                print("Disabling " + rtype + " rule: {}".format(rule.name))
                arcpy.DisableAttributeRules_management(fc, rule.name)
            
def EnableRules(FC,ruletypes):
    desc = arcpy.Describe(fc).attributeRules
    for rule in desc:
         for rtype in ruletypes:
            rtypeesri = "esriART" + rtype
            #print (rtypeesri)
            if rule.isEnabled == False and rule.type == rtypeesri:
                print("Enabling " + rtype + " rule: {}".format(rule.name))
                arcpy.EnableAttributeRules_management(fc, rule.name)

#######################################
                
try:
    logfile = "D:\\GISLogs\\07-UpdateAttributeRules.txt"
    arcpy.Delete_management (logfile) 
    logfile = open(logfile, "w")   
    starttime =  datetime.datetime.now()
    logfile.write ('\n' + '\n' + "StartTime:" + str(starttime) + '\n' + '\n')
    print ("StartTime:" + str(starttime))
    
    Rules = "On"
    
    #Library = 'P:\\ORMAProFabric\\TaxmapPolkV3.01\\'
    Library = 'P:\\ORMAProFabric\\T7-4V2.0\\'
        
    OutDb = Library + "\\Fabric\\TownEd.gdb"

    FabricPath = OutDb    
    arcpy.env.workspace = FabricPath
        
    FCs = ["Taxlot_lines","Taxlot","TaxlotPoints","Taxcode","Taxcode_lines","CartographicLines","Anno0100Scale","Anno0200Scale","Anno0400Scale","Anno2000Scale","Anno0100Scale","PLSSLINES","ReferenceLines","WaterLines","TaxCodeAnno","TaxlotNumberAnno","ConstructionLines"]
                
    datasets = arcpy.ListDatasets(feature_type='feature')
    datasets = [''] + datasets if datasets is not None else []
    #ruletypes = ["Constraint","Calculation","Validation"]
    ruletypes = ["Calculation"]
    
    for ds in datasets:
        #for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        for fc in FCs: 
            print (fc)
            logfile.write ('\n' + fc) 
            path = os.path.join(arcpy.env.workspace, ds, fc)
            if Rules == "On":
                EnableRules(fc,ruletypes)
            else:
                DisableRules(fc,ruletypes)

    endtime =  datetime.datetime.now()
    timepassed = endtime - starttime 
    
    print ("Run Time: " + str(timepassed))
    print ( "Start-End Time: " + str(starttime) + "---" + str(endtime))
    logfile.write ('\n' + '\n' + "Calc Map Title Succesfule" + '\n' + '\n' )
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
    
