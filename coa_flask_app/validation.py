import pandas as pd
import numpy as np

def read_data_dict(input_path):
    test_file = pd.ExcelFile (input_path)
    data_dict1 = {}
    for sheetname in test_file.sheet_names:
        new_data = pd.read_excel(input_path, skiprows=9, usecols = "D:K" , sheet_name=sheetname)
        data_dict1[sheetname] = new_data
    return data_dict1

def make_data_dict2(input_path):
    test_file = pd.ExcelFile (input_path)
    data_dict2 = {}
    for sheetname in test_file.sheet_names:
        new_data = pd.read_excel(input_path, skiprows=9,sheet_name=sheetname)
        new_data = new_data.reset_index(drop=False)
        new_data['index'] = new_data['index']+11
        new_data = new_data.set_index('index')
        data_dict2[sheetname] = new_data
    return data_dict2

# def totalCorrect(data_dict):
#     invalidTotals=[]
#     for r in range(0,data_dict.shape[0]):
#         rowSeries = data_dict.iloc[r]
#         print(rowSeries.values)
#         i=0
#         while i < len(rowSeries.values)-1:
#             if(np.isnan(rowSeries.values[i])):
#                 total += 0
#             else:
#                 total = total + rowSeries.values[i]
#             i+=1
#         print (total)
#         print(rowSeries.values[i])
#     return total
        # if(rowSeries.values[i] != total):
        #     print("ERROR: In row", r, "your total is incorrect!")
        # else:
        #     print("Everything is all right!")

def repetitionOfItems(df):
    temp = df[["Material","Category","Item Name"]]
    return temp[temp.duplicated(keep=False)]


def checkNegative(data):
    problems=[]
    for r in range (0, data.shape[0]):
        rowSeries = data.iloc[r]
        for c in rowSeries.values:
            if c < 0:
                problems.append([r,c])
    return problems

def checkDecimal(data_dict):
    decimal =[]
    for r in range (0, data_dict.shape[0]):
        rowSeries = data_dict.iloc[r]
        for c in rowSeries.values:
            if (pd.isnull(c) == False):
                cFloat = c
                if float(cFloat).is_integer() == False:
                    decimal.append([r,cFloat])
    return decimal

def allValidationChecks(input_path):

    allErrors = []

    data_dict=read_data_dict(input_path)

    data_dict2=make_data_dict2(input_path)

    # for sheetname in data_dict: #this traverses through the multiple sheets
    #     Total = totalCorrect(data_dict[sheetname])
    #     #print (Total)
    for sheetname in data_dict: #this traverses through the multiple sheets
        repetition = repetitionOfItems(data_dict2[sheetname])
        if repetition.empty != True:
            repError = "The following items are repeated in " + (sheetname) + ":"+ str(repetition)
            allErrors.append(repError)
            #print ("The following items are repeated in" ,(sheetname), ":",repetition)
    for sheetname in data_dict:
        these_problems=checkNegative(data_dict[sheetname])
        for rc in these_problems:
            r=rc[0]
            c=rc[1]
            negativeError = "The value "+ str(c)+ " in row " + str(r+11) + " in sheet " + sheetname + " is negative"
            allErrors.append(negativeError)
            #print("A value", c, "in row", r, "in sheet", sheetname ,"is negative")
    for sheetname in data_dict:
        these_decimal=checkDecimal(data_dict[sheetname])
        for rcFloat in these_decimal:
            r=rcFloat[0]
            cFloat=rcFloat[1]
            decError = "A value " + str(cFloat)+ " in row " + str(r+11) + " in sheet " + sheetname + " is a decimal"
            allErrors.append(decError)
            #print("A value", cFloat, "in row", r+11, "in sheet", sheetname ,"is a decimal")
    return allErrors