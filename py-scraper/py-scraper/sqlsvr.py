import pymssql

def openConn():
    conn = pymssql.connect(host="PRODAMBFC108691",
                           server="SQLEXPRESS",
                           port="4391",
                           user="usr-intel",
                           password="Lsm1103!!",
                           database="app-intel")
    return conn

def closeConn(conn):
    conn.close()

def return_countrycodes():
    conn = openConn()
    cursor = conn.cursor(as_dict=True)
    cursor.execute('SELECT COUNTRY_CODE FROM COUNTRY_CODES')
    cc = cursor.fetchall()
    closeConn(conn)
    return cc

def WriteItem(conn, cat_id, cc_sigla, fname, fgoogleurl, adescription, agoogleurl, apackage, aiconurl, position, rating):
    cursor = conn.cursor()
    cursor.callproc('p_ins_rank_data', (cat_id, cc_sigla, fname, fgoogleurl, adescription, agoogleurl, apackage, aiconurl, position, rating))
    conn.commit()
    return
