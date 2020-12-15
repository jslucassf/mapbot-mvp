import psycopg2

class ObjectDAO:
    def init_connection(self):
        db_connection = psycopg2.connect(host='localhost', database='cg_geo', 
        user='postgres', password='elessar42')
        
        return db_connection

    def close_connection(self, db_connection):
        db_connection.close()

    def run_insert(self, query):
        connection = self.init_connection()
        cursor = connection.cursor()

        cursor.execute(query)

        connection.commit()

        self.close_connection(connection)

    def run_query(self, query):
        connection = self.init_connection()
        cursor = connection.cursor()

        cursor.execute(query)

        result = cursor.fetchall()[0][0]

        self.close_connection(connection)

        return result