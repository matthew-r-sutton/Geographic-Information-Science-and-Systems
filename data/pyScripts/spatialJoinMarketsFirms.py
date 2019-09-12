#-------------------------------------------------------------------------------
# Name:        spatialJoinSubmarketsFirms
#
# Purpose:     spatially join markets FC to firms FC
#
# Author:      Matthew Sutton
#
# Created:     22/12/2018
#-------------------------------------------------------------------------------

import arcpy

#get and set markets and firms FCs
firms = arcpy.GetParameterAsText(0)
markets = arcpy.GetParameterAsText(1)

#get path from markets FC and use it as the spatial join's path
marketsPath = [markets]
wantedPathList = marketsPath[0].split('\\')
wantedPathList.pop(-1)
path = wantedPathList[0]
index = 1
while index < len(wantedPathList):
    path = path + "\\" + wantedPathList[index]
    index = index + 1
spatialJoinPath = str(path) + "\\marketsJoinedToFirms"

#delete spatial join if it already exists
if arcpy.Exists(spatialJoinPath):
    arcpy.Delete_management(spatialJoinPath)

#spatially join markets to firms
arcpy.SpatialJoin_analysis  (firms,
                            markets,
                            spatialJoinPath,
                            "JOIN_ONE_TO_MANY",
                            "KEEP_COMMON",
                            "#",
                            "INTERSECT")

#create output node for model builder
arcpy.SetParameterAsText(2, spatialJoinPath)