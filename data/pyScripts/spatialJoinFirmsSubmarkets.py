#-------------------------------------------------------------------------------
# Name:        spatialJoinSubmarketsFirms
#
# Purpose:     spatially join firms to submarkets, using 1-to-many, interect
#
# Author:      Matthew Sutton
#
# Created:     30/12/2018
#-------------------------------------------------------------------------------

import arcpy

#get and set markets and firms FCs
firms = arcpy.GetParameterAsText(0)
submarkets = arcpy.GetParameterAsText(1)

#get path from submarkets and use it as the spatial join's path
submarketsPath = [submarkets]
wantedPathList = submarketsPath[0].split('\\')
wantedPathList.pop(-1)
path = wantedPathList[0]
index = 1
while index < len(wantedPathList):
    path = path + "\\" + wantedPathList[index]
    index = index + 1
spatialJoinPath = str(path) + "\\firmsJoinedToSubmarkets"

#delete spatial join if it already exists
if arcpy.Exists(spatialJoinPath):
    arcpy.Delete_management(spatialJoinPath)

#spatially join markets to firms
arcpy.SpatialJoin_analysis  (submarkets,
                            firms,
                            spatialJoinPath,
                            "JOIN_ONE_TO_MANY",
                            "KEEP_COMMON",
                            "#",
                            "INTERSECT")

#create output node for model builder
arcpy.SetParameterAsText(2, spatialJoinPath)