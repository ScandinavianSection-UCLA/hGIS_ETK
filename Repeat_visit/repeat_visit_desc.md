## **Point Layer to Revisited Point Layer**

**RevisitCount** is an hGIS tool that aggregates points in the same location into a single point and gives it a count attribute value.

<span style="text-decoration: underline;">**Tool description:**</span>  
This script takes a point layer with multiple points at the same location as input feature class. The output point layer gets only one point for every unique location, with an attribute named "FREQUENCY" that indicates how many times the specific location occurred in the original point layer. There are some nice visualization options such as giving the points proportionate size to how many times they have been visited. In addition to the output point layer, there is an output Excel table that shows the data in a list with places and corresponding number of visits.”

<span style="text-decoration: underline;">**Name of python script used to run the tool:**</span>  
“RevisitCount”

**Steps:**  
o Create a copy of the input shapefile.  
o Add X and Y points to the new shapefile’s attribute table.  
o Add an empty field.  
o Populate the empty field with a combined value of the data in the X and the Y field (one unique value for each location).  
o A .dbf file is generated based on running a summary on the combined XY-field. It looks like a table where each record is a unique place. The number of points that has been “summarized” into one record is accounted for in a field called “FREQUENCY”. The name of the place is also an attribute, as well as the X and Y location in separate fields.  
o The .dbf file is imported back into ArcMap using the X and Y coordinates to create one points for each individual record. It creates an “Event Layer” that needs to be copied to become a feature class which is the final output.  
o An Excel table that looks like the attribute table of the generated “revisit point layer” is exported by the tool.  
o All data generated in the steps leading up to the final output, as well as unnecessary attributes, is deleted by the tool leaving the user with only the revisit point layer and the Excel table with a user specified name in the user specified workspace.

Additional test data is available in this subdirectory.