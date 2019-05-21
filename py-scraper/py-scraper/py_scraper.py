import schedule
import time
from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime

# variáveis globais
items_to_scrape = 120
intervalo = 30
indices = range(0, items_to_scrape * 3 + 1, items_to_scrape)
paises = ['br', 'us']
googleplay_produtos = []

def msg():
    print("Oi")

def openConn():
    conn = sqlite3.connect('data/dados.db')
    cursor = conn.cursor()

    return conn, cursor

def closeConn(conn):

    conn.close()

def scrape():
    print("scraping...")

    db, cursor = openConn()

    for country_code in paises:
        for indice in indices:
            url = "https://play.google.com/store/apps/category/GAME_WORD/collection/topselling_free?start=%s&num=%s&gl=%s"
            origem = requests.get(url % (str(indice),items_to_scrape,country_code)).text
            html = BeautifulSoup(origem, 'html.parser')
            produtos = html.find_all('div', {'class': ['card-content']})

            for current, produto in enumerate(produtos):
                atual, descricao = str(current), str(produto.attrs['data-docid'])
                print('%s: %s', (atual, descricao))
                titulo_produto = produto.find('a', {'class': ['title']}).text
                classificacao = str.replace(str.split(titulo_produto)[0], '.', '')
                detalhes_produto = [str(produto.attrs['data-docid']), classificacao, 'br']
                googleplay_produtos.append(detalhes_produto)
                cursor.execute("INSERT INTO RAW_DATA (PACKAGE, DESCRIPTION, POSITION, ORIGIN, DATAHORA) VALUES ('%s', '%s', %s, 'br', '%s')" % (descricao, titulo_produto[titulo_produto.find('.  ') + 3:999], classificacao, str(datetime.datetime.utcnow())))
                db.commit()

            time.sleep(15)

            #origem = requests.get(url % (str(indice),items_to_scrape,"us")).text
            #html = BeautifulSoup(origem, 'html.parser')
            #produtos = html.find_all('div', {'class': ['card-content']})

            #for current, produto in enumerate(produtos):
            #    atual, descricao = str(current), str(produto.attrs['data-docid'])
            #    print('%s: %s', (atual, descricao))
            #    titulo_produto = produto.find('a', {'class': ['title']}).text
            #    classificacao = str.replace(str.split(titulo_produto)[0], '.', '')
            #    detalhes_produto = [str(produto.attrs['data-docid']), classificacao, 'us']
            #    googleplay_produtos.append(detalhes_produto)
            #    cursor.execute("INSERT INTO RAW_DATA (PACKAGE, DESCRIPTION, POSITION, ORIGIN, DATAHORA) VALUES ('%s', '%s', %s, 'us', '%s')" % (descricao, titulo_produto[titulo_produto.find('.  ') + 3:999], classificacao, str(datetime.datetime.utcnow())))
            #    db.commit()

            #time.sleep(15)

    closeConn(db)

schedule.every(5).minutes.do(msg)

while True:
    # schedule.run_pending()
    scrape()
    time.sleep(1)