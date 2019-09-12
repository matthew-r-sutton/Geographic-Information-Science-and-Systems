#-------------------------------------------------------------------------------
# Name:        joinFirmMetricHHIForMarketWithInputMarketFC
#
# Purpose:     join the firm metric HHI for markets to the input market FC
#              and the markets-firms spatial join
#
# Author:      Matthew Sutton
#
# Created:     23/12/2018
#-------------------------------------------------------------------------------

import arcpy

#get and set input markets FC, the markets field from the markets FC,
#the metric from the firms FC, the markets-firms spatial join,
#and the table with the HHI field
markets = arcpy.GetParameterAsText(0)
marketsField = arcpy.GetParameterAsText(1)
firmMetricField = arcpy.GetParameterAsText(2)
spatialJoin = arcpy.GetParameterAsText(3)
HHITable = arcpy.GetParameterAsText(4)

#set output HHI_(firm metric) field for joining to markets FC
outputHHIField = "HHI_" + firmMetricField

#delete HHI field if it already exists within the input markets FC
if len(arcpy.ListFields(markets, outputHHIField)) > 0:
    arcpy.DeleteField_management(markets,[outputHHIField])

#add HHI field from HHITable to the input markets feature class
arcpy.JoinField_management  (markets,
                            marketsField,
                            HHITable,
                            "market",
                            ["HHI"])

#rename HHI field to HHI_(firm metric)
arcpy.AlterField_management (markets,
                            "HHI",
                            outputHHIField,
                            outputHHIField)

#add HHI field from HHITable to the markets-firms spatial join
arcpy.JoinField_management  (spatialJoin,
                            "market",
                            HHITable,
                            "market",
                            ["HHI"])

#rename HHI field to HHI_(firm metric)
arcpy.AlterField_management (spatialJoin,
                            "HHI",
                            outputHHIField,
                            outputHHIField)

#create ouput node for model builder
arcpy.SetParameterAsText(5, markets)
arcpy.SetParameterAsText(6, spatialJoin)