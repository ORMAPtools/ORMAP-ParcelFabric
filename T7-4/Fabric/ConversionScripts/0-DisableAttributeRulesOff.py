#0-EnableDisableAttributeRulesOFF.py
#
# Rules set to "Off" will disenable attribute rules. If set to something
# else it will disable them. Also disables topology. 
#
# Inputs: All feature classes in Geodatabase
#
# Outputs: All feature class in Geodatabase with attribute rules either turned on or off
# 
# Dean - 11/2020

import os,arcpy


def DisableRules(FC,ruletypes):
    desc = arcpy.Describe(fc).attributeRules
    for rule in desc:
        for rtype in ruletypes:
            rtypeesri = "esriART" + rtype
            #print (rtypeesri)
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
        
Rules = "Off" 
            
ScriptPath = os.getcwd()
FabricPath =  ScriptPath[:-17] + "\\OrMapPFTemplate.gdb"      
arcpy.env.workspace = FabricPath

print (FabricPath)

datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []
ruletypes = ["Constraint","Calculation","Validation"]
    
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        print (fc) 
        path = os.path.join(arcpy.env.workspace, ds, fc)
        if Rules == "On":
            EnableRules(fc,ruletypes)
        else:
            DisableRules(fc,ruletypes)

# ALSO Disable Parcel Topology

TopoPath = FabricPath + "\\TaxlotsFD\\TaxlotsPF"
arcpy.DisableParcelTopology_parcel(TopoPath)
print ("NOTICE: Topology Disabled")

