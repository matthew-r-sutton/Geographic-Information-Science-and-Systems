#-------------------------------------------------------------------------------
# Name:        joinTotalFirmMetricWithSpatialJoin
#
# Purpose:     Join the total firm metric by market table to the
#              spatial join of markets to firms FC by the
#              market field.
#
# Author:      Matthew Sutton
#
# Created:     21/12/2018
#-------------------------------------------------------------------------------

import arcpy

#get and set spatial join and total firm metric by market table
spatialJoin = arcpy.GetParameterAsText(0)
totalFirmMetricTable = arcpy.GetParameterAsText(1)

#delete total firm metric field if it exists
if len(arcpy.ListFields(spatialJoin, "totalFirmMetric")) > 0:
    arcpy.DeleteField_management(spatialJoin,["totalFirmMetric"])

#join the total firm metric by market table to spatial join by market
arcpy.JoinField_management  (spatialJoin,
                            "market",
                            totalFirmMetricTable,
                            "market",
                            ["totalFirmMetric"])

#create output node for model builder
arcpy.SetParameterAsText(2, spatialJoin)