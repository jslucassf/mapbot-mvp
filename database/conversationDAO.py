import psycopg2
from time import time
from datetime import date
from database.objectDAO import ObjectDAO

class ConversationDAO(ObjectDAO):
    def conversation_started(self, conversation_id):
        query = '''SELECT id_chat
        FROM interaction
        ORDER BY timestamp DESC
        LIMIT 1;'''

        return self.run_query(query) == conversation_id

    def insert_interaction(self, tracker, acceptance_region):
        conversation_id = tracker.sender_id
        user_message = tracker.latest_message['text']

        if not self.conversation_started(conversation_id):
            insert_chat_query = '''INSERT INTO chat
            (id, date) VALUES
            ('{}', '{}')'''.format(conversation_id, date.today().strftime('%Y-%m-%d'))

            self.run_insert(insert_chat_query)

        query = '''INSERT INTO interaction
        (id_chat, timestamp, bot_message, user_message, acc_region) VALUES
        ('{}', {}, '{}', '{}', '{}'::geometry)'''.format(conversation_id, time(), tracker.latest_action_name, user_message, acceptance_region);

        self.run_insert(query)

