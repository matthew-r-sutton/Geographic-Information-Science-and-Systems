#-------------------------------------------------------------------------------
# Name:        sumSqFirmsPropsOfTotalFirmMetricByMarketForHHI
#
# Purpose:     sum the square of firms' proportion of total market metric by
#              market to calculate markets' HHIs
#
# Author:      Matthew Sutton
#
# Created:     23/12/2018
#-------------------------------------------------------------------------------
import arcpy

#get and set squared firms' proportion of total firm metric table
sqFirmsPropOfTotalFirmMetricTable = arcpy.GetParameterAsText(0)

#get path from squared firms' proportion of total firm metric table and create
#HHI table path in its geodatabase
sqFirmsPropOfTotalFirmMetricTablePath = [sqFirmsPropOfTotalFirmMetricTable]
wantedPathList = sqFirmsPropOfTotalFirmMetricTablePath[0].split('\\')
wantedPathList.pop(-1)
sqFirmsPropOfTotalFirmMetricTablePath = wantedPathList[0]
index = 1
while index < len(wantedPathList):
    sqFirmsPropOfTotalFirmMetricTablePath = sqFirmsPropOfTotalFirmMetricTablePath + "\\" + wantedPathList[index]
    index = index + 1
HHITableOutput = str(sqFirmsPropOfTotalFirmMetricTablePath) + "\\HHITable"

#delete table if it already exists
if arcpy.Exists(HHITableOutput):
    arcpy.Delete_management(HHITableOutput)

#create HHITable from sqFirmsPropOfTotalFirmMetricTable
arcpy.TableToTable_conversion   (sqFirmsPropOfTotalFirmMetricTable,
                                sqFirmsPropOfTotalFirmMetricTablePath,
                                "HHITable")

#add empty HHI field
arcpy.AddField_management   (HHITableOutput,
                            "HHI",
                            "FLOAT",
                            5,
                            4)

#calculate sum of sqFirmPropTotalMetric by market to create HHI
arcpy.Statistics_analysis   (sqFirmsPropOfTotalFirmMetricTable,
                            HHITableOutput,
                            [["sqFirmPropTotalMetric", "SUM"]],
                            ["market"])

#rename summed sqFirmPropTotalMetric field to HHI
arcpy.AlterField_management (HHITableOutput,
                            "SUM_sqFirmPropTotalMetric",
                            "HHI",
                            "HHI")

#create output node for model builder
arcpy.SetParameterAsText(1, HHITableOutput)