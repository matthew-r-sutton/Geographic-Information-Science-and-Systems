#-------------------------------------------------------------------------------
# Name:        sumFirmsPropOfTotalFirmMetricByMarketFirmField
#
# Purpose:     sum firms' proportion of total firm metric if the are in the same
#              market and are the same firm
#
# Author:      Matthew Sutton
#
# Created:     23/12/2018
#-------------------------------------------------------------------------------
import arcpy

#get and set spatial join var
spatialJoin = arcpy.GetParameterAsText(0)

#get path from spatial join and create output table path in its geodatabase
spatialJoinPath = [spatialJoin]
wantedPathList = spatialJoinPath[0].split('\\')
wantedPathList.pop(-1)
path = wantedPathList[0]
index = 1
while index < len(wantedPathList):
    path = path + "\\" + wantedPathList[index]
    index = index + 1
sumFirmPropOfTotalFirmMetricOutput = str(path) + "\\sumFirmPropOfTotalFirmMetric"

#delete table if it already exists
if arcpy.Exists(sumFirmPropOfTotalFirmMetricOutput):
    arcpy.Delete_management(sumFirmPropOfTotalFirmMetricOutput)

#calculate sum of firms' proportion of total firm metric by market if they
#are the same firm
arcpy.Statistics_analysis   (spatialJoin,
                            sumFirmPropOfTotalFirmMetricOutput,
                            [["firmPropTotalFirmMetric", "SUM"]],
                            ["market_firm"])

#rename SUM_firmPropTotalFirmMetric field
arcpy.AlterField_management (sumFirmPropOfTotalFirmMetricOutput,
                            "SUM_firmPropTotalFirmMetric",
                            "firmPropTotalFirmMetric",
                            "firmPropTotalFirmMetric")

#create output node for model builder
arcpy.SetParameterAsText(1, sumFirmPropOfTotalFirmMetricOutput)