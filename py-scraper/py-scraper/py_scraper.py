import schedule
import time
from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime
import json
#import http.server
#import socketserver

#carrega as configurações
with open('config.json') as config_file:
    config = json.load(config_file)

# variáveis globais
items_to_scrape = config['items_to_scrape']
intervalo = config['intervalo']
start_item = config['item_inicial']
indices = range(start_item, start_item + (items_to_scrape * 4), items_to_scrape)
paises = config['country_codes'].split(',')
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

            for ix in range(intervalo, 0, -1):
                print("Esperando por %i segundos antes de efetuar o novo request \r" % ix, end="")
                time.sleep(1)

            print("")

    closeConn(db)

# schedule.every(5).minutes.do(msg)

#PORT = 9090
#Handler = http.server.SimpleHTTPRequestHandler

#with socketserver.TCPServer(("", PORT), Handler) as httpd:
#    print("Serving at port", PORT)
#    httpd.serve_forever()

while True:
    # schedule.run_pending()
    for ix in range(config['delay'], 0, -1):
        print("Esperando por %i segundos antes de iniciar as capturas \r" % ix, end="")
        time.sleep(1)
    scrape()
    #qtd = 120
    #valores = range(0, 360, 120)
    #for val in valores:
    #    print(val)
    time.sleep(60)