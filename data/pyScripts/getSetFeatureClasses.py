#-------------------------------------------------------------------------------
# Name:        getSetFeatureClasses
#
# Purpose:     get input FCs and duplicate them in the output GDB; set vars for
#              analysis
#
# Author:      Matthew Sutton
#
# Created:     22/12/2018
#-------------------------------------------------------------------------------
import arcpy

#get and set markets FC
markets = arcpy.GetParameterAsText(0)

#get and set the markets' metric and markets fields
marketsField = arcpy.GetParameterAsText(1)
marketsMetricField = arcpy.GetParameterAsText(2)

#create list of fields from the markets FC for field mapping
marketsFieldList = [marketsField, marketsMetricField]

#create FieldMappings for markets
fms_markets = arcpy.FieldMappings()

#for each field in marketsFieldList, set an empty FieldMap, add the field to the
#FieldMap, and add the FieldMap to the FieldMappings
for field in marketsFieldList:
    fm_marketField = arcpy.FieldMap()
    fm_marketField.addInputField(markets, field)
    fms_markets.addFieldMap(fm_marketField)


#get and set submarkets FC
submarkets = arcpy.GetParameterAsText(3)

#get and set the submarkets' metric, submarket, and market fields
submarketsField = arcpy.GetParameterAsText(4)
submarketsMarketField = arcpy.GetParameterAsText(5)
submarketsMetricField = arcpy.GetParameterAsText(6)

#create list of fields from submarkets FC to use for field mapping
submarketsFieldList = [submarketsField,submarketsMarketField,submarketsMetricField,]

#create FieldMappings for submarkets
fms_submarkets = arcpy.FieldMappings()

#for each field in submarketsFieldList, set an empty FieldMap, add the field to the
#FieldMap, and add the FieldMap to the FieldMappings
for field in submarketsFieldList:
    fm_submarketField = arcpy.FieldMap()
    fm_submarketField.addInputField(submarkets, field)
    fms_submarkets.addFieldMap(fm_submarketField)


#get and set firms FC
firms = arcpy.GetParameterAsText(7)

#get and set firms' metric and firm fields
firmsMetricField = arcpy.GetParameterAsText(8)
firmField = arcpy.GetParameterAsText(9)

#create list of fields from firms FC to use for field mapping
firmsFieldList = [firmsMetricField, firmField]

#create FieldMappings for firms
fms_firms = arcpy.FieldMappings()

#for each field in firmsFieldsList, set an empty FieldMap, add the field to the
#FieldMap, and add the FieldMap to the FieldMappings
for field in firmsFieldList:
    fm_firmField = arcpy.FieldMap()
    fm_firmField.addInputField(firms, field)
    fms_firms.addFieldMap(fm_firmField)


#set output GDB path and output GDB name
outputGDB = arcpy.GetParameterAsText(10)

#set market output path
marketsOutputPath = outputGDB + "\\markets"

#set submarkets output path
submarketsOutputPath = outputGDB + "\\submarkets"

#set firms output path
firmsOutputPath = outputGDB + "\\firms"

#delete markets, submarkets, and firms FCs if they already exist in the
#output GDB
if arcpy.Exists(marketsOutputPath):
    arcpy.Delete_management(marketsOutputPath)
if arcpy.Exists(submarketsOutputPath):
    arcpy.Delete_management(submarketsOutputPath)
if arcpy.Exists(firmsOutputPath):
    arcpy.Delete_management(firmsOutputPath)


#create new markets FC in output GDB
arcpy.FeatureClassToFeatureClass_conversion(markets,
                                            outputGDB,
                                            "markets",
                                            "#",
                                            fms_markets)
#rename markets field
arcpy.AlterField_management (marketsOutputPath,
                            marketsField,
                            "market",
                            "market")
#rename markets' metric field
arcpy.AlterField_management (marketsOutputPath,
                            marketsMetricField,
                            "marketMetric",
                            "marketMetric")

#create new submarkets FC in output GDB
arcpy.FeatureClassToFeatureClass_conversion(submarkets,
                                            outputGDB,
                                            "submarkets",
                                            "#",
                                            fms_submarkets)
#rename submarkets field
arcpy.AlterField_management (submarketsOutputPath,
                            submarketsField,
                            "submarket",
                            "submarket")
#rename submarkets' market field
arcpy.AlterField_management (submarketsOutputPath,
                            submarketsMarketField,
                            "submarketMarket",
                            "submarketMarket")
#rename submarkets' metric field
arcpy.AlterField_management (submarketsOutputPath,
                            submarketsMetricField,
                            "submarketMetric",
                            "submarketMetric")


#create new firms FC in output GDB
arcpy.FeatureClassToFeatureClass_conversion(firms,
                                            outputGDB,
                                            "firms",
                                            "#",
                                            fms_firms)
#rename market measure field
arcpy.AlterField_management (firmsOutputPath,
                            firmsMetricField,
                            "firmMetric",
                            "firmMetric")
#rename firm field
arcpy.AlterField_management (firmsOutputPath,
                            firmField,
                            "firm",
                            "firm")

#creates output nodes for model builder
arcpy.SetParameterAsText(11, marketsOutputPath)
arcpy.SetParameterAsText(12, submarketsOutputPath)
arcpy.SetParameterAsText(13, firmsOutputPath)