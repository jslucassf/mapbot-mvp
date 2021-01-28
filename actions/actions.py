# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database.geoDAO import GeoDAO
from database.conversationDAO import ConversationDAO
from utils.filterNLUData import filter_spatial_relation, filter_landmark
from time import time

DEBUG_LOGS = False

class ActionFoundOrNot(Action):
    def name(self) -> Text:
        return "action_found_or_not"

    def get_current_entities(self, entities):
        spatial_relations = filter(lambda entity: entity["entity"][:2] == "sr", entities)
        landmarks = filter(lambda entity: entity["entity"] == "landmark", entities)

        return (list(spatial_relations), list(landmarks))

    def get_relation_and_references(self, spatial_relations, landmarks):
        relation_landmark_pairs = []

        spatial_relations = list(map(filter_spatial_relation, spatial_relations))
        landmarks = list(map(filter_landmark, landmarks))

        viewed_landmark_index = 0
        for spatial_relation in spatial_relations:
            if spatial_relation["relation_name"] == "sr_between":
                relation_landmark_pairs.append({"relation": spatial_relation,
                                                "first_landmark": landmarks[viewed_landmark_index],
                                                "second_landmark": landmarks[viewed_landmark_index + 1]})
                viewed_landmark_index += 2
            else:
                relation_landmark_pairs.append({"relation": spatial_relation,
                                                "landmark": landmarks[viewed_landmark_index]})
                viewed_landmark_index += 1

        return relation_landmark_pairs

    # WARNING: THIS METHOD CURRENTLY SUPPORTS ONLY ONE PAIR OF RELATION-LANDMARK
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        spatial_relations, landmarks = self.get_current_entities(tracker.latest_message["entities"])
        
        relation_and_references = self.get_relation_and_references(spatial_relations, landmarks)

        geoDAO = GeoDAO()

        relation_regions = []
        for relationship in relation_and_references:
            if DEBUG_LOGS:
                print(relationship)
            
            relation_regions.append(geoDAO.resolve_spatial_relation(relationship)[0])

        acceptance_region = geoDAO.intersect_regions(relation_regions)

        if DEBUG_LOGS:
            print(relation_regions)
            print('------------')
        
        print(acceptance_region)

        conversationDAO = ConversationDAO()

        if False: # Disable to prevent inserting too much data into the DB while testing
            conversationDAO.insert_interaction(tracker, acceptance_region)        
        
        found_or_not = geoDAO.contains_goal(acceptance_region)

        if(found_or_not):
            dispatcher.utter_message(text="Localização encontrada, obrigado!")
        else:
            dispatcher.utter_message(text="Não consegui encontrar a localização " +
                                            "na região que você descreveu, poderia tentar mais uma vez?")
        return []
