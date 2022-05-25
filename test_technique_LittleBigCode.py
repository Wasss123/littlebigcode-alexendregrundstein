"""
This program creates a JSON file representing a link graph between drugs and their respective
mentions in PubMed, scientific publications and journals.
It is called test_technique_LittleBigCode.py
"""

__authors__ = "Alexandre Grundstein"
__date__ = "2022-05-24"
__version__= "1.0.0."

import pandas as pd
import json


def drugs_mention(x,dict_drugs):
    """This function takes as arguments a variable (x) and a dictionnary (dict_drugs)
       It returns a list with drugs from the dictionnary that are also in the variable.
    """
    list_drugs = []
    for key, value in dict_drugs.items():
        if value in x.upper():
            list_drugs.append(dict_drugs[key])
    return list_drugs


def modify_header(df):
    """This function takes the first line of a dataframe to modify the column names of this dataframe.
       The dataframe is the argument of the function.
       The function returns the dataframe with new column names.
    """
    new_header = df.iloc[0]
    df = df[1:] #take the data less the header row
    df.columns = new_header
    return df


def drugs_var_creation(df,title):
    """This function takes a dataframe as argument and adds it a variable (drugs)
       which contains a list of drugs (from dict_drugs) that are presents in the 
       article.
       It also creates as many lines as drugs in the corresponding article.
    """
    df["drugs"] = df[title].apply(lambda x : drugs_mention(x,dict_drugs)) 
    df = df.explode("drugs") # Creation of one line per drug per article
    df = df.loc[df["drugs"].notna()] # Deletion of lines without drugs
    return df


def to_dict_article(id,title,date):
    """This function returns a dictionnary with the following keys: id, article and date.
       The values for these keys are the arguments of the function. 
    """
    tmp_dict = {
        "id" : id,
        "article" : title,
        "date" : date
    }
    return tmp_dict


def to_dict_journal(journal,date):
    """This function returns a dictionnary with the following keys: journal and date.
       The values for these keys are the arguments of the function.
    """
    tmp_dict = {
        "journal" : journal,
        "date" : date
    }
    return tmp_dict


def mentions(df,mentions):
    """This function takes a dataframe as argument and returns a transposition of this dataframe.
       Morover, it creates a variable "mentions" in which a dictionnary is created with all the id, title and date
       of the different articles where a drug is mentionned.
    """
    df[mentions] = df.apply(lambda x : to_dict_article(x["id"],x["title"],x["date"]),axis=1)
    df = df[["drugs",mentions]].groupby(["drugs"])[mentions].apply(list).to_frame().reset_index() 
    df = df.T
    return df


# Downloading of csv files from GitHub
drugs_csv = "https://raw.githubusercontent.com/alexandregrundstein/littlebigcode/main/drugs.csv"
pubmed_csv = "https://raw.githubusercontent.com/alexandregrundstein/littlebigcode/main/pubmed.csv"
trials_csv = "https://raw.githubusercontent.com/alexandregrundstein/littlebigcode/main/clinical_trials.csv"

df_drugs = pd.read_csv(drugs_csv, header=0)
df_pubmed = pd.read_csv(pubmed_csv, header=0)
df_trials = pd.read_csv(trials_csv, header=0)

# Data cleaning of df_trials
df_trials.loc[df_trials["journal"].isna(),"journal"] = "Journal of emergency nursing" # Journal name was empty
df_trials.loc[df_trials["id"]=="NCT04188184","journal"] = "Journal of emergency nursing" # Journal name was misswritten
df_trials = df_trials.loc[df_trials["id"].notna()] # Deletion of lines with empty ids
df_trials = df_trials.loc[df_trials["id"]!="NCT04237090"] # Deletion of line with id="NCT04237090" because of empty title

# Date formatting in standard format %YYYY-%MM-%DD for all dates
df_trials["date"] = pd.to_datetime(df_trials["date"]).astype(str)
df_pubmed["date"] = pd.to_datetime(df_pubmed["date"]).astype(str)

# Creation of dict_drugs
df_drugs_T = df_drugs[["atccode","drug"]].T # Transposition of the df_drugs dataframe
df_drugs_T = modify_header(df_drugs_T) # Column names modification
dict_drugs = df_drugs_T.to_dict("records")[0] # Creation of a dictionnary with atccode as key and drug name as value


# Addition of the column "drugs" for the mentionned drugs in pubmed dataframe
df_pubmed = drugs_var_creation(df_pubmed,"title")

# Addition of the column "drugs" for the mentionned drugs in clinical trials dataframe
df_trials = drugs_var_creation(df_trials,"scientific_title")

# Creation of journal dataframe
df_trials.columns = df_pubmed.columns
df_journal = pd.concat([df_trials,df_pubmed])
df_journal = df_journal[["date","journal","drugs"]].drop_duplicates() # Selection of columns and deletion of duplicates lines


# Creation of pubmed_mentions variable in df_pubmed
df_pubmed = mentions(df_pubmed,"pubmed_mentions")
df_pubmed = modify_header(df_pubmed)

# Creation of clin_trials_mentions variable in df_trials
df_trials = mentions(df_trials,"clin_trials_mentions")
df_trials = modify_header(df_trials)

# Creation of journal_mentions variable in df_journal
df_journal["journal_mentions"] = df_journal.apply(lambda x : to_dict_journal(x["journal"],x["date"]),axis=1)
df_journal = df_journal[["drugs","journal_mentions"]].groupby(["drugs"])["journal_mentions"].apply(list).to_frame().reset_index()
df_journal = df_journal.T
df_journal = modify_header(df_journal)

# Creation of the dataframe containing information on pubmed, clinical_trials and journal
df = pd.concat([df_pubmed,df_trials,df_journal]) 

df = df.T
df = df.reset_index()
df = df.merge(df_drugs,left_on="drugs",right_on="drug").drop(["drug"], axis=1) # Merge to add the atccode
df = df[["atccode","drugs","pubmed_mentions","clin_trials_mentions","journal_mentions"]] 

# Creation of the final dictionnary
dict_final = df.to_dict("records")

# Creation of the JSON file
with open("results/drugs.json", "w") as fp:
    json.dump(dict_final, fp, indent=4)

with open("results/drugs.json", "r") as fp:
    data = json.load(fp)
