import random
import string
from typing import Optional, List, Union
from langchain.schema import HumanMessage, AIMessage


def get_user_id_by_api_key(db_connection, api_key: str) -> Optional[str]:
    cursor = db_connection.cursor()
    cursor.execute("SELECT id FROM User WHERE key=?", (api_key,))
    result = cursor.fetchone()
    return result[0] if result else None


def re_initialize_db(connection):
    connection.execute('''CREATE TABLE IF NOT EXISTS User
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  key TEXT)''')

    connection.execute('''CREATE TABLE IF NOT EXISTS Message
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  user_id INTEGER,
                  sender TEXT CHECK (sender IN ('user', 'AI')),
                  text TEXT,
                  FOREIGN KEY (user_id) REFERENCES User(id))''')

    connection.commit()


def register_new_api_key(db_connection) -> str:
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    db_connection.execute('INSERT INTO User (key) VALUES (?)', (key,))
    db_connection.commit()
    return key


def get_user_api_keys(db_connection) -> List[str]:
    cursor = db_connection.execute('SELECT key FROM User')

    return [r[0] for r in cursor]


def add_user_message(db_connection, user_id: int, message_text: str):
    cursor = db_connection.cursor()
    cursor.execute(
        """
        INSERT INTO Message (user_id, sender, text)
        VALUES (?, 'user', ?)
        """,
        (user_id, message_text)
    )
    db_connection.commit()


def add_ai_message(db_connection, user_id: int, message_text: str):
    cursor = db_connection.cursor()
    cursor.execute(
        """
        INSERT INTO Message (user_id, sender, text)
        VALUES (?, 'AI', ?)
        """,
        (user_id, message_text)
    )
    db_connection.commit()


def save_to_chat_history(db_connection, messages: List[Union[HumanMessage, AIMessage]], user_id: int):
    for message in messages:
        if isinstance(message, HumanMessage):
            add_user_message(db_connection, user_id, message.content)
        elif isinstance(message, AIMessage):
            add_ai_message(db_connection, user_id, message.content)


def load_chat_history(db_connection, user_id: int) -> List[Union[HumanMessage, AIMessage]]:
    cursor = db_connection.cursor()
    cursor.execute(
        """
        SELECT Message.sender, Message.text
        FROM User
        JOIN Message
        ON User.id = Message.user_id
        WHERE User.id = ?
        ORDER BY Message.created_at
        """,
        (user_id,)
    )
    result = cursor.fetchall()

    chat_history = []
    for sender, text in result:
        if sender == 'user':
            chat_history.append(HumanMessage(content=text))
        elif sender == 'AI':
            chat_history.append(AIMessage(content=text))

    return chat_history
