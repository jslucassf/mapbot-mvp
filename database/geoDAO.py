# TODO: THINK OF A BETTER NAME
import psycopg2
from database.objectDAO import ObjectDAO
from utils.fuzzyLandmarkSearch import fuzzyLandmarkSearch
from database.spatial_relations_functions import get_appropriate_relation_function

class GeoDAO(ObjectDAO):

    def find_landmark(self, landmark_fk):
        connection = self.init_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM cg_landmarks where id='{}'".format(landmark_fk)
        cursor.execute(query)
        recset = cursor.fetchall()[0]

        self.close_connection(connection)

        return {
            "id": recset[0],
            "class": recset[1],
            "name": recset[2],
            "type": recset[3],
            "geom": recset[4]

        }

    # TEMP
    def contains_goal(self, acceptance_region):
        query = '''SELECT ST_Contains(ST_GeomFromGeoJSON('{}'),
                                    ST_GeomFromText('POINT(-35.8709436 -7.2322137)', 4326));''' \
                                    .format(acceptance_region)

        contains = self.run_query(query)

        return contains

    def resolve_spatial_relation(self, relationship):
        relation_function = get_appropriate_relation_function(relationship["relation"]["relation_name"])
        
        connection = self.init_connection()
        cursor = connection.cursor()
        
        if relationship["relation"]["relation_name"] == "sr_between":
            true_entity_1 = fuzzyLandmarkSearch(relationship["first_landmark"]["text"])
            true_entity_2 = fuzzyLandmarkSearch(relationship["second_landmark"]["text"])
            
            projection = relation_function([true_entity_1["landmark_fk"], true_entity_2["landmark_fk"]], cursor)
        else:
            true_entity = fuzzyLandmarkSearch(relationship["landmark"]["text"])

            projection = relation_function(true_entity["landmark_fk"], cursor)

        self.close_connection(connection)

        return projection

    def intersect_regions(self, regions):
        current_region = regions[0]
        for region_index in range(1, len(regions)):
            query = '''SELECT ST_AsGeoJSON(ST_Intersection(ST_GeomFromGeoJSON('{}'), ST_GeomFromGeoJSON('{}')));''' \
                                    .format(current_region, regions[region_index])

            current_region = self.run_query(query)

        return current_region