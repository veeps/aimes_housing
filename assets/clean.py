
# Import libraries here.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import pickle
get_ipython().run_line_magic('run', '../assets/eda.py')



def clean(filepath):
    df = pd.read_csv(filepath , index_col='Id')

    # clean column names
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.lower()

    # fill in NA values
    df["misc_feature"].fillna("None", inplace = True)
    df["alley"].fillna("None", inplace = True)
    df["fence"].fillna("None", inplace = True)

    # create a new boolean column for houses with pool vs. no pool
    df["has_pool"] = np.where(df["pool_qc"].notnull(), 1, 0)
    # drop pool area and pool qc columns
    df.drop(columns = ["pool_area", "pool_qc"], inplace = True)
    
    # create a new boolean column if the house has been remodeled or not
    df["has_remodel"] = np.where(df["year_built"] != df["year_remod/add"], 1, 0)

    # find the rows that do not have a garage
    no_garage = df["garage_type"].isnull()  & df["garage_finish"].isnull() & df["garage_qual"].isnull()  & df["garage_cond"].isnull()  == True

    # replace NA values with "None" across these rows
    df.loc[no_garage, df.columns[df.columns.str.contains("garage")]] = df.loc[no_garage, df.columns[df.columns.str.contains("garage")]].fillna("None")


    # create conversion dictionarys
    # this code was adapted from this stack overflow answer: https://stackoverflow.com/questions/21818886/changing-ordinal-character-data-to-numeric-data-with-pandas
    conv_dict_2={
    "Y": 1,
    "N": 0
}
    
    conv_dict_5 = {
        "Ex" : int(5),
        "Gd" : int(4),
        "TA" : int(3),
        "Fa" : int(2),
        "Po" : int(1),
    }


    conv_dict_4 = {
        "Ex" : int(4),
        "Gd" : int(3),
        "TA" : int(2),
        "Fa" : int(1)
    }

    conv_dict_6 ={
        "GLQ" : 5,
        "ALQ" : 4,
        "BLQ" : 3,
        "Rec" : 2,
        "LwQ" : 1,
        "Unf" : 0,
    }

    neighborhood_dict = {'Blmngtn': 'medium',
      'Blueste': 'medium',
      'BrDale': 'medium',
      'BrkSide': 'medium',
      'ClearCr': 'medium',
      'CollgCr': 'medium',
      'Crawfor': 'medium',
      'Edwards': 'medium',
      'Gilbert': 'medium',
      'Greens': 'medium',
      'GrnHill': 'high',
      'IDOTRR': 'low',
      'Landmrk': 'medium',
      'MeadowV': 'medium',
      'Mitchel': 'medium',
      'NAmes': 'medium',
      'NPkVill': 'medium',
      'NWAmes': 'medium',
      'NoRidge': 'medium',
      'NridgHt': 'high',
      'OldTown': 'medium',
      'SWISU': 'medium',
      'Sawyer': 'medium',
      'SawyerW': 'medium',
      'Somerst': 'medium',
      'StoneBr': 'high',
      'Timber': 'medium',
      'Veenker': 'medium'}

    housing_stock = {
      "NAmes": 5,
      "CollgCr": 4,
      "OldTown": 4,
      "Edwards": 4,
      "Somerst": 4,
      "NridgHt": 4,
      "Gilbert": 4,
      "Sawyer": 4,
      "NWAmes": 3,
      "SawyerW": 3,
      "Mitchel": 3,
      "BrkSide": 3,
      "Crawfor": 3,
      "IDOTRR": 3,
      "NoRidge": 2,
      "Timber": 2,
      "StoneBr": 2,
      "SWISU": 2,
      "ClearCr": 2,
      "MeadowV": 1,
      "Blmngtn": 1,
      "BrDale": 1,
      "NPkVill": 1,
      "Veenker": 1,
      "Blueste": 1,
      "Greens": 1,
      "GrnHill": 1,
      "Landmrk": 1}


    def replace_ordinal(columns, df, dictionary):
        for column in columns:
            df[column] = df[column].apply(dictionary.get)


    # convert the columns with "Ex", "Gd", "TA", "Fa", and "Po" values to a numeric
    replace_ordinal(["exter_qual",
                     "exter_cond",
                     "bsmt_qual", 
                     "bsmt_cond",
                     "heating_qc",
                     "kitchen_qual",
                     "garage_qual",
                     "garage_cond", 
                     "fireplace_qu"], df, conv_dict_5)


    # convert the columns with "Ex", "Gd", "TA", and "Fa" values to a numeric
    #replace_ordinal(["pool_qc"], df, conv_dict_4)

    replace_ordinal(["bsmtfin_type_1", "bsmtfin_type_2"], df, conv_dict_6)
    
    # convert the columns with "N", "Y"  values to a numeric
    replace_ordinal(["central_air",  "paved_drive"], df, conv_dict_2)

    # fill NA's with 0 for basment quality
    df["bsmt_qual"].fillna(0, inplace = True)

    # fill NA's with 0 for garage quality
    df["garage_qual"].fillna(0, inplace = True)

    # fill NA's with 0 for garage cars
    df["garage_cars"].fillna(0, inplace = True)

    # categorize neighborhood sale prices
    df["neighborhood_price"] = df["neighborhood"].apply(neighborhood_dict.get)

    # create dummy variables for neighborhood price
    df = pd.get_dummies(df, columns = ["neighborhood_price"])

    df.drop("neighborhood_price_medium", axis=1, inplace = True)

    # create function to read through the values for each type
    def format_zone(zone):
        if zone == "RL":
            return zone
        if zone == "RM":
            return zone
        if zone == "FV" :
            return zone
        else:
            return "Other"

    # apply to ms_zone column
    df["ms_zoning"] = df["ms_zoning"].apply(format_zone)

    # create dummy variables for zones
    df = pd.get_dummies(df, columns = ["ms_zoning"])

    # remove the other column to set as default
    df.drop("ms_zoning_Other", axis=1, inplace = True)

    # create dummy variables for condition
    df = pd.get_dummies(df, columns = ["condition_1"])

    # remove the normal column to set as default
    df.drop("condition_1_Norm", axis=1, inplace = True)

    # categorize neighborhood housing stock
    df["housing_stock"] = df["neighborhood"].apply(housing_stock.get)

    # add a column for bathroom to bedroom ratio

    df["bed_bath_ratio"] = df["bedroom_abvgr"]/(df["full_bath"] + df["half_bath"])

    # replace the null values with 0
    df["bed_bath_ratio"].fillna(0, inplace = True)

    # replace the infinity values with 0
    df["bed_bath_ratio"].replace(np.inf, 0, inplace = True)

    # create function to read through the values for each type
    def format_garage(garage):
        if garage == "Attchd":
            return garage
        if garage == "BuiltIn":
            return garage
        if garage == "Basment" :
            return garage
        else:
            return "Other"

    # apply to garage_type column
    df["garage_type"] = df["garage_type"].apply(format_garage)

    # create dummy variables
    df = pd.get_dummies(df, columns = ["garage_type"])

    # remove the other column to set as default
    df.drop("garage_type_Other", axis=1, inplace = True)

    # interaction column for garage quality * number of cars
    df["garage_qual_cars"] = df["garage_qual"] * df["garage_cars"]

    # total square feet



    return df

