import sqlite3
import pandas as pd


def create_db():

    conn = sqlite3.connect('Data/speakings.db')

    cursor = conn.cursor()

    df = pd.read_csv('Greek_Parliament_Proceedings_1989_2020.csv')

    df.to_sql('parliament_data', conn)

    cursor.execute('''CREATE TABLE parliament_data (
                            _id INT AUTO_INCREMENT,
                            member_name TEXT,
                            sitting_date DATE,
                            parliamentary_period TEXT,
                            parliamentary_session TEXT,
                            parliamentary_sitting TEXT,
                            political_party TEXT,
                            government TEXT,
                            member_region TEXT,
                            roles TEXT,
                            member_gender TEXT,
                            speech TEXT,
                            PRIMARY KEY(_id)
                        )''')

    cursor.execute('''CREATE INDEX idx_member_name ON parliament_data(member_name)''')

    cursor.execute('''CREATE INDEX idx_speech ON parliament_data(speech)''')

    conn.commit()
    conn.close()


# create_db()
