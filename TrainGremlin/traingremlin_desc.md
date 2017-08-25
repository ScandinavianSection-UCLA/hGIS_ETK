## **<u>“TrainGremlin”</u>**

**TrainGremlin** is an hGIS tool that can be used in ArcMap to assign means of transportation to undefined route segments. Read about its use it in context and with more detailed description (_6.1.1 Train)_ in the “Methods” document. This is an introduction.

*   Tool description: This script takes a route ("Route Segments") and a point ("Train Stations") shapefile and check for the number of intersections. The output shapefile (RouteSegments StationAdd) contains all route segment records and attributes that the input route segment shapefile does, but has a field called "COUNT_Abs_" that indicates the number of train stations the individual route segments intersects. The stations have been confirmed opened at the time of travel on the route segment. The “COUNT_Abs_” field can be used to assign the values ≥2 "Train assigned by model" (or similar) in the transportation field.

Fields necessary in the route shapefile:

Transportation - "trans_upda"

Year of travel on the route segment - "Year"

Order of the route segments - "Abs_seq"

Fields necessary in the station shapefile:

Opening year of station - "Year"

Name of the python script used to run the code: “TrainGremlin”.

*   Steps:
*   Create a copy of the input route shapefile.
*   Create a subset of the original route segment layer only containing only route segments that lack transportation data.
*   Create a 2km buffer around the train station layer.
*   “Spatial join” between the route and station shapefiles.
*   Establish that only stations that were open at the time counts for intersecting with the route segments.
*   Join the field with the count of intersecting train stations to a copy of the original route segment shapefile. Get a new final output shapefile with the intersection count.

*Additional data is available in this subdirectory