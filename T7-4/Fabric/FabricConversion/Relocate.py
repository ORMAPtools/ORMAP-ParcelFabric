arcpy 
import arcpy
aprx = arcpy.mp.ArcGISProject(r'P:\GISPROJECTS\ASSESSOR\NewCartography\StateView1\OrMapPF.aprx')

aprx.updateConnectionProperties(r'P:\GISPROJECTS\ASSESSOR\NewCartography\StateView1\TownEd.gdb',
                                r'P:\AIGIS\libraries\taxmap\County\Fabric\TownEd.gdb')

aprx.saveACopy(r'P:\GISPROJECTS\ASSESSOR\NewCartography\StateView1\OrMapPF2.aprx')