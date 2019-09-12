#-------------------------------------------------------------------------------
# Name:        addCalcMarketFirmField
#
# Purpose:     Add and calculate a field comprising the concatenation of the
#              market and firm field; the market and firm are separated by
#              an underscore
#
# Author:      Matthew Sutton
#
# Created:     21/12/2018
#-------------------------------------------------------------------------------

import arcpy

#set spatial join var
spatialJoin = arcpy.GetParameterAsText(0)

#delete market_firm field var if it exists
if len(arcpy.ListFields(spatialJoin, "market_firm")) > 0:
    arcpy.DeleteField_management(spatialJoin,["market_firm"])

#add empty market_firm field
arcpy.AddField_management   (spatialJoin,
                            "market_firm",
                            "TEXT")

#set market_firm field calculation
calculateMarketFirmField = '!market! + "_" + !firm!'

#calculate market_firm field
arcpy.CalculateField_management (spatialJoin,
                                "market_firm",
                                calculateMarketFirmField,
                                "PYTHON_9.3")

#create output node for model builder
arcpy.SetParameterAsText(1, spatialJoin)