

# Import system modules
import arcpy
arcpy.env.overwriteOutput = True



# Set local variables
InLocation = arcpy.GetParameterAsText(0)
OutLocation = arcpy.GetParameterAsText(1)
in_table_river = arcpy.GetParameterAsText(2)
river = "!RiverCode!"
reach = "!ReachCode!"
FN_river =  "DWAY_NAME"
FT_river = "TEXT"
FL_river = 100
sep = '"-"'
FC_river = river + sep + reach
outFC_river = "Stream_Centerline"
in_table_XS = arcpy.GetParameterAsText(3)
FN1_XS = "WSEL"
FT1_XS = "DOUBLE"
FS1_XS = 2
WSEL_100YR = arcpy.GetParameterAsText(4)
FN2_XS = "DWAY_NAME"
FT2_XS = "TEXT"
FL2_XS = 100
FC2_XS = river + sep + reach
FN3_XS = "XSEC_ID"
FT3_XS = "LONG"
FS3_XS = 0
FC3_XS = "!ProfileM!"
FC4_XS = "round(float(!WSEL!),2)"
outRiverTarget = arcpy.GetParameterAsText(5)
outXSTarget = arcpy.GetParameterAsText(6)

#Add DWAY_NAME field to River2D
arcpy.AddField_management(in_table_river, FN_river, FT_river,"","",FL_river,"","","","")

#Add WSEL field to XS Cut Lines
arcpy.AddField_management(in_table_XS,FN1_XS,FT1_XS,"",FS1_XS,"","","","","")

#Add DWAY_NAME field to XS Cut Lines
arcpy.AddField_management(in_table_XS,FN2_XS,FT2_XS,"","",FL2_XS,"","","","")

#Add XSEC_ID field to XS Cut Lines
arcpy.AddField_management(in_table_XS,FN3_XS,FT3_XS,"",FS3_XS,"","","","","")

#FieldCalc DWAY_NAME on River2D off River + Reach
arcpy.management.CalculateField(in_table_river,FN_river,FC_river,"PYTHON_9.3")

#FieldCalc WSEL on XS Cut Lines from user specified field
arcpy.management.CalculateField(in_table_XS,FN1_XS,"!{0}!".format(WSEL_100YR),"PYTHON_9.3")

#FieldCalc DWAY NAME on XS Cut Lines from River + Reach
arcpy.management.CalculateField(in_table_XS,FN2_XS,FC2_XS,"PYTHON_9.3")

#FieldCalc XSEC_ID on XS Cut Lines form ProfileM
arcpy.management.CalculateField(in_table_XS,FN3_XS,FC3_XS,"PYTHON_9.3")

#Append River2D to Stream_Centerline in MHFD formatted .gdb
arcpy.Append_management(in_table_river,outRiverTarget,"NO_TEST","","")

#Append XS Cut Lines to Cross_Section in MHFD formatted .gdb
arcpy.Append_management(in_table_XS,outXSTarget,"NO_TEST","","")

#Round WSEL On MHFD XS file
arcpy.management.CalculateField(outXSTarget,"WSEL",FC4_XS,"PYTHON_9.3")
