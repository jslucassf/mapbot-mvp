import pandas as pd
from fuzzywuzzy import process

def fuzzyLandmarkSearch(landmark_reference):
    aliases = pd.read_csv("../data/landmark_aliases_no_duplicates.csv")
    
    results = process.extract(landmark_reference, list(aliases.landmark_alias), limit=3)

    print(results)

def cleanRepeatedEntries():
    repeated = pd.read_csv("../data/repeated.csv")
    aliases = pd.read_csv("../data/landmark_aliases.csv")

    aliases = aliases.drop_duplicates(subset="landmark_alias", keep="first")

    aliases.to_csv("../data/landmark_aliases_no_duplicates.csv", index = False)

    #for name in repeated.name:

#cleanRepeatedEntries()
fuzzyLandmarkSearch("estadual da prata")