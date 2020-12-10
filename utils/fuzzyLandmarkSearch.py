import pandas as pd
from fuzzywuzzy import process

def fuzzyLandmarkSearch(landmark_reference):
    aliases = pd.read_csv("static-data/landmark_aliases_no_duplicates.csv")
    aliases = zip(list(aliases.landmark_alias), list(aliases.landmark_fk))
    aliases = dict(aliases)

    closest_landmark_entry = process.extract(landmark_reference, list(aliases.keys()), limit=1)

    closest_landmark_entry = {
        "landmark_name": closest_landmark_entry[0][0],
        "landmark_fk": aliases[closest_landmark_entry[0][0]],
        "similarity": closest_landmark_entry[0][1]}

    return closest_landmark_entry



def cleanRepeatedEntries():
    repeated = pd.read_csv("static_data/repeated.csv")
    aliases = pd.read_csv("static_data/landmark_aliases.csv")

    aliases = aliases.drop_duplicates(subset="landmark_alias", keep="first")

    aliases.to_csv("static_data/landmark_aliases_no_duplicates.csv", index = False)