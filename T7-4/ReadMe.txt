Update 2.03 
Dean - 6/4/2022

1. Updated Annotation tasks. Added filters so that taxlots and taxlot_lines that were retired by record were not selected for calculating the correct underlying values. 
2. Created a new tool - UpdateORMAPArea that updates the taxlotfeet,taxlotacres, and mapacres fields for selected taxlots 
3. see #2 in the 2.02 update 
4. Update Mapindex feature class for county (it was empty before) it is now #27. 


Updates 2.02 
Dean - 4/16/2022 

1. Removed scripts that are not needed 
2. Taxlot Attribute Rules - fixed in the backup geodatabase (TownEdbk.gdb) - These were corrected earlier but if you replace the TownEd.gdb with the backup the rules will be bad again.  This has been fixed 
3. UpdateMapIndex - The Update MapIndex tool has been updated.  The MapScale now gets updated correctly in but the validate session and in the python script. In addition, the updatecursor in the update mapindex has been replaced with a search cursor.  


Updates 2.01 
Dean - 2/14/22

1. Attribute Domains - LineTypes - On Split set them to "Duplicate" rather then "Default" 
2. CalcMapTaxlot Taxlot Rule - Corrected error when taxlot was 3 charaters long had an extra "+" 
3. CalcCounty Taxlot Rule - Corrected error. Used MapNumber instead of county in one statement. 
4. ZoomTool Fix - When using SDE has a problem with null taxlots (fix sent from John) 
