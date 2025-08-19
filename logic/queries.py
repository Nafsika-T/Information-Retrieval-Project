import sqlite3
from flask import g

DATABASE = 'Data/speakings.db'


#This method returns an active connection to the SQLite database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#This method closes the connection to the database when it is no longer needed
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#This method returns a list of member names
def fetch_names_of_members():
    cursor = get_db().cursor()

    cursor.execute('SELECT DISTINCT member_name FROM parliament_data')

    result = cursor.fetchall()

    names = [name[0] for name in result if name[0] is not None]  #None in member_name means vouli

    return names


#This method returns a list of the names of political parties recorded in the database
def fetch_names_of_parties():
    cursor = get_db().cursor()

    cursor.execute('SELECT DISTINCT political_party FROM parliament_data')

    result = cursor.fetchall()

    names = [name[0] for name in result if name[0] is not None]  # None in member_name means vouli!

    return names

#This method returns the speeches of a specific member. There is an option to choose between the edited or the unedited form of the speech
def fetch_speeches_of_member(member_name: str, edited=True):
    cursor = get_db().cursor()

    if edited:
        query = """
            SELECT speech_edited, sitting_date 
            FROM parliament_data
            WHERE member_name = ? AND speech_edited != ''
        """
    else:
        query = """
                   SELECT speech, sitting_date 
                   FROM parliament_data
                   WHERE member_name = ? AND speech_edited != ''
               """

    cursor.execute(query, (member_name,))

    return cursor.fetchall()

#This method returns the speeches of a specific political party in their edited form, along with the date of the session
def fetch_speeches_of_party(party_name):
    cursor = get_db().cursor()

    query = """
        SELECT speech_edited, sitting_date 
        FROM parliament_data
        WHERE political_party = ? AND speech_edited != ''
    """

    cursor.execute(query, (party_name,))

    return cursor.fetchall()

#This method returns all the edited speeches
def fetch_all_speeches():
    cursor = get_db().cursor()

    cursor.execute('SELECT speech_edited FROM parliament_data')

    result = cursor.fetchall()

    data = [speech[0] for speech in result]  # its a list of tuples, extract the data from each tuple

    return data

#This method updates the database with the new edited speeches
def modify_speeches(speeches):
    cursor = get_db().cursor()

    data_to_update = [(speech, id_) for id_, speech in enumerate(speeches)]

    cursor.executemany("UPDATE parliament_data SET speech_edited = ? WHERE id = ?", data_to_update)

    get_db().commit()


#This method retrieves the details of a specific speech from the database based on the speech ID
def fetch_speech_details(doc_id):
    cursor = get_db().cursor()
    query = """
        SELECT id, member_name, political_party, sitting_date, speech
        FROM parliament_data
        WHERE id = ?
    """
    cursor.execute(query, (doc_id,))
    result = cursor.fetchone()

    if result:
        return {
            'id': result[0],
            'member_name': result[1],
            'political_party': result[2],
            'sitting_date': result[3],
            'speech': result[4]
        }
    else:
        return None
