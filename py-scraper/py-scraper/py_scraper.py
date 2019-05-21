import schedule
import time
from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime

# variáveis globais
items_to_scrape = 100
intervalo = 30
start_item = 0
indices = range(start_item, start_item + (items_to_scrape * 4), items_to_scrape)
paises = ['pt'] #'br', 'us'
googleplay_produtos = []

def msg():
    print("Oi")

def openConn():
    conn = sqlite3.connect('data/dados.db')
    cursor = conn.cursor()

    return conn, cursor

def closeConn(conn):

    conn.close()

def repeat_to_length(string_to_expand, length):
   return (string_to_expand * ((length/len(string_to_expand))+1))[:length]

def scrape():
    print("scraping...")

    db, cursor = openConn()

    for country_code in paises:
        for indice in indices:
            #url = "https://play.google.com/store/apps/category/GAME_WORD/collection/topselling_free?start=%s&num=%s&gl=%s"
            url = "https://play.google.com/store/apps/category/GAME_WORD/collection/topselling_free"
            print("Capturando %s" % url)
            #origem_raw = requests.get(url % (str(indice),items_to_scrape,country_code), headers = {'User-agent': 'appai bot 0.1'})
            origem_raw = requests.post(url, {"start":str(indice), "num":str(items_to_scrape), "xhr":"1", "numChildren":"0", "gl": country_code})

            if origem_raw.status_code != 200:
                print("Erro: %s" % str(origem_raw.status_code))
            origem = origem_raw.text
            html = BeautifulSoup(origem, 'html.parser')
            produtos = html.find_all('div', {'class': ['card-content']})

            for current, produto in enumerate(produtos):
                atual, descricao = str(current), str(produto.attrs['data-docid'])
                print(str(current + indice))
                # print('%s: %s', (atual, descricao))
                titulo_produto = str.replace(produto.find('a', {'class': ['title']}).text, '\'', '\'\'')
                classificacao = str.replace(str.split(titulo_produto)[0], '.', '')
                detalhes_produto = [str(produto.attrs['data-docid']), classificacao, 'br']
                googleplay_produtos.append(detalhes_produto)
                cursor.execute("INSERT INTO RAW_DATA (PACKAGE, DESCRIPTION, POSITION, ORIGIN, DATAHORA) VALUES ('%s', '%s', %s, '%s', '%s')" % (descricao, titulo_produto[titulo_produto.find('.  ') + 3:999], classificacao, country_code, str(datetime.datetime.utcnow())))
                db.commit()

            for ix in range(180, 0, -1):
                print("Esperando por %i segundos antes de efetuar o novo request \r" % ix, end="")
                time.sleep(1)

            print("")

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

# schedule.every(5).minutes.do(msg)

while True:
    # schedule.run_pending()
    scrape()
    #qtd = 120
    #valores = range(0, 360, 120)
    #for val in valores:
    #    print(val)
    time.sleep(60)