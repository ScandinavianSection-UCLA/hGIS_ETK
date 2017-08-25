# -*- coding: utf-8 -*-
"""
TrainGremlin Dynamic to be used to generate a script in ArcMap

"""
import arcpy

#setting up the folder where I keep my digitized polygon. 
#change to raw input
arcpy.env.workspace = arcpy.GetParameterAsText(0) 


#if the file name already exists, over write it.
arcpy.env.overwriteOutput = True

#input shapefile, trans_update with empty fields. 
#change to raw input
in_routeSegment = arcpy.GetParameterAsText(1) 

#the one we want to create. Will be deleted = no raw input necessary.
out_train_segments = "trainRouteSegments4.shp" 

#in station layer
#no copy neeede - buffer will be new shapefile and this one will not be altered
#cange to raw input
in_stations = arcpy.GetParameterAsText(2)

#make a copy, looks like original, named trainRouteSegments.shp  
arcpy.Copy_management(in_routeSegment, out_train_segments)

#the following steps are part in using "selct by attribute. This can not be done
#directly on the feature class, rather it must me made a "layer" and finally 
#copied to a new shapefile.
arcpy.MakeFeatureLayer_management(out_train_segments, "lyr") 
#select all the route segment that does not have any value in the field trans_update
#note that this is not going to be made dynamic in the tool. If performed on 
#other data, its tranportation field needs to be called "trans_upda" or update
#this script.

arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", " \"trans_upda\" = '' ")
arcpy.CopyFeatures_management("lyr", "only_TransMissing.shp")

#create a buffere around the stations. 2km.
arcpy.Buffer_analysis(in_stations, "station_buffer.shp", "2000 meters")

#Spatial join - stations that intersect with the route segments are joined to
#the route segment. Each station intersection, after the first, will add a new
#record. Route segments with one intersecting train station has one records and
#the same goes for stations with one intersecting train station. The difference
#is the join count (0 for no intersection and 1 for intersection). The main
#importance is that two records for one route segment means that two stations 
#intersect it: hence should be assign train as means of transportation. 
arcpy.SpatialJoin_analysis("only_TransMissing.shp", "station_buffer.shp", "join_route_to_station3.shp", "JOIN_ONE_TO_MANY")

#make a selection of the output of the spatial join: only select route segments
#(records) where the travel on the segment happened after the intersecrting 
#train station opened. Again, select by attribute requires a layer as opposed to
#a feature class. Once selection: copied back into a new feature class. 
arcpy.MakeFeatureLayer_management("join_route_to_station3.shp", "lyr") 
arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", " \"Year\" > \"Year_1\" ")
arcpy.CopyFeatures_management("lyr", "only_travel_when_open.shp")

#"Abs_seq" is unique for each route segment. Since each route segment has been
#copied once for each train station it intersects along with the abs_seq field 
#and all other attribute fields, counting the number of times a route segments 
#abs_seq value appears counts the number of train intersections. 
#the output will be the table (.dbf) with one field for each abs seq value along
#with a count field called "COUNT_Abs_"
arcpy.Statistics_analysis("only_travel_when_open.shp", "count_intersections7.dbf" ,[["Abs_seq", "COUNT"],["Name", "MIN"]], "Abs_seq")

arcpy.Copy_management("count_intersections7.dbf", "count_table_extra3.dbf")

#make a copy of the original route shapefile, for the intersection data to be 
#joined back to. 
#change to raw input,

final_output = arcpy.GetParameterAsText(3)
arcpy.Copy_management(in_routeSegment, final_output)

#join intersection data to the final route segment with intersections output.
#the only field we are interested in to join is "COUNT_Abs_"
arcpy.JoinField_management(final_output, "Abs_seq", "count_table_extra3.dbf", "Abs_seq", "COUNT_Abs_")


#delete unneccesary tables and shapefiles
arcpy.Delete_management(arcpy.env.workspace + '/' + "only_travel_when_open.shp")

arcpy.Delete_management(arcpy.env.workspace + '/' + "count_table_extra3.dbf")

arcpy.Delete_management(arcpy.env.workspace + '/' + "join_route_to_station3.shp")

arcpy.Delete_management(arcpy.env.workspace + '/' + "only_TransMissing.shp")

arcpy.Delete_management(arcpy.env.workspace + '/' + "count_intersections7.dbf")

arcpy.Delete_management(arcpy.env.workspace + '/' + "station_buffer.shp")

arcpy.Delete_management(arcpy.env.workspace + '/' + "trainRouteSegments4.shp" )


print 'done'
