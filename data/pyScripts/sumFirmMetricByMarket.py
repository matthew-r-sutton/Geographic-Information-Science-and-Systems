#-------------------------------------------------------------------------------
# Name:        sumFirmMetricByMarket
#
# Purpose:     calculate the sum of firms' metric for each market
#
# Author:      Matthew Sutton
#
# Created:     22/12/2018
#-------------------------------------------------------------------------------
import arcpy

#get and set spatial join
spatialJoin = arcpy.GetParameterAsText(0)

#get path from markets joined to firms FC and create output table path in its
#geodatabase
spatialJoinPath = [spatialJoin]
wantedPathList = spatialJoinPath[0].split('\\')
wantedPathList.pop(-1)
path = wantedPathList[0]
index = 1
while index < len(wantedPathList):
    path = path + "\\" + wantedPathList[index]
    index = index + 1
totalFirmMetricMarketPath = str(path) + "\\totalFirmMetricMarket"

#delete totalFirmMetricMarket table if it already exists
if arcpy.Exists(totalFirmMetricMarketPath):
    arcpy.Delete_management(totalFirmMetricMarketPath)

#calculate sum of firms' metric by market
arcpy.Statistics_analysis   (spatialJoin,
                            totalFirmMetricMarketPath,
                            [["firmMetric", "SUM"]],
                            ["market"])

#rename summed metric field
arcpy.AlterField_management (totalFirmMetricMarketPath,
                            "SUM_firmMetric",
                            "totalFirmMetric",
                            "totalFirmMetric")

#create output node for model builder
arcpy.SetParameterAsText(1,totalFirmMetricMarketPath)