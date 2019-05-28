import sqlite3
import datetime

def openConn():
    conn = sqlite3.connect('data/dados.db')
    return conn

def closeConn(conn):

    conn.close()

# Grava um item capturado no banco de dados
def WriteItem(conn, descricao, titulo, classificacao, country_code):

    cursor = conn.cursor()

    cursor.execute("INSERT INTO RAW_DATA (PACKAGE, DESCRIPTION, POSITION, ORIGIN, DATAHORA) VALUES ('%s', '%s', %s, '%s', '%s')" % (descricao, titulo, classificacao, country_code, str(datetime.datetime.utcnow())))
    conn.commit()

    # closeConn(db)
