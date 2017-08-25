# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 16:07:09 2017

@author: Owner
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 08:53:24 2017

Ida Storm

Depeloping tools that will take a point data set as input. The point dataset
will have a field for year/data as well as a field with names of the place.
The output will be a repeat visit map. Work for places with the same name in 
different locations. 

- add X and Y field to the attribute table
- add field in the attribute table
- use field calculator to add x and y in the new field. Unique number for location.
- summarize by the combined x/y field. 

Dynamic tool version:
"""

import arcpy

#setting up the folder where I keep my digitized polygon. 

#change to raw input
arcpy.env.workspace = arcpy.GetParameterAsText(0) 

#change to raw input

arcpy.env.overwriteOutput = True

in_point = arcpy.GetParameterAsText(1) 
out_points_revisits = "revisits.shp" 


#if arcpy.Exists(env.workspace + '/' + out_points_revisits):
 #   arcpy.Delete_management(env.workspace + '/' + out_points_revisits)
    
arcpy.Copy_management(in_point, out_points_revisits)

# Execute AddXY
arcpy.AddXY_management(out_points_revisits)


arcpy.AddField_management(out_points_revisits, "comb_XY", "FLOAT", 16, 4)


arcpy.CalculateField_management(out_points_revisits, "comb_XY" , "[POINT_X]+ [POINT_Y]", "VB")

#if arcpy.Exists(env.workspace + '/' + "revisits_stats.dbf"):
 #   arcpy.Delete_management(env.workspace + '/' + "revisits_stats.dbf")
#Name field - input from user.

#cannot delete. have to keep updating name. not same name twice = lock
output_stats_table = "stats_table2.dbf"

placeField_name = arcpy.GetParameterAsText(4) 

arcpy.Statistics_analysis(out_points_revisits, output_stats_table , [["comb_XY", "COUNT"], [placeField_name, "FIRST"],["POINT_X", "MIN"], ["POINT_Y", "MIN"], ["POINT_Y", "MIN"]], "comb_XY")


#get the spatial reference of input layer:

desc = arcpy.Describe(in_point)
sr = desc.spatialReference

event_layer = "unnecessary.lyr"

#if arcpy.Exists(arcpy.env.workspace + '/' + event_layer):
 #   arcpy.Delete_management(arcpy.env.workspace + '/' + event_layer)
    
arcpy.MakeXYEventLayer_management(output_stats_table, "MIN_POINT_", "MIN_POINT1", event_layer, sr)

layer_file = "unnecessary.lyr"
#if arcpy.Exists(arcpy.env.workspace + '/' + layer_file):
 #   arcpy.Delete_management(env.workspace + '/' + layer_file)
    
arcpy.SaveToLayerFile_management(event_layer, layer_file)

#also not same name twice, lock.
repeat_visits =  arcpy.GetParameterAsText(2)  #this is the output. 

#if arcpy.Exists(env.workspace + '/' + repeat_visits):
 #   arcpy.Delete_management(env.workspace + '/' + repeat_visits)

#"repeat visits" should be the only layer lef. as well as the dbf tables that are in a lock.
arcpy.CopyFeatures_management(event_layer, repeat_visits)

dropFields = ["COUNT_comb", "comb_XY", "MIN_POINT_", "MIN_POINT1", "MIN_POIN_1"]
arcpy.DeleteField_management(repeat_visits, dropFields)

excel_name = arcpy.GetParameterAsText(3)

arcpy.TableToExcel_conversion(repeat_visits, excel_name)

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "copy_inPoint"

#delete unncessesary_files:
arcpy.Delete_management(arcpy.env.workspace + '/' + layer_file)
arcpy.Delete_management(arcpy.env.workspace + '/' + output_stats_table)

arcpy.Delete_management(arcpy.env.workspace + '/' + out_points_revisits)
#print 'done'