# TODO: THINK OF A BETTER NAME
import psycopg2
from utils.fuzzyLandmarkSearch import fuzzyLandmarkSearch
from database.spatial_relations_functions import get_appropriate_relation_function

class GeoDAO:
    def init_connection(self):
        db_connection = psycopg2.connect(host='localhost', database='cg_geo', 
        user='postgres', password='elessar42')
        
        return db_connection

    def close_connection(self, db_connection):
        db_connection.close()

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
        connection = self.init_connection()
        cursor = connection.cursor()

        query = '''SELECT ST_Contains(ST_GeomFromGeoJSON('{}'),
                                    ST_GeomFromText('POINT(-35.8709436 -7.2322137)', 4326));''' \
                                    .format(acceptance_region)

        cursor.execute(query)
        contains = cursor.fetchall()[0][0]

        self.close_connection(connection)

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
