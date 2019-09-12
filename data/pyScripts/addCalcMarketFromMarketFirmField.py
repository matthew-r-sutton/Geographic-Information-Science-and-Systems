#-------------------------------------------------------------------------------
# Name:        addCalcMarketFromMarketFirmField
#
# Purpose:     calculate market field from the market_firm field so that
#              sqFirmPropTotalMetric can be summed by market to generate the
#              HHI, before rejoining the table to the spatial join
#
# Author:      Matthew Sutton
#
# Created:     23/12/2018
#-------------------------------------------------------------------------------
import arcpy

#get and set square of firms' proportion of total firm metric table
sqFirmsPropOfTotalFirmMetricTable = arcpy.GetParameterAsText(0)

#get path from sqFirmsPropOfTotalFirmMetricTable and set it so that the table can be
#duplicated in the same geodatabase
sqFirmsPropOfTotalFirmMetricTablePath = [sqFirmsPropOfTotalFirmMetricTable]
wantedPathList = sqFirmsPropOfTotalFirmMetricTablePath[0].split('\\')
wantedPathList.pop(-1)
sqFirmsPropOfTotalFirmMetricTablePath = wantedPathList[0]
index = 1
while index < len(wantedPathList):
    sqFirmsPropOfTotalFirmMetricTablePath = sqFirmsPropOfTotalFirmMetricTablePath + "\\" + wantedPathList[index]
    index = index + 1

#set the split market_firm table name using sqFirmsPropOfTotalFirmMetricTablePath
splitMarketFirmTable = sqFirmsPropOfTotalFirmMetricTablePath + "\\splitMarketFirm"

#deletes splitMarketFirmTable if it exists
if arcpy.Exists(splitMarketFirmTable):
    arcpy.Delete_management(splitMarketFirmTable)

#create splitMarketFirm table from sqFirmsPropOfTotalFirmMetricTable
arcpy.TableToTable_conversion   (sqFirmsPropOfTotalFirmMetricTable,
                                sqFirmsPropOfTotalFirmMetricTablePath,
                                "splitMarketFirm")

#add empty market field
arcpy.AddField_management   (splitMarketFirmTable,
                            "market",
                            "TEXT")

#set calculation to split market from the market_firm field
marketCalculation = '!market_firm!.split("_")[0]'

#calculate the market field
arcpy.CalculateField_management (splitMarketFirmTable,
                                "market",
                                marketCalculation,
                                "PYTHON_9.3")

#create output node for model builder
arcpy.SetParameterAsText(1, splitMarketFirmTable)