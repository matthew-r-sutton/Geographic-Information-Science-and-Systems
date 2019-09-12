#-------------------------------------------------------------------------------
# Name:        calcSiAndSumOfSiMinusXiSquaredByMarket
# Purpose:     Calculate Si:
#
#              Use firms joined to submarkets to sum firm metric by submarket;
#              Use firms joined to submarkets to sum firm metric by
#              submarketMarket;
#              Rejoin firm metric summed by submarket and firm metric summed by
#              submarketMarketto submarkets-markets spatial join, using
#              submarket, making sure that null values are then converted to
#              zeroes;
#              Calculate the proportion of firmMetricBySubmarket to
#              firmMetricBySubmarketMarket - Si;
#              Subtract Xi from Si and square the result;
#              Sum square (Si - Xi) by market and rejoin the result to submarket
#              -market join by market;
#
# Author:      Matthew Sutton
#
# Created:     29/12/2018
#-------------------------------------------------------------------------------
import arcpy

#get and set firms and submarkets
submarketsJoinedToMarkets = arcpy.GetParameterAsText(0)
firmsJoinedToSubmarkets = arcpy.GetParameterAsText(1)
###############################################################################
###############################################################################
###############################################################################
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
#Use firms joined to submarkets to sum firm metric by submarket;
#set table name
sumFirmMetricBySubmarketPath = str(path) + "\\sumFirmMetricBySubmarket"

#delete sumFirmMetricBySubmarket table if it already exists
if arcpy.Exists(sumFirmMetricBySubmarketPath):
    arcpy.Delete_management(sumFirmMetricBySubmarketPath)

#sum firms' metric by submarket
arcpy.Statistics_analysis   (firmsJoinedToSubmarkets,
                            sumFirmMetricBySubmarketPath,
                            [["firmMetric", "SUM"]],
                            ["submarket"])

#rename summed metric field
arcpy.AlterField_management (sumFirmMetricBySubmarketPath,
                            "SUM_firmMetric",
                            "firmMetricBySubmarket",
                            "firmMetricBySubmarket")
###############################################################################
###############################################################################
###############################################################################
#Use firms joined to submarkets to sum firm metric by submarketMarket;
#set table name
sumFirmMetricBySubmarketMarketPath = str(path) + "\\sumFirmMetricBySubmarketMarket"

#delete sumFirmMetricMarket table if it already exists
if arcpy.Exists(sumFirmMetricBySubmarketMarketPath):
    arcpy.Delete_management(sumFirmMetricBySubmarketMarketPath)

#sum firms' metric by submarketMarket
arcpy.Statistics_analysis   (firmsJoinedToSubmarkets,
                            sumFirmMetricBySubmarketMarketPath,
                            [["firmMetric", "SUM"]],
                            ["submarketMarket"])

##rename summed metric field
arcpy.AlterField_management (sumFirmMetricBySubmarketMarketPath,
                           "SUM_firmMetric",
                           "firmMetricByMarket",
                           "firmMetricByMarket")

###############################################################################
###############################################################################
###############################################################################
#Rejoin firm metric summed by submarket to submarketsJoinedToMarkets,
#using submarket;
#delete firmMetricBySubmarket & firmMetricBySubmarketMarket fields if they exist
#in submarketsJoinedToMarkets
if len(arcpy.ListFields(submarketsJoinedToMarkets, "firmMetricByMarket")) > 0:
    arcpy.DeleteField_management(submarketsJoinedToMarkets,["firmMetricByMarket"])
if len(arcpy.ListFields(submarketsJoinedToMarkets, "firmMetricByMarket")) > 0:
    arcpy.DeleteField_management(submarketsJoinedToMarkets,["firmMetricByMarket"])


#join firmMetricBySubmarket and firmMetricBySubmarketMarket to
#submarketsJoinedToMarkets by submarket
arcpy.JoinField_management  (submarketsJoinedToMarkets,
                            "submarket",
                            sumFirmMetricBySubmarketPath,
                            "submarket",
                            ["firmMetricBySubmarket"])


