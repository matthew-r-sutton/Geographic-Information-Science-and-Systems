#-------------------------------------------------------------------------------
# Name:        calcXiAndSumOfXiSquaredByMarket
# Purpose:     Calculate Xi:
#
#              Calculate the proportion of total submarket metric to total
#              market metric - Xi;
#              Calculate the square of Xi - Xi squared;
#              Sum squared Xi by market;
#              Rejoin sum of square Xi's to spatial join of submarkets to
#              markets by market
#
# Author:      Matthew Sutton
#
# Created:     29/12/2018
#-------------------------------------------------------------------------------
import arcpy

#get and set submarketsJoinedToMarkets
submarketsJoinedToMarkets = arcpy.GetParameterAsText(0)
###############################################################################
###############################################################################
###############################################################################
#Use spatial join of submarkets to markets to sum submarkets' metric by market,
#producing total submarket metric;
#get path from submarketsJoinedToMarkets and create output table path in its
#geodatabase
submarketsJoinedToMarketsPath = [submarketsJoinedToMarkets]
wantedPathList = submarketsJoinedToMarketsPath[0].split('\\')
wantedPathList.pop(-1)
path = wantedPathList[0]
index = 1
while index < len(wantedPathList):
    path = path + "\\" + wantedPathList[index]
    index = index + 1
###############################################################################
###############################################################################
###############################################################################
#Calculate the proportion of submarket metric to market metric - Xi;
#delete Xi field if it exists in submarketsJoinedToMarkets
if len(arcpy.ListFields(submarketsJoinedToMarkets, "Xi")) > 0:
    arcpy.DeleteField_management(submarketsJoinedToMarkets,["Xi"])

#add Xi field to submarketsJoinedToMarkets
arcpy.AddField_management   (submarketsJoinedToMarkets,
                            "Xi",
                            "FLOAT",
                            5,
                            4)

#set to calculate proportion of total submarket metric to total market metric
calculateProp = "float(!submarketMetric!)/!marketMetric!"

#calculate Xi
arcpy.CalculateField_management (submarketsJoinedToMarkets,
                                "Xi",
                                calculateProp,
                                "PYTHON_9.3")
###############################################################################
###############################################################################
###############################################################################
#Calculate the square of Xi - Xi squared;
#delete XiSquared field if it exists in submarketsJoinedToMarkets
if len(arcpy.ListFields(submarketsJoinedToMarkets, "XiSquared")) > 0:
    arcpy.DeleteField_management(submarketsJoinedToMarkets,["XiSquared"])

#add XiSquared field to submarketsJoinedToMarkets
arcpy.AddField_management   (submarketsJoinedToMarkets,
                            "XiSquared",
                            "FLOAT",
                            15,
                            14)

#set to calculate square of Xi
calculateSquare = "!Xi!*!Xi!"

#calculate square of Xi
arcpy.CalculateField_management (submarketsJoinedToMarkets,
                                "XiSquared",
                                calculateSquare,
                                "PYTHON_9.3")
###############################################################################
###############################################################################
###############################################################################
#Sum squared Xi by market;
#set table name
sumXiSquaredByMarketPath = str(path) + "\\sumXiSquaredByMarket"

#delete sumXiSquaredByMarket table if it already exists
if arcpy.Exists(sumXiSquaredByMarketPath):
    arcpy.Delete_management(sumXiSquaredByMarketPath)

#sum firms' metric by market
arcpy.Statistics_analysis   (submarketsJoinedToMarkets,
                            sumXiSquaredByMarketPath,
                            [["XiSquared", "SUM"]],
                            ["market"])

#rename summed metric field
arcpy.AlterField_management (sumXiSquaredByMarketPath,
                            "SUM_XiSquared",
                            "sumXiSquaredByMarket",
                            "sumXiSquaredByMarket")
###############################################################################
###############################################################################
###############################################################################
#Rejoin sum of square Xi's to spatial join of submarkets to markets by market;
#delete sumXiSquaredByMarket field if it exists in submarketsJoinedToMarkets
if len(arcpy.ListFields(submarketsJoinedToMarkets, "sumXiSquaredByMarket")) > 0:
    arcpy.DeleteField_management(submarketsJoinedToMarkets,["sumXiSquaredByMarket"])


#join the sumXiSquaredByMarket to submarketsJoinedToMarkets by market
arcpy.JoinField_management  (submarketsJoinedToMarkets,
                            "market",
                            sumXiSquaredByMarketPath,
                            "market",
                            ["sumXiSquaredByMarket"])
###############################################################################
###############################################################################
###############################################################################
arcpy.SetParameterAsText(1,submarketsJoinedToMarkets)