#-------------------------------------------------------------------------------
# Name:        addCalcFirmPropOfTotalFirmMetric
#
# Purpose:     Add and calculate a field comprising firms' proportion of the
#              total firm metric for a market
#
# Author:      Matthew Sutton
#
# Created:     23/12/2018
#-------------------------------------------------------------------------------

import arcpy

#get and set the spatial join var
spatialJoin = arcpy.GetParameterAsText(0)

#delete new field if it already exists
if len(arcpy.ListFields(spatialJoin, "firmPropTotalFirmMetric")) > 0:
    arcpy.DeleteField_management(spatialJoin,["firmPropTotalFirmMetric"])

#add firms' proportion of total firm metric field to the spatial join
arcpy.AddField_management   (spatialJoin,
                            "firmPropTotalFirmMetric",
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