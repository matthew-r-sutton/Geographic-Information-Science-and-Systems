#-------------------------------------------------------------------------------
# Name:        addCalcSqOfFirmsPropOfTotalFirmMetric
#
# Purpose:     square firms' proportion of total firm metric if the are in the
#              same market and are the same firm
#
# Author:      Matthew Sutton
#
# Created:     23/12/2018
#-------------------------------------------------------------------------------
import arcpy

#get and set summed firms' proportion of total firm metric table
summedFirmsPropOfTotalFirmMetricTable = arcpy.GetParameterAsText(0)

#get path from summed firms' proportion of total firm metric table and set it so
#that the table can be duplicated in the same geodatabase
summedFirmsPropOfTotalFirmMetricTablePath = [summedFirmsPropOfTotalFirmMetricTable]
wantedPathList = summedFirmsPropOfTotalFirmMetricTablePath[0].split('\\')
wantedPathList.pop(-1)
summedFirmsPropOfTotalFirmMetricTablePath = wantedPathList[0]
index = 1
while index < len(wantedPathList):
    summedFirmsPropOfTotalFirmMetricTablePath = summedFirmsPropOfTotalFirmMetricTablePath + "\\" + wantedPathList[index]
    index = index + 1

#set square of firms' proportion of total firm metric table name using
#summedFirmsPropOfTotalFirmMetricTablePath
sqFirmsPropOfTotalFirmMetricTable = summedFirmsPropOfTotalFirmMetricTablePath + "\\sqFirmsPropOfTotalFirmMetric"

#deletes duplicate table if it exists
if arcpy.Exists(sqFirmsPropOfTotalFirmMetricTable):
    arcpy.Delete_management(sqFirmsPropOfTotalFirmMetricTable)

#create square of firms' proportion of total firm metric table from
#summedFirmsPropOfTotalFirmMetricTable
arcpy.TableToTable_conversion   (summedFirmsPropOfTotalFirmMetricTable,
                                summedFirmsPropOfTotalFirmMetricTablePath,
                                "sqFirmsPropOfTotalFirmMetric")

#add empty square of firms' proportion of total firm metric field
arcpy.AddField_management   (sqFirmsPropOfTotalFirmMetricTable,
                            "sqFirmPropTotalMetric",
                            "FLOAT",
                            15,
                            14)

#create calculation to square firms' proportion of total firm metric
sqFirmsPropOfTotalFirmMetricCalculation = '!firmPropTotalFirmMetric! * !firmPropTotalFirmMetric!'

#calculate sqFirmPropTotalMetric field
arcpy.CalculateField_management (sqFirmsPropOfTotalFirmMetricTable,
                                "sqFirmPropTotalMetric",
                                sqFirmsPropOfTotalFirmMetricCalculation,
                                "PYTHON_9.3")

#create output node for model builder
arcpy.SetParameterAsText(1, sqFirmsPropOfTotalFirmMetricTable)