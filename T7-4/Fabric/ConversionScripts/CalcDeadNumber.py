
#CalcDeadNumber.py
#
# Converts maptaxlot, and SI into standard MapNumber and Taxlot (with SI Type and Number Appended)
#
# parces maptaxlot in view to convert it using an updatecursor
#
#
# Dean March 2021



import arcpy, os, sys

tabled = "C:\\Taxmap\\T7-4\\fabric\\Default.gdb\\All_Canceled_Numbers"

with arcpy.da.UpdateCursor(tabled,["Map_Taxlot","S_I_TYPE","S_I_Number","MapNumber","Taxlot"]) as cursor:
    for row in cursor:
        maptaxlot = row[0]
        sitype = row[1]
        sinumber = row[2]
        taxlot = maptaxlot[-5:].strip()

        if sitype != None: taxlot = taxlot + sitype + str(int(sinumber)) 
        if str(maptaxlot[:2]) == "10":
            tr = maptaxlot[0:2] + '.' + maptaxlot[2]
            if maptaxlot[3:5] != "00":
                s = int(maptaxlot[3:5])
                tr = tr + "." + str(s)
                if maptaxlot[5] != "0": tr = tr + maptaxlot[5]
                if maptaxlot[6] != "0": tr = tr + maptaxlot[6]
        else:
            tr = maptaxlot[0] + '.' + maptaxlot[1]
            if maptaxlot[2:4] != "00":
                s = int(maptaxlot[2:4])
                tr = tr + "." + str(s)
                if maptaxlot[4] != "0": tr = tr + maptaxlot[4]
                if maptaxlot[5] != "0": tr = tr + maptaxlot[5]
        row[3] = tr
        row[4] = taxlot 
        #print (maptaxlot + "==" + tr + "--" + taxlot)        
        cursor.updateRow(row)
print ("all done")
