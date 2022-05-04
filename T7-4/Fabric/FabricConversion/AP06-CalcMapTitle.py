# CalcMapTitle
#
# Calcs map title using the ORMAPNum
#
# Inputs: OutGDB - New ORMAP Geodatabase
#         MapIndex - The MapIndex Feature Class
#
# Outputs: Title calculated from ORMAPNUM - Easy to add additional title stuff here
#       ALSO --- Now is a good time to calc default map angle if you have one
#
# Dependencies
#   Library - path where stuff is
#   log file - make sure path is right (D:\\GISLOGS)
# 
# Note: Converts T/R/S to Integer and back to string to get rid of leading 0 
#
# This code can be added to for more complex map titles
#
# Dean 12/2020 



import os,arcpy,time,datetime,traceback

try:


    logfile = "D:\\GISLogs\\06APCalcMapTitle.txt"
    arcpy.Delete_management (logfile) 
    logfile = open(logfile, "w")   
    starttime =  datetime.datetime.now()
    logfile.write ('\n' + '\n' + "StartTime:" + str(starttime) + '\n' + '\n')
    print ("StartTime:" + str(starttime))


    #Library = 'P:\\ORMAProFabric\\TaxmapPolkV3.01\\'
    Library = 'P:\\ORMAProFabric\\T7-4V2.0\\'
    
    OutGDB =  Library + "\\Fabric\\TownEd.gdb"


    MapIndex = OutGDB + "//MapIndex"

    MapAngle = 1.8             # Assign mapangle if you have not done so 
    # MapAngle = None

    with arcpy.da.UpdateCursor(MapIndex, ["OrmapNum","maptitle","MapAngle"]) as cursor:
        for row in cursor:
            ORMAPNUM = row[0]
            MapTitle = row[1]
            T = int(ORMAPNUM[2:4])
            TP = ORMAPNUM[4:7]
            TD = ORMAPNUM[7]
            R = int(ORMAPNUM[8:10])
            RP = ORMAPNUM[10:13]
            RD = ORMAPNUM[13]
            S = ORMAPNUM[14:16]
            Q = ORMAPNUM[16]
            QQ =ORMAPNUM[17]
            A = ORMAPNUM[18:20]
            MST = ORMAPNUM[20]
            MSN = ORMAPNUM[21:24]

            qs = ['',' N.E.1/4 ',' N.W.1/4 ',' S.W.1/4 ',' S.E.1/4 ']
            qtrs = ['0','A','B','C','D']
            Title = "T." + str(T) + " " + TD + ". R." + str(R) + " " + RD + ". W.M."
            if S != "00":
                S = int(S)
                QT = ""
                QQT = "" 
                x = 0
                for q in qtrs:
                    arcpy.AddMessage(x) 
                    if q == Q:
                        QT = qs[x]
                    if q == QQ:
                        QQT = qs[x] 
                    x = x + 1
                Title = QQT + QT + "SEC. " + str(S) + ' ' + Title
            row[1] = Title
            print (Title)
            logfile.write ('\n' + Title)
    
            if MapAngle != None: row[2] =  MapAngle    
            cursor.updateRow(row)
            
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
