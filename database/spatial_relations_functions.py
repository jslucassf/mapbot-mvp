#import psycopg2
#db_connection = psycopg2.connect(host='localhost', database='cg_geo', 
#                                 user='postgres', password='elessar42')

#cursor = db_connection.cursor()

def front(reference_id, cursor):
    query = "SELECT front({})".format(reference_id)
    cursor.execute(query)
    return cursor.fetchall()[0]

def left_of(reference_id, cursor):
    query = "SELECT left_of({})".format(reference_id)
    cursor.execute(query)
    return cursor.fetchall()[0]

def right_of(reference_id, cursor):
    query = "SELECT right_of({})".format(reference_id)
    cursor.execute(query)
    return cursor.fetchall()[0]

def at_street(reference_id, cursor):
    query = "SELECT at_street({})".format(reference_id)
    cursor.execute(query)
    return cursor.fetchall()[0]

def next_to(reference_id, cursor):
    query = "SELECT next_to({})".format(reference_id)
    cursor.execute(query)
    return cursor.fetchall()[0]

def near(reference_id, cursor):
    query = "SELECT near({})".format(reference_id)
    cursor.execute(query)
    return cursor.fetchall()[0]

def between(reference_ids, cursor):
    reference_1_id, reference_2_id = reference_ids
    query = "SELECT in_between({}, {})".format(reference_1_id, reference_2_id)
    cursor.execute(query)
    return cursor.fetchall()[0]

def get_appropriate_relation_function(relation_name):
    spatial_relations = {
        "sr_front": front,
        "sr_left": left_of,
        "sr_right": right_of,
        "sr_at_street": at_street,
        "sr_next": next_to,
        "sr_near": near,
        "sr_between": between
    }

    return spatial_relations[relation_name]

#foo = spatial_relations["sr_between"]

#print(foo(1923, 3309, cursor))

#db_connection.close()