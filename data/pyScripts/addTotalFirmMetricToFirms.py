#-------------------------------------------------------------------------------
# Name:        addTotalFirmMetricToFirms
#
# Purpose:     Add total firm metric from totalFirmMetric table to the firms FC
#
# Author:      Matthew Sutton
#
# Created:     23/12/2018
#-------------------------------------------------------------------------------

import arcpy

#get and set the spatial join var
firms = arcpy.GetParameterAsText(0)
totalFirmMetricTable = arcpy.GetParameterAsText(1)

#delete new field if it already exists
if len(arcpy.ListFields(firms, "totalFirmMetric")) > 0:
    arcpy.DeleteField_management(firms,["totalFirmMetric"])

#add totalFirmMetric to firms
arcpy.AddField_management   (firms,
                            "totalFirmMetric",
                            "FLOAT",
                            15,
                            14)

#set firms' proportion of total firm metric calculation
calculateProportion = '!firmMetric! / !totalFirmMetric!'

#calculate firms' proportion of total firm metric for a market
arcpy.CalculateField_management (spatialJoin,
                                "firmPropTotalFirmMetric",
                                calculateProportion,
                                "PYTHON_9.3")

#create output node for model builder
arcpy.SetParameterAsText(1, spatialJoin)