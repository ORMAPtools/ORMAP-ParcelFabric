# ORMAP Parcel Fabric project

ReadMe - Version 1.07

## Changes in 1.07

Looks like the APRX file (OrMapPF.aprx) changed 
and the meeting notes have been updated to include June 16. (Documents/MeetingNotes.docx).

There were some changes in the template GDB and it was not included in the 1.06
version. It has been added, for now anyway. (OrMapPFTemplate.gdb)

## Changes to the design for 1.06 

addition of two fields - CreateByRecord and CurrentFeature (anno/line/polygon) 

This is the sixth draft version of the ORMAP ArcPro data structure that includes Parcel Fabric 2.6.  This directory is an ArcPro workspace. 

## Manifest

AttributeRuleSamples - Contains samples of attribute rules from users. (Missing?)

CountySamples - where stuff from participating counties will go (has attribute rules from Multnomah) 

Default.gdb - Started ESRI Database 

Documents - Design Documents (Original Design from 2006 and the New Draft Design) 

ImportLog - Standard ESRI Log 

Index - Standard ESRI Index subdirectory 

ORMAPPFTemplate.gdb - The new database template (includes empty feature classes, fields, and domains) 

Default.tbx - default tool box 

OrMapPF.aprx - ESRI ArcGIS Pro project file 


----
These two are things that were in the Esri Sharepoint folder. They might not stay here.

LabelToAnnoTest - 2/22/21 Dean says "I have completed my tests for converting bearing/distance labels to annotation for a variety of scales and styles.  It all seems to work OK.   

I have placed a ZIP file on the ORMAPTools site "LabelToAnnoTest.zip". It contains a word document that describes the process, the toolbox containing the tool and a python script that does the conversion.  These will not work unless you go through the process of creating  labelclasses for taxlot_lines (what they look like is described in the word document. 

This work was done on my prototype machine which is running 2.7.  It should work fine in 2.6. 

I will include this in the next design version to be sent out in a couple of weeks.  I will make sure it all runs smoothly in the 2.6 release.  I will also be fixing attribute rules so they work in the 2.6 environment. 

Glad the new label and annotation tools work well."


TownEdScripts - 

## To Set This Up

1. Have ArcPro installed 2.6 or greater on recommended machine
2. Must have a working knowledge of ArcPro (Editing, Map Layouts, Feature Class Design, Catalog) 
3. Have a working knowlege of Arcade 
4. Have a working knowledge of Parcel Fabric (Take the ESRI ArcPro class) 

 
