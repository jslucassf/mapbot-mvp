# Helper functions to filter data from the objects that RASA extracts
# from the text

def filter_confidence_and_value(entity):
    return {
        "confidence": entity["confidence_entity"],
        "text": entity["value"]
    }

def filter_spatial_relation(entity):
    spatial_relation = filter_confidence_and_value(entity)
    spatial_relation["relation_name"] = entity["entity"]

    return spatial_relation

def filter_landmark(entity):
    return filter_confidence_and_value(entity)
    