T7-4 - ORMAP ArcPro Conversion - Version 1.06 

This is a sample conversion dataset for One township in Polk County. It operates with ArcPro 2.6 (you could use 2.7 but the table for map production does not work correctly due an ESRI bug (which is being fixed).  The update contains: 

Clean Up of Tools and addition of two fields - CreateByRecord and CurrentFeature (anno/line/polygon) 


Geodb - Contains an township geodatabase that meets the ORMAP ArcMap standard (or is close) and an MXD (mapreview_v106.mxd) to look at it. 

Fabric - Contains a converted township (Polk County t7-4) in the new structure.  ONLY the taxlot, taxlotline, and Points are in the new Parcel Fabric Structure. The Condo feature class is presend but contains no features. 

 (check Readme.Txt in this directory for more information. 


*** To See the Results Goto - fabric/OrMapPF.aprx
*** To Install So it works... 


I have done little to load/calculate attributes as that will come once I know the fabric works. 


- Dean May 2021 