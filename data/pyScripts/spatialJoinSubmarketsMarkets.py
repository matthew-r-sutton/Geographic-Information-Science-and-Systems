#-------------------------------------------------------------------------------
# Name:        spatialJoinSubmarketsMarkets
#
# Purpose:     spatially join submarkets to markets
#
# Author:      Matthew Sutton
#
# Created:     22/12/2018
#-------------------------------------------------------------------------------

import arcpy

#get and set submarkets and markets
markets = arcpy.GetParameterAsText(0)
submarkets = arcpy.GetParameterAsText(1)

#get path from markets FC and use it as the spatial join's path
marketsPath = [markets]
wantedPathList = marketsPath[0].split('\\')
wantedPathList.pop(-1)
path = wantedPathList[0]
index = 1
while index < len(wantedPathList):
    path = path + "\\" + wantedPathList[index]
    index = index + 1
spatialJoinPath = str(path) + "\\submarketsJoinedToMarkets"

#delete spatial join if it already exists
if arcpy.Exists(spatialJoinPath):
    arcpy.Delete_management(spatialJoinPath)

#spatially join submarkets to markets
arcpy.SpatialJoin_analysis  (markets,
                            submarkets,
                            spatialJoinPath,
                            "JOIN_ONE_TO_MANY",
                            "KEEP_COMMON",
                            "#",
                            "CONTAINS_CLEMENTINI")

#create output node for model builder
arcpy.SetParameterAsText(2, spatialJoinPath)