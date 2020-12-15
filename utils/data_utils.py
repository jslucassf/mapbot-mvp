import pandas as pd

def cleanRepeatedEntries():
    repeated = pd.read_csv("static-data/repeated.csv")
    aliases = pd.read_csv("static-data/landmark_aliases.csv")

    aliases = aliases.drop_duplicates(subset="landmark_alias", keep="first")

    aliases.to_csv("static-data/landmark_aliases_no_duplicates.csv", index = False)

def generate_lookup_table():
    aliases = pd.read_csv("static-data/landmark_aliases_no_duplicates.csv")

    aliases.landmark_alias.to_csv('static-data/lookup.txt', header=False, index=False, sep='\n', mode='a')