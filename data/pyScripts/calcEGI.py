#-------------------------------------------------------------------------------
# Name:        calcEGI
#
# Purpose:     calculate EGI for markets:
#
#              calculate EGI for markets:
#                   ( sumSiMinusXiSquared
#                       minus
#                   ( (1 minus sumXiSquaredByMarket)
#                       times
#                   marketIndustryHHI) ) )
#                       divided by
#                   ( (1 minus sumXiSquaredByMarket)
#                       times
#                   (1 minus marketIndustryHHI) );
#              join EGI to input markets FC;
#
#
# Author:      Matthew Sutton
#
# Created:     30/12/2018
#-------------------------------------------------------------------------------
import arcpy

#get and set submarkets-markets join
submarketsJoinedToMarkets = arcpy.GetParameterAsText(0)
###############################################################################
###############################################################################
###############################################################################
#calculate EGI for markets:
#                   ( sumSiMinusXiSquared
#                       minus
#                   ( (1 minus sumXiSquaredByMarket)
#                       times
#                   marketIndustryHHI) ) )
#                       divided by
#                   ( (1 minus sumXiSquaredByMarket)
#                       times
#                   (1 minus marketIndustryHHI) );
#delete new field if it already exists
if len(arcpy.ListFields(submarketsJoinedToMarkets, "EGI")) > 0:
    arcpy.DeleteField_management(submarketsJoinedToMarkets,["EGI"])

#add EGI to submarketsJoinedToMarkets
arcpy.AddField_management   (submarketsJoinedToMarkets,
                            "EGI",
                            "FLOAT",
                            15,
                            14)

#set calculation to EGI
calculateEGI = "(!sumSiMinusXiSquared!-((1-!sumXiSquaredByMarket!)*!marketIndustryHHI!))/((1-!sumXiSquaredByMarket!)*(1-!marketIndustryHHI!))"

#calculate markets' EGI
arcpy.CalculateField_management (submarketsJoinedToMarkets,
                                "EGI",
                                calculateEGI,
                                "PYTHON_9.3")
###############################################################################
###############################################################################
###############################################################################

#create output node for model builder
arcpy.SetParameterAsText(1, submarketsJoinedToMarkets)