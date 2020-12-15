import psycopg2
from time import time
from database.objectDAO import ObjectDAO

class ConversationDAO(ObjectDAO):
    def conversation_started(self, conversation_id):
        query = '''SELECT id_chat
        FROM interaction
        ORDER BY timestamp DESC
        LIMIT 1;'''

        print(self.run_query(query))



    def insert_interaction(self, tracker, acceptance_region):
        conversation_id = tracker.sender_id
        user_message = tracker.latest_message['text']
        message_timestamp = time()

        self.conversation_started(conversation_id)

