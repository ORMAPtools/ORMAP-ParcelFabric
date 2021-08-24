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
# Note: Converts T/R/S to Integer and back to string to get rid of leading 0 
#
# This code can be added to for more complex map titles
#
# Dean 12/2020 



import arcpy, os, sys

# Set Paths

ScriptPath = os.getcwd()
OutGDB =  ScriptPath[:-17] + "\\OrMapPFTemplate.gdb"
MapIndex = OutGDB + "//MapIndex"

MapAngle = 1.8             # Assign mapangle if you have not done so

# MapAngle = None

# Build the map tile from the the ORMAPNUMBER to meet the Polk County Structure
#
#  1:100 - N.E.1/4  S.W.1/4 SEC. 30 T.7 S. R.4 W. W.M.
#  1:200 - S.W.1/4 SEC. 30 T.7 S. R.4 W. W.M.
#  1:400 - SEC. 1 T.7 S. R.4 W. W.M.
#

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
        if MapAngle != None: row[2] =  MapAngle    
        cursor.updateRow(row)
