#
# Name: ImportCoGoLines.py
#
# This is a hack on ESRI's tool for converting arcmap cogo feature classes to
# ArcPro Cogo feature classes (PLSSLINES, REFERENCELINES, TAXLOT_LINE)
# copies features with cogo attributes from geodatabase to new fabric 
#
# I added a front end to go the feature classes and a second function to
# process them before calling the main.  I also made assumptiongs about
# what attributes(used defaults from tool) would be used.
#
# DB Dependencies
#   Managed as variables..
#
#    Library = 'Wherever it is'
#    OutGDB =  Library +  "\\Fabric\\TownEd.gdb"
#    WorkGDB =  Library +  "\\Fabric\\Default.gdb"
#    InGDB =  Library +  "\\geodb\\townedgeo.gdb"
#    Logfile - make sure your path is righ (c/d drive) 
# 
# Dean 9/7/2020
# Update - Dean 8/30/2021 - Made to work with countywide dataset 
# 
#-------------------------------------------------------------------------------
# Name:         Migrate COGO To ArcGIS Pro
# Purpose:      Will migrate values from an ArcGIS 10.x COGO enabled feature class to the correct fields for an ArcGIS
#               Pro feature class.
# Author:       Esri
#
# Created:      12/23/2015
#-------------------------------------------------------------------------------

import arcpy,os,time,datetime,traceback 


#inputLineFeatureClass = arcpy.GetParameterAsText(0)
#inputProLineFC = arcpy.GetParameterAsText(1)

#outputErrorFC_Location = arcpy.GetParameterAsText(2)

#inputDirectionFormat = arcpy.GetParameterAsText(3)
#inputDirectionField = arcpy.GetParameterAsText(4)
#inputDistanceField = arcpy.GetParameterAsText(5)
#inputRadiusField = arcpy.GetParameterAsText(6)
#inputRadius2Field = arcpy.GetParameterAsText(7)
#inputCurveField = arcpy.GetParameterAsText(8)
#inputCurveType = arcpy.GetParameterAsText(9)
#inputCurveDirectionType = arcpy.GetParameterAsText(10)
#inputCurveDirectionField = arcpy.GetParameterAsText(11)

inputDirectionFormat = "Quadrant Bearing"
inputDirectionField = "Direction"
inputDistanceField = "Distance"
inputRadiusField = "Radius"
inputRadius2Field = "Radius2"
inputCurveField = "ArcLength"
inputCurveType = "Arc Length"
inputCurveDirectionType = "Field with L and R"
inputCurveDirectionField = "Side"

def ImportCogoLines(InClass,OutClass,TempClass):

    global inputLineFeatureClass
    global inputProLineFC
    global outputErrorFC_Location
    outputErrorFC_Location = None
    inputLineFeatureClass = InClass
    inputProLineFC = TempClass
     
    # Prep

    arcpy.Delete_management(TempClass)    
    arcpy.DeleteFeatures_management(OutClass)

    # Make a temp copy in outclass 
    main()
    # Append
    arcpy.Append_management(TempClass, OutClass, "NO_TEST")
    #arcpy.Append_management(InClass, OutClass, "NO_TEST")

