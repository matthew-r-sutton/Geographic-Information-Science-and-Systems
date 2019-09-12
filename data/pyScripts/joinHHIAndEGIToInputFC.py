#-------------------------------------------------------------------------------
# Name:        joinHHIAndEGIToInputFC
# Purpose:     join HHI and EGI to the input FC
#
# Author:      Matthew Sutton
#
# Created:     30/12/2018
#-------------------------------------------------------------------------------
import arcpy

#get and set
marketsJoinedToFirms = arcpy.GetParameterAsText(0)
submarketsJoinedToMarkets = arcpy.GetParameterAsText(1)
inputMarketsFC = arcpy.GetParameterAsText(2)
inputMarketsMarketField = arcpy.GetParameterAsText(3)
###############################################################################
###############################################################################
###############################################################################
#join HHI and EGI to the input FC;
#delete HHI and EGI fields if they exist in inputMarketsFC
if len(arcpy.ListFields(inputMarketsFC, "HHI")) > 0:
    arcpy.DeleteField_management(inputMarketsFC,["HHI"])
if len(arcpy.ListFields(inputMarketsFC, "EGI")) > 0:
    arcpy.DeleteField_management(inputMarketsFC,["EGI"])

#join the HHI to inputMarketsFC by market
arcpy.JoinField_management  (inputMarketsFC,
                            inputMarketsMarketField,
                            marketsJoinedToFirms,
                            "market",
                            ["HHI"])
#join the EGI to inputMarketsFC by market
arcpy.JoinField_management  (inputMarketsFC,
                            inputMarketsMarketField,
                            submarketsJoinedToMarkets,
                            "market",
                            ["EGI"])
###############################################################################
###############################################################################
###############################################################################
arcpy.SetParameterAsText(1,submarketsJoinedToMarkets)

