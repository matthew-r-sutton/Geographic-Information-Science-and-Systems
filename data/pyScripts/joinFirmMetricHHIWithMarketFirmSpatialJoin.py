#-------------------------------------------------------------------------------
# Name:        joinFirmMetricHHIByMarketWithSpatialJoin
#
# Purpose:     join the firm metric HHI for markets to the markets-firms spatial
#              join
#
# Author:      Matthew Sutton
#
# Created:     23/12/2018
#-------------------------------------------------------------------------------

import arcpy

#get and set the table with the HHI field
HHITable = arcpy.GetParameterAsText(0)
###############################################################################
###############################################################################
###############################################################################
HHITablePath = [HHITable]
wantedPathList = HHITablePath[0].split('\\')
wantedPathList.pop(-1)
HHITablePath = wantedPathList[0]
index = 1
while index < len(wantedPathList):
    HHITablePath = HHITablePath + "\\" + wantedPathList[index]
    index = index + 1
spatialJoin = str(HHITablePath) + "\\marketsJoinedToFirms"

#delete HHI field if it already exists within the spatial join
if len(arcpy.ListFields(spatialJoin, "HHI")) > 0:
    arcpy.DeleteField_management(spatialJoin,["HHI"])


#add HHI field from HHITable to the markets-firms spatial join
arcpy.JoinField_management  (spatialJoin,
                            "market",
                            HHITable,
                            "market",
                            ["HHI"])
###############################################################################
###############################################################################
###############################################################################
#create ouput node for model builder
arcpy.SetParameterAsText(1, spatialJoin)