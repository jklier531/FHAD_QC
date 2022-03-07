#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Created By: John Klier
# Created On: 02/28/2022
# Last Updated: 02/28/2022
# This script was authored to assist in FHAD QC checks by generating points of intersect between a given floodplain delineation and 
# contour dataset to determine where a given contour line may intersect the delineation polygon in multiple locations. This version
# is meant for ArcPro.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Import system modules
import arcpy
import os

#set workspace to desired GDB from user input
arcpy.env.workspace= arcpy.GetParameterAsText(0)

#set variables
FP_delineation = arcpy.GetParameterAsText(1)
Contours = arcpy.GetParameterAsText(2)
Countour_table_name = os.path.basename(Contours).rstrip(os.path.splitext(Contours)[1])
inFeatures = [FP_delineation, Contours]
intersectOutput = "PT_FP_poly_Int_Contour_ln"
SPFC = "SP_PT_INT"
deDupeFieldIn = "FID_"+Countour_table_name
fieldOut = "Int_Count"
SPFC_lyr = "SPFC_lyr"
whereClause = '"Int_Count" >1'
deDupe_FC = "deDupe_PT_intersect"
delete_FC = [intersectOutput,SPFC]

#Run intersect geoprocessing tool and output points where contour intersects floodplain polygon
arcpy.Intersect_analysis(inFeatures, intersectOutput, "", "", "point")

#Run multipart to single part on intersectOutput
arcpy.MultipartToSinglepart_management(intersectOutput, SPFC)

#Add field to results from multipart to singlepart point feature class, and field calc duplicate count
arcpy.AddField_management(SPFC,fieldOut,"SHORT")

lista=[]
cursor1=arcpy.SearchCursor(SPFC)
for row in cursor1:
    i=row.getValue(deDupeFieldIn)    
    lista.append(i)
del cursor1, row

cursor2=arcpy.UpdateCursor(SPFC)
for row in cursor2:
    i=row.getValue(deDupeFieldIn)
    occ=lista.count(i)   
    row.setValue(fieldOut,occ)
    cursor2.updateRow(row)
del cursor2, row

#Select where DUPE_COUNT >1 within a temporary feature layer, and write those selected features to a new feature class.
arcpy.MakeFeatureLayer_management(SPFC,SPFC_lyr,whereClause)

arcpy.CopyFeatures_management(SPFC_lyr, deDupe_FC)

#Delete eronios feature classes
arcpy.Delete_management(delete_FC)