def main():
   
    print (inputLineFeatureClass)
    print (inputProLineFC) 
    #These will be appended in place of the COGO Direction/Distacne/Radius/Arclength strings to maintain order
    fieldsToAdd = [("Direction", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED"),
                   ("Distance", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED"),
                   ("Radius", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED"),
                   ("ArcLength", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED"),
                   ("Radius2", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED")]

    #Error Fields will be extended at the end of the existing fields
    errorFieldsToAdd = [("ErrorType", "TEXT", "", "", "", "", "NULLABLE", ""),
                        ("Org_OID", "LONG", "", "", "", "", "NULLABLE", "")]

    #Gets all the source fields and then makes a list of all the names (lower cased) for cursors later
    sourceFields = addSourceFields()
    sourceFieldNames = [eachName[0].lower() for eachName in sourceFields]
    #This will prep the Pro FC to have the same Fields as the source except if those fields are in the
    #Fields to add list it will swap them out in place with the new fields to add.  If not it will
    #Append any remaining fields to add to the end of the list
    proFields = sourceFields[:]

    #For each of the input COGO fields change them to their representative new COGO fields
    proFields[sourceFieldNames.index(inputDirectionField.lower())] = fieldsToAdd[0]
    proFields[sourceFieldNames.index(inputDistanceField.lower())] = fieldsToAdd[1]
    proFields[sourceFieldNames.index(inputRadiusField.lower())] = fieldsToAdd[2]
    proFields[sourceFieldNames.index(inputCurveField.lower())] = fieldsToAdd[3]
    if inputRadius2Field:
        proFields[sourceFieldNames.index(inputRadius2Field.lower())] = fieldsToAdd[4]


    #ErrorFields will all be the same as the source plus some added fields
    errorFields = sourceFields[:]
    for eachField in errorFieldsToAdd:
        errorFields.append(eachField)

    createProCOGO_FeatureClass(sourceFields, proFields, errorFields)

    try:
        arcpy.EnableCOGO_management(inputProLineFC)
    except:
        pass #already enabled

def createProCOGO_FeatureClass(sourceFields, proFields, errorFields):

    #Gets spatial reference
    spatial_ref = arcpy.Describe(inputLineFeatureClass).spatialReference
    #If there is an output path for an error FC get the path and name
    if outputErrorFC_Location:
        outputErrorFC_Path, outputErrorFC_Name = os.path.split(outputErrorFC_Location)

    #Getting names of the Fields and changing "shape" to the catchall "shape@"
    sourceFieldNames = [eachName[0].lower() for eachName in sourceFields]
    sourceFieldNames[sourceFieldNames.index("shape")] = "shape@"
    proFieldNames = [eachName[0].lower() for eachName in proFields]
    proFieldNames[proFieldNames.index("shape")] = "shape@"
    errorFieldNames = [eachName[0].lower() for eachName in errorFields]
    errorFieldNames[errorFieldNames.index("shape")] = "shape@"

    arcpy.AddMessage("Loading all the lines into memory, this may take a moment...")

    inputLines = [list(eachRow) for eachRow in arcpy.da.SearchCursor(inputLineFeatureClass, sourceFieldNames)]
    errorLines = []
    arcpy.AddMessage("Converting COGO String values to numeric double values...")

    #Start looping through all the lines and converting the strings to floats
    for num, eachLine in enumerate(inputLines):

        #errorMessages will catch all the errors returned and originalInputLine will store the original value of the line
        errorMessages = []
        originalInputLine = eachLine[:]

        #Check if field exists.  If so and it is not None, convert it to float.  If that fails, put None in its place

        #Convert Direction
        #Check to see if the value is None or empty if that's the case transfer the empty value over with no error
        if checkFieldIsEmpty(inputLines, num, sourceFieldNames, inputDirectionField):
            if inputDirectionFormat == "Quadrant Bearing":
                try:
                    #Try to convert.  If in proper format it will work, other wise it will error
                    inputLines[num][sourceFieldNames.index(inputDirectionField.lower())] = \
                        float(Polar2Azimuth(Quad2Polar(eachLine[sourceFieldNames.index(inputDirectionField.lower())])))
                except:
                    errorMessages.append(importWarning(num, inputLines, sourceFieldNames, inputDirectionField.lower()))
                    inputLines[num][sourceFieldNames.index(inputDirectionField.lower())] = None
            elif inputDirectionFormat == "North Azimuth":
                try:
                    inputLines[num][sourceFieldNames.index(inputDirectionField.lower())] = \
                        float(eachLine[sourceFieldNames.index(inputDirectionField.lower())])
                except:
                    errorMessages.append(importWarning(num, inputLines, sourceFieldNames, inputDirectionField.lower()))
                    inputLines[num][sourceFieldNames.index(inputDirectionField.lower())] = None
        else:
            inputLines[num][sourceFieldNames.index(inputDirectionField.lower())] = None

        #Convert Distance
        #Check to see if Distance Field is there or not.  If so convert the string to a float
        if checkFieldIsEmpty(inputLines, num, sourceFieldNames, inputDistanceField):
            try:
                inputLines[num][sourceFieldNames.index(inputDistanceField.lower())] = \
                    float(eachLine[sourceFieldNames.index(inputDistanceField.lower())])
            except:
                errorMessages.append(importWarning(num, inputLines, sourceFieldNames, inputDistanceField.lower()))
        else:
            inputLines[num][sourceFieldNames.index(inputDistanceField.lower())] = None

        #Convert Radius
        #Check to see if Radius exists.  If so convert it and Null out the Distance (Old COGO had this field populated)
        if checkFieldIsEmpty(inputLines, num, sourceFieldNames, inputRadiusField):
            inputLines[num][sourceFieldNames.index(inputDistanceField.lower())] = None
            #Check how the curve direction is calculated.  If it already had +/- use that.  If it's L/R user the
            #Curve Direction Field to determine the direction of the curve
            if inputCurveDirectionType == "Positive and Negative Radius":
                try:
                    inputLines[num][sourceFieldNames.index(inputRadiusField.lower())] = \
                        float(eachLine[sourceFieldNames.index(inputRadiusField.lower())])
                except:
                    errorMessages.append(importWarning(num, inputLines, sourceFieldNames, inputRadiusField.lower()))
            elif inputCurveDirectionType == "Field with L and R":
                try:
                    if inputLines[num][sourceFieldNames.index(inputCurveDirectionField.lower())].lower() == "l":
                        inputLines[num][sourceFieldNames.index(inputRadiusField.lower())] = \
                            float(eachLine[sourceFieldNames.index(inputRadiusField.lower())]) * -1
                    else:
                        inputLines[num][sourceFieldNames.index(inputRadiusField.lower())] = \
                            float(eachLine[sourceFieldNames.index(inputRadiusField.lower())])
                except:
                    errorMessages.append(importWarning(num, inputLines, sourceFieldNames, inputRadiusField.lower()))
        else:
            inputLines[num][sourceFieldNames.index(inputRadiusField.lower())] = None

        #Convert Curve Parameter
        #Check how the curve is defined
        if inputCurveType == "Arc Length":
        #If it's arcLength just do a quick convert to float
            if checkFieldIsEmpty(inputLines, num, sourceFieldNames, inputCurveField):
                try:
                    inputLines[num][sourceFieldNames.index(inputCurveField.lower())] = \
                        float(eachLine[sourceFieldNames.index(inputCurveField.lower())])
                except:
                    errorMessages.append(importWarning(num, inputLines, sourceFieldNames, inputCurveField.lower()))
            else:
                inputLines[num][sourceFieldNames.index(inputCurveField.lower())] = None
        # TODO: Calc chord to arclength
        elif inputCurveType == "Chord":
            pass

        # TODO: Calc delta to arclenth
        elif inputCurveType == "Delta":
            pass

        # Convert Radius2 (if applicable)
        if inputRadius2Field:
            # Check to see if Radius exists.  If so convert it and Null out the Distance (Old COGO had this field populated)
            if checkFieldIsEmpty(inputLines, num, sourceFieldNames, inputRadius2Field):
                if inputCurveDirectionType == "Positive and Negative Radius":
                    try:
                        inputLines[num][sourceFieldNames.index(inputRadius2Field.lower())] = \
                            float(eachLine[sourceFieldNames.index(inputRadius2Field.lower())])
                    except:
                        errorMessages.append(importWarning(num, inputLines, sourceFieldNames, inputRadius2Field.lower()))
                elif inputCurveDirectionType == "Field with L and R":
                    try:
                        if inputLines[num][sourceFieldNames.index(inputCurveDirectionField.lower())].lower() == "l":
                            inputLines[num][sourceFieldNames.index(inputRadius2Field.lower())] = \
                                float(eachLine[sourceFieldNames.index(inputRadius2Field.lower())]) * -1
                        else:
                            inputLines[num][sourceFieldNames.index(inputRadius2Field.lower())] = \
                                float(eachLine[sourceFieldNames.index(inputRadius2Field.lower())])
                    except:
                        errorMessages.append(importWarning(num, inputLines, sourceFieldNames, inputRadius2Field.lower()))
            else:
                inputLines[num][sourceFieldNames.index(inputRadius2Field.lower())] = None


        #arcpy.AddMessage("InputLines =\n\t{}".format(inputLines[num]))
        #arcpy.AddMessage("Original Lines =\n\t{}".format(originalInputLine))
        #If any error messages were generated, take the originalInputLine and append it to the Error Line list
        if errorMessages:
            errorMessages = [each for each in errorMessages if each]
            errorLines.append(originalInputLine)
            #arcpy.AddMessage("Error Lines = \n\t{}".format(errorLines))
            #arcpy.AddMessage("Error Message =\n\t{}\nOrigOID = {}".format(errorMessages, inputLines[num][0]))

            errorLines[len(errorLines) - 1].extend((errorMessages[0], inputLines[num][0]))
        #quit()

    #Create feature class to be used in ArcGIS Pro
    arcpy.AddMessage("Creating COGO feature class for use in ArcGIS Pro...")
    inputProLineFC_Path, inputProLineFC_Name = os.path.split(inputProLineFC )
    try:
        proLineFC = arcpy.CreateFeatureclass_management(inputProLineFC_Path, inputProLineFC_Name, "POLYLINE", "", "", "", spatial_ref)
        addFields(proLineFC, proFields)
    except Exception as e:
        arcpy.AddError("Unable to create feature class: \nError: {}".format(e))
        quit()

    arcpy.AddMessage("Copying lines to COGO feature class...")
    with arcpy.da.InsertCursor(proLineFC, proFieldNames) as proLineFC_cursor:
        for eachLine in inputLines:
            proLineFC_cursor.insertRow(eachLine)

    #Create ERROR feature class to be used in ArcGIS Pro
    if outputErrorFC_Location:
        arcpy.AddMessage("Creating an Error COGO feature class for use in ArcGIS Pro...")
        try:
            errorLineFC = arcpy.CreateFeatureclass_management(outputErrorFC_Path, outputErrorFC_Name, "POLYLINE", "", "", "", spatial_ref)
            addFields(errorLineFC, errorFields)
        except Exception as e:
            arcpy.AddError("Unable to create feature class: \nError: {}".format(e))
            quit()

        arcpy.AddMessage("Copying lines to Error feature class...")
        with arcpy.da.InsertCursor(errorLineFC, errorFieldNames) as errorLineFC_cursor:
            for eachLine in errorLines:
                errorLineFC_cursor.insertRow(eachLine)

def checkFieldIsEmpty(inputLines, num, sourceFieldNames, field):
    """This is to check if a field in a list is empty"""
    if isinstance(inputLines[num][sourceFieldNames.index(field.lower())], str):
        if inputLines[num][sourceFieldNames.index(field.lower())] is not None and \
            inputLines[num][sourceFieldNames.index(field.lower())].strip() is not '':
            return True
        else:
            return False
    elif inputLines[num][sourceFieldNames.index(field.lower())] is not None:
        return True
    else:
        return False


def addSourceFields():
    #Get all the source fields and run a describe on the input feature class
    sourceFields = arcpy.ListFields(inputLineFeatureClass)
    fields = []
    #descSourceData = arcpy.Describe(inputLineFeatureClass)

    #If the user is passing fields into this method, don't add those fields from the source to the fieldsToAdd list
    #Also omit OID, Shape and Shape_Length
    #existingFieldsToAdd = [each[0].lower() for each in fieldsToAdd]
    #existingFieldsToAdd.extend((descSourceData.oidFieldName.lower(), descSourceData.shapeFieldName.lower(), "shape_length"))
    #"shape_length" can be removed if this method is used on a layer that is not a Polyline


    #Go through the source list and append each as tuple to the list.  Formatted to run in addField_management
    for sourceField in sourceFields:
        fields.append((sourceField.name,
                            sourceField.type,
                            sourceField.precision,
                            sourceField.scale,
                            sourceField.length,
                            sourceField.aliasName,
                            sourceField.isNullable,
                            sourceField.required,
                            sourceField.domain))
    return fields

#This function is used if any of the Try/Excepts fail during import.  It informs the user of failure
def importWarning(num, inputLines, inputFieldList, fieldName):

    errorType = ["One or more expected COGO fields are Null. ",
                 "One or more expected COGO fields have invalid values. "]

    if inputLines[num][inputFieldList.index(fieldName)] is None:
        inputLines[num][inputFieldList.index(fieldName)] = None
        return

    elif not (inputLines[num][inputFieldList.index(fieldName)]).strip():
         inputLines[num][inputFieldList.index(fieldName)] = None
         return

    else:
        #arcpy.AddWarning("Line OID: {} did not have a valid {}: {} and <null> has been entered.".format(inputLines[num][inputFieldList.index("OID@")], fieldName,
        #                                                                                                               inputLines[num][inputFieldList.index(fieldName)]))
        inputLines[num][inputFieldList.index(fieldName)] = None
        return errorType[1]

def addFields(featureClass, fieldsToAdd):

    #Creates a dictionary of the TargetFeatureClass fields {FieldName: FieldType}
    targetFieldList = arcpy.ListFields(featureClass)
    targetFieldNamesLowerCase = {each.name.lower(): each.type for each in targetFieldList}

    #Cycles through all the fields to add and checks if field already exists
    for eachField in fieldsToAdd:
        #Does the field exist?
        if eachField[0].lower() in targetFieldNamesLowerCase:
            #If the field does exist, is it the correct type?
            if targetFieldNamesLowerCase[eachField[0].lower()].lower() == eachField[1].lower():
                pass
                #For this script we don't need warnings since the source is empty
                #arcpy.AddWarning("{} field already exists and is the correct field type".format(eachField[0]))
            else:
                #Wrong type.  Throw Error, user must fix manually
                pass
                #For this script we don't need warnings since the source is empty
                #arcpy.AddWarning("{} field exists as {}. The correct field type is {}".format(eachField[0],
                #                                                                               targetFieldNamesLowerCase[eachField[0].lower()],
                #                                                                               eachField[1]))
        else:
            #Try to add field
            try:
                arcpy.AddField_management(*(featureClass,) + eachField)
                #arcpy.AddMessage("Field name: {} added successfully.".format(eachField[0].upper()))
            #Except: Error thrown if field fails to add (Locking...)
            except:
                arcpy.AddError("Failed to Add {} field...".format(eachField[0]))


def Quad2Polar(Quadbearing):

    if (Quadbearing.replace("N","").replace("S","").replace("E","").replace("W","").replace("-","").replace(" ","")).isdigit() != 1:
        return Quadbearing

    AngleStr = (Quadbearing.lstrip("NS ")).rstrip("EW ")

    if AngleStr.count("-") != 2:
        return Quadbearing
    else:
        AngleArray=AngleStr.split("-")
    try:
        deg=float(AngleArray[0])
        min=float(AngleArray[1])
        sec=float(AngleArray[2])
    except IndexError:
        return Quadbearing
    except ValueError:
        return Quadbearing
    alpha=deg+min/60+sec/3600
    if Quadbearing.find("N") != -1 and Quadbearing.find("E") != -1:
        polar=90-alpha
    elif Quadbearing.find("N") != -1 and Quadbearing.find("W") != -1:
        polar=90+alpha
    elif Quadbearing.find("S") != -1 and Quadbearing.find("W") != -1:
        polar=270-alpha
    elif Quadbearing.find("S") != -1 and Quadbearing.find("E") != -1:
        polar=270+alpha
    else:
        polar = - 5

    return polar

def Polar2Azimuth(polar):
    if polar <= 90:
        azimuth = 90 - polar
    else:
        azimuth = 450 - polar
    return azimuth

def UpdateSource(SimpClass):
    
    arcpy.AlterField_management(SimpClass, 'Source', 'OldSource', 'OldSource')
    arcpy.AddField_management(SimpClass, "Source", "Text", 255)
                                
    arcpy.MakeFeatureLayer_management(SimpClass,'SimpClassLyr')

    exp = "Autowho IS NOT NULL"
    arcpy.SelectLayerByAttribute_management('SimpClassLyr',"NEW_SELECTION", exp)
    calcexp =  "!OldSource! + '--' + !AutoWho!"                              
    arcpy.management.CalculateField ('SimpClassLyr','source',calcexp)
    print ("WhoDone")
                                
    exp = "AutoDate IS NOT NULL"
    arcpy.SelectLayerByAttribute_management('SimpClassLyr',"NEW_SELECTION", exp)
    calcexp =  "!Source! + '--' + str(!AutoDate!)"  
    arcpy.management.CalculateField ('SimpClassLyr','source',calcexp)
    print ("DateDone")                            

    arcpy.Delete_management('SimpClassLyr')
    
################# Main Program #####################
try:

    # Log File
    
    logfile = "D:\\GISLogs\\03APImportCogo.txt"
    arcpy.Delete_management (logfile) 
    logfile = open(logfile, "w")   
    starttime =  datetime.datetime.now()
    logfile.write ('\n' + '\n' + "StartTime:" + str(starttime) + '\n' + '\n')
    print ("StartTime:" + str(starttime))

    #Library = 'P:\\ORMAProFabric\\TaxmapPolkV3.01\\'
    Library = 'P:\\ORMAProFabric\\T7-4V2.0\\'
        
    OutGDB =  Library + "\\Fabric\\TownEd.gdb"
    WorkGDB =  Library + "\\Fabric\\Default.gdb"
    InGDB =  Library + "\\geodb\\townedgeo.gdb"

    TempClass = WorkGDB + "/" + "LineCogoX"
    SimpClass = WorkGDB + "/" + "LineCogoSp"


    FeatureClasses = ["PLSSLines","ReferenceLines","TaxlotsFD/TaxlotLines"]
    
    #FeatureClasses = ["ReferenceLines"]

    for c in FeatureClasses:
        InClass = InGDB + "/" + c 
        OutClass = OutGDB + "/" + c

        if c == "TaxlotsFD/TaxlotLines":
            OutClass = OutGDB + "/" + "TaxlotsFD/Taxlot_Lines"
        else:
            OutClass = OutGDB + "/" + c 

    # Added the simplify Arc Stuff at a .1 foot tolerance

        arcpy.Delete_management(SimpClass)    
        arcpy.Copy_management(InClass, SimpClass)

    # Recalced radius with infinity to be 0 - Dean Dec 2021 - Recommendation from Tim H. ESRI 

        whereclause = "Radius = 'INFINITY'"
        arcpy.MakeFeatureLayer_management(SimpClass, "FixInfinity_lyr",whereclause)
        arcpy.CalculateField_management("FixInfinity_lyr", "Radius", "0", "PYTHON", "")
        arcpy.Delete_management("FixInfinity_lyr")

        print ("FixRadius Done: " + c)
        logfile.write ('\n' + "FixRadius done: "+ c)
        
    # Update Source - put old source data into source
    
        UpdateSource(SimpClass)
        print ("UpdateSource Done: " + c)
        logfile.write ('\n' + "UpdateSource done: "+ c)
        
    # Fix Type 
        whereclause = "SourceType IS NOT NULL"
        arcpy.MakeFeatureLayer_management(SimpClass, "FixSourceType_lyr",whereclause)
        arcpy.CalculateField_management("FixSourceType_lyr", "SourceType", "!SourceType!.lower()", "PYTHON", "")    
        arcpy.CalculateField_management("FixSourceType_lyr", "SourceType", "!SourceType!.capitalize()", "PYTHON", "")      
        arcpy.Delete_management("FixSourceType_lyr")

        print ("FixSourceType Done: " + c)
        logfile.write ('\n' + "FixSourceType done: "+ c)
        
     # Added the simplify Arc Stuff at a .1 foot tolerance
     
        arcpy.SimplifyByStraightLinesAndCircularArcs_edit(SimpClass, ".1 feet")   
        ImportCogoLines (SimpClass,OutClass,TempClass)
        arcpy.Delete_management(SimpClass)
        arcpy.Delete_management(TempClass)
        
        print ("Class Done: " + c)
        logfile.write ('\n' + "Class done: "+ c)


#   finish up

    endtime =  datetime.datetime.now()
    timepassed = endtime - starttime 
    
    print ("Run Time: " + str(timepassed))
    print ( "Start-End Time: " + str(starttime) + "---" + str(endtime))
    logfile.write ('\n' + '\n' + "ImportCoto Succesful" + '\n' + '\n' )
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

