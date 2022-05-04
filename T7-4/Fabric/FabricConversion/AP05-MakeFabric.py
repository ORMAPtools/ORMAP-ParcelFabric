# MakeFabric.py
#
# converts taxlot_lines (from previous cogo conversion) and geodb taxlot polygons into a fabric feature class
# The build will also build 
#
# DB Dependencies
#   Managed as variables..
#
#    Library = 'whever you are'
#    OutGDB =  Library +  "\\Fabric\\TownEd.gdb"
#    WorkGDB =  Library + "\\Fabric\\Default.gdb"
#    InGDB =  Library + "\\geodb\\townedgeo.gdb"
#    logfile = check path of log file (D:\\GISLogs\\)
# 
#   PFGDB = Path for pro geodatabase 
#   TaxlotLinesTMP - This is a PRO CoGo line feature class appended the ImportCoGoLines.py. This feature class is a copy
#      uses the same field definitions as the Fabric Taxlot_lines in the TaxlotFD (part of the fabric)
#
# For the Record Field when building records I used the Mapnumber just to see if it would work
# 
# Dean - 8/7/2020
# Update - Dean - Made to work on countywide database


import os,arcpy,time,datetime,traceback

try:

    logfile = "D:\\GISLogs\\" + "5MakeFabric.txt"
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

    InTaxLotsPly = InGDB + "/TaxlotsFD/Taxlot"

    TaxlotPlyExp = WorkGDB  + "/TaxlotPlyExp"
    TaxlotPlyTmp = WorkGDB  + "/TaxlotPlyTmp"
    TaxlotPtTmp = WorkGDB  + "/TaxlotPtTmp"

    TaxlotLn = OutGDB  + "/TaxlotsFD/Taxlot_Lines"
    TaxlotPt = OutGDB  + "/TaxlotsFD/TaxlotPoints"
    PF = OutGDB + "/TaxlotsFD/TaxlotsPF"
    OutClassTxLtPly = OutGDB + "/TaxlotsFD/Taxlot"

    OutClassPoints = OutGDB + "/TaxlotsFD/TaxlotsPF_Points"

    # Setup
    
    arcpy.Delete_management(TaxlotPtTmp)
    arcpy.Delete_management(TaxlotPlyTmp)
    arcpy.Delete_management(TaxlotPlyExp)
    arcpy.DeleteFeatures_management(OutClassTxLtPly)
    arcpy.parcel.DisableParcelTopology(PF)

    # Fix Bad Points
    
    
    print("Convert Mapnumber to T,R,S,QQ")

    arcpy.MakeFeatureLayer_management(TaxlotPt, "TaxlotPt_lyr","")
    cursor = ''
    row = ''
    MapLayerFields = ["MapNumber","Taxlot","MapTaxlot"]
    with arcpy.da.UpdateCursor("TaxlotPt_lyr",  MapLayerFields) as cursor:
        for row in cursor: 
            MapNumber = row[0]
            Taxlot = row[1]
            MapParts = MapNumber.split('.')
            Town = MapParts[0]
            Range = MapParts[1]
            mappartscount = 0 
            for p in MapParts:
                    mappartscount = mappartscount + 1
            # MapNumber is township Only  1:2000
            Qtr = "0"
            QtrQtr = "0" 
            arcpy.AddMessage ("Parts" + str(mappartscount))
            if mappartscount == 2:
                    Section = 0
            else:
                    # Mapnumber has Sections Only 1:400
                    QSec = MapParts[2]
                    if QSec.isdigit():
                            Section = int(QSec)
                    else:
                    # Mapnumber is 1:200 or 1:100 
                            cd = 0
                            ca = 0
                            sec = "" 
                            for s in QSec:
                                    if s.isalpha():
                                            if cd == 0:
                                                    Qtr = s
                                                    cd = 1
                                            else:
                                                    QtrQtr = s
                                    else:
                                            sec = sec + s 
                            Section = int(sec)
                            
            StrSec = str(Section)
            if Section < 10:
                StrSec = ' ' + str(Section)
            if Section == 0:
                StrSec = ''
            #print (MapNumber + '--' + str(Section) + '--' + StrSec) 
            Taxlotlen = len(Taxlot)
            Taxlot = str(Taxlot)
            if Taxlotlen == 2:
                Taxlot = '   ' + Taxlot           
            if Taxlotlen == 3:
                Taxlot = '  ' + Taxlot
            if Taxlotlen == 4:
                Taxlot = ' ' + Taxlot
            MapTaxlot = str(Town) + str(Range) + StrSec + Qtr + QtrQtr + Taxlot
            #print (MapNumber,Taxlot,MapTaxlot)    
            row[2] = MapTaxlot        
            cursor.updateRow(row)
            
        del row,cursor 

    # Fix Type
    
    whereclause = "SourceType IS NOT NULL"
    arcpy.MakeFeatureLayer_management(TaxlotPt, "FixSourceType_lyr",whereclause)
    arcpy.CalculateField_management("FixSourceType_lyr", "SourceType", "!SourceType!.lower()", "PYTHON", "")  
    arcpy.CalculateField_management("FixSourceType_lyr", "SourceType", "!SourceType!.capitalize()", "PYTHON", "")      
    arcpy.Delete_management("FixSourceType_lyr")

    print ("FixSourceType Done")
    logfile.write ('\n' + "FixSourceType done") 
                   
    # Create temporary Copies

    arcpy.FeatureToPolygon_management(TaxlotLn,TaxlotPlyTmp,"0.002 Feet","ATTRIBUTES", TaxlotPt)
    print ("Polygon features made")
    logfile.write ('\n' + "Prep done")
    
    # Do the fabric thing...
    # 1. Append polygons to fabric taxlot polygons 
    arcpy.Append_management(TaxlotPlyTmp, OutClassTxLtPly, "NO_TEST")
    logfile.write ('\n' + "Append done")
        
    # 2. Enable Parcel Topology 
    arcpy.parcel.EnableParcelTopology(PF)
    # 3. Build parcels 
    arcpy.parcel.BuildParcelFabric(PF)
    print ("Topology and Parcels Built")
    logfile.write ('\n' + "Topology and Parcels Built")
    
    # 4. Create parcel records for polygons 
    arcpy.parcel.CreateParcelRecords(OutClassTxLtPly, 'MapNumber')
    print ("Records Made")
    logfile.write ('\n' + "Records Made")   

    endtime =  datetime.datetime.now()
    timepassed = endtime - starttime 
    
    print ("Run Time: " + str(timepassed))
    print ( "Start-End Time: " + str(starttime) + "---" + str(endtime))
    logfile.write ('\n' + '\n' + "Makde Fabric Succesfule" + '\n' + '\n' )
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
