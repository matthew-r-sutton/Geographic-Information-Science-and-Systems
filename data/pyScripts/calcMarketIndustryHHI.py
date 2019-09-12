#-------------------------------------------------------------------------------
# Name:        calcMarketIndustryHHI
#
# Purpose:     calculate industry HHI for a market
#
#              Use markets joined to firms to sum firm metric by firm, by
#              market-firm metric;
#              Use markets joined to firms to sum firm metric by market-
#              market industry metic;
#              Join market industry metric to the table resulting from the sum
#              of firm metric by firm, by market;
#              Calculate the proportion of firm metric to market industry
#              metric - Zj;
#              Calculate the square of Zj;
#              Sum Zj squared, by market - market industry HHI;
#              Join market industry HHI to submarkets to markets spatial join;
#
# Author:      Matthew Sutton
#
# Created:     29/12/2018
#-------------------------------------------------------------------------------
import arcpy

#get and set marketsJoinedToFirms, markets, and submarkets
marketsJoinedToFirms = arcpy.GetParameterAsText(0)
submarketsToMarketsJoin = arcpy.GetParameterAsText(1)
###############################################################################
###############################################################################
###############################################################################
#Use markets joined to firms to sum firm metic by firm by market-firm
#metic;
#get path from marketsJoinedToFirms and create output table path in its
#geodatabase
marketsJoinedToFirmsPath = [marketsJoinedToFirms]
wantedPathList = marketsJoinedToFirmsPath[0].split('\\')
wantedPathList.pop(-1)
path = wantedPathList[0]
index = 1
while index < len(wantedPathList):
    path = path + "\\" + wantedPathList[index]
    index = index + 1
sumFirmMetricByFirmByMarketPath = str(path) + "\\sumFirmMetricByFirmByMarket"

#delete sumFirmMetricByFirmByMarket table if it already exists
if arcpy.Exists(sumFirmMetricByFirmByMarketPath):
    arcpy.Delete_management(sumFirmMetricByFirmByMarketPath)

#sum firms' metric by firm by market
arcpy.Statistics_analysis   (marketsJoinedToFirms,
                            sumFirmMetricByFirmByMarketPath,
                            [["firmMetric", "SUM"]],
                            ["firm","market"])

#rename summed metric field
arcpy.AlterField_management (sumFirmMetricByFirmByMarketPath,
                            "SUM_firmMetric",
                            "firmMetricByFirmByMarket",
                            "firmMetricByFirmByMarket")
###############################################################################
###############################################################################
###############################################################################
#Use markets joined to firms to sum firm metric by market - market industry
#metric;
#set table name
sumFirmMetricByMarketPath = str(path) + "\\sumFirmMetricByMarket"

#delete sumFirmMetricByMarket table if it already exists
if arcpy.Exists(sumFirmMetricByMarketPath):
    arcpy.Delete_management(sumFirmMetricByMarketPath)

#sum firms' metric by market
arcpy.Statistics_analysis   (marketsJoinedToFirms,
                            sumFirmMetricByMarketPath,
                            [["firmMetric", "SUM"]],
                            ["market"])

#rename summed metric field
arcpy.AlterField_management (sumFirmMetricByMarketPath,
                            "SUM_firmMetric",
                            "firmMetricByMarket",
                            "firmMetricByMarket")
###############################################################################
###############################################################################
###############################################################################
#Join market industry metric to firmMetricByFirmByMarket table by market

#delete firmMetricByFirmByMarket field if it exists in marketsJoinedToFirms
if len(arcpy.ListFields(sumFirmMetricByFirmByMarketPath, "firmMetricByMarket")) > 0:
    arcpy.DeleteField_management(sumFirmMetricByFirmByMarketPath,["firmMetricByMarket"])


#join the firmMetricByMarket to sumFirmMetricByFirmByMarket table by market
arcpy.JoinField_management  (sumFirmMetricByFirmByMarketPath,
                            "market",
                            sumFirmMetricByMarketPath,
                            "market",
                            ["firmMetricByMarket"])
###############################################################################
###############################################################################
###############################################################################
#Calculate the proportion of firm metric to market industry metric - Zj;
#add Zj field to sumFirmMetricByFirmByMarket table
arcpy.AddField_management   (sumFirmMetricByFirmByMarketPath,
                            "Zj",
                            "FLOAT",
                            15,
                            14)

#set to calculate proportion of firm metric to total market industry metric
calculateProp = "!firmMetricByFirmByMarket!/!firmMetricByMarket!"

#calculate Zj
arcpy.CalculateField_management (sumFirmMetricByFirmByMarketPath,
                                "Zj",
                                calculateProp,
                                "PYTHON_9.3")
###############################################################################
###############################################################################
###############################################################################
#Calculate the square of Zj;
#add ZjSquared field to sumFirmMetricByFirmByMarket table
arcpy.AddField_management   (sumFirmMetricByFirmByMarketPath,
                            "ZjSquared",
                            "FLOAT",
                            15,
                            14)

#set to calculate square of Zj
calculateSquare = "!Zj!*!Zj!"

#calculate square of Zj
arcpy.CalculateField_management (sumFirmMetricByFirmByMarketPath,
                                "ZjSquared",
                                calculateSquare,
                                "PYTHON_9.3")
###############################################################################
###############################################################################
###############################################################################
#Sum Zj squared, by market - market industry HHI;
#set table name
marketIndustryHHIPath = str(path) + "\\marketIndustryHHI"

#delete marketIndustryHHI table if it already exists
if arcpy.Exists(marketIndustryHHIPath):
    arcpy.Delete_management(marketIndustryHHIPath)

#sum firms' metric by market
arcpy.Statistics_analysis   (sumFirmMetricByFirmByMarketPath,
                            marketIndustryHHIPath,
                            [["ZjSquared", "SUM"]],
                            ["market"])

#rename summed metric field
arcpy.AlterField_management (marketIndustryHHIPath,
                            "SUM_ZjSquared",
                            "marketIndustryHHI",
                            "marketIndustryHHI")
###############################################################################
###############################################################################
###############################################################################
#Join market industry HHI to submarkets to markets spatial join;
#delete firmMetricByFirmByMarket field if it exists in marketsJoinedToFirms
if len(arcpy.ListFields(submarketsToMarketsJoin, "marketIndustryHHI")) > 0:
    arcpy.DeleteField_management(submarketsToMarketsJoin,["marketIndustryHHI"])


#join marketIndustryHHI to submarketsToMarketsJoin by market
arcpy.JoinField_management  (submarketsToMarketsJoin,
                            "market",
                            marketIndustryHHIPath,
                            "market",
                            ["marketIndustryHHI"])

arcpy.SetParameterAsText(2,submarketsToMarketsJoin)