#change null values to zeroes
with arcpy.da.UpdateCursor  (submarketsJoinedToMarkets,
                            ["firmMetricBySubmarket"]) as row:
    for obs in row:
        if obs[0] == None:
            obs[0] = 0
            row.updateRow(obs)
arcpy.JoinField_management  (submarketsJoinedToMarkets,
                            "submarketMarket",
                            sumFirmMetricBySubmarketMarketPath,
                            "submarketMarket",
                            ["firmMetricByMarket"])
#change null values to zeroes
with arcpy.da.UpdateCursor  (submarketsJoinedToMarkets,
                            ["firmMetricByMarket"]) as row:
    for obs in row:
        if obs[0] == None:
            obs[0] = 0
            row.updateRow(obs)
###############################################################################
###############################################################################
###############################################################################
#Calculate the proportion of firmMetricBySubmarket to submarketMetric- Si;
#delete new field if it already exists
if len(arcpy.ListFields(submarketsJoinedToMarkets, "Si")) > 0:
    arcpy.DeleteField_management(submarketsJoinedToMarkets,["Si"])

#add Si to submarketsJoinedToMarkets
arcpy.AddField_management   (submarketsJoinedToMarkets,
                            "Si",
                            "DOUBLE",
                            15,
                            14)

#set calculation to Si
calculateProp = "!firmMetricBySubmarket!/!firmMetricByMarket!"

#calculate proportion of firmMetricBySubmarket to submarketMetric(Si)
arcpy.CalculateField_management (submarketsJoinedToMarkets,
                                "Si",
                                calculateProp,
                                "PYTHON_9.3")
###############################################################################
###############################################################################
###############################################################################
#Subtract Xi from Si and square the result;
#delete new field if it already exists
if len(arcpy.ListFields(submarketsJoinedToMarkets, "SiMinusXiSquared")) > 0:
    arcpy.DeleteField_management(submarketsJoinedToMarkets,["SiMinusXiSquared"])

#add Si to submarketsJoinedToMarkets
arcpy.AddField_management   (submarketsJoinedToMarkets,
                            "SiMinusXiSquared",
                            "DOUBLE",
                            15,
                            14)

#set calculation to square difference of Si and Xi
calculateSqOfDiff = "(!Si!-!Xi!)*(!Si!-!Xi!)"

#calculate square difference of Si and Xi - (Si - Xi)squared
arcpy.CalculateField_management (submarketsJoinedToMarkets,
                                "SiMinusXiSquared",
                                calculateSqOfDiff,
                                "PYTHON_9.3")
###############################################################################
###############################################################################
###############################################################################
#Sum square (Si - Xi) by market and rejoin the result to submarket-market join
#by market;
#set table name
sumSiMinusXiSquaredByMarketPath = str(path) + "\\sumSiMinusXiSquaredByMarket"

#delete sumSiMinusXiSquaredByMarket table if it already exists
if arcpy.Exists(sumSiMinusXiSquaredByMarketPath):
    arcpy.Delete_management(sumSiMinusXiSquaredByMarketPath)

#sum SiMinusXiSquared by market
arcpy.Statistics_analysis   (submarketsJoinedToMarkets,
                            sumSiMinusXiSquaredByMarketPath,
                            [["SiMinusXiSquared", "SUM"]],
                            ["market"])

#rename summed metric field
arcpy.AlterField_management (sumSiMinusXiSquaredByMarketPath,
                            "SUM_SiMinusXiSquared",
                            "sumSiMinusXiSquared",
                            "sumSiMinusXiSquared")

#delete sumSiMinusXiSquared field if it exists in submarketsJoinedToMarkets
if len(arcpy.ListFields(submarketsJoinedToMarkets, "sumSiMinusXiSquared")) > 0:
    arcpy.DeleteField_management(submarketsJoinedToMarkets,["sumSiMinusXiSquared"])


#join the sumSiMinusXiSquared to submarketsJoinedToMarkets by market
arcpy.JoinField_management  (submarketsJoinedToMarkets,
                            "market",
                            sumSiMinusXiSquaredByMarketPath,
                            "market",
                            ["sumSiMinusXiSquared"])
###############################################################################
###############################################################################
###############################################################################
arcpy.SetParameterAsText(2,submarketsJoinedToMarkets)