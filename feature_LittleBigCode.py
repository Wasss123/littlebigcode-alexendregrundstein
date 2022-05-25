"""
This program allows to display the journal that mentions the most different drugs.
It is called feature_LittleBigCode.py
"""

__authors__ = "Alexandre Grundstein"
__date__ = "2022-05-24"
__version__= "1.0.0."

import pandas as pd


df=pd.read_json("results/drugs.json") # Recovery of the JSON file

df = df[["atccode","journal_mentions"]] # Selection of the variables of interest
df = df.explode("journal_mentions").reset_index(drop=True) # Creation of as many lines as different journals (+date) there are
df["journal"] = df.apply(lambda x: x["journal_mentions"]["journal"],axis=1) # Creation of the journal variable to enter the name of the journal
df = df.drop_duplicates(subset=["atccode","journal"]) 

df_final = df[["atccode","journal"]].groupby(["journal"]).count().sort_values(["atccode"], ascending=False) # Calculation of the number of drugs mentionned per journal
df_final = df_final.loc[df_final["atccode"]==df_final["atccode"].max()] # Selection of the journal(s) with the max number of drugs
print(df_final)