import schedule
import time
from bs4 import BeautifulSoup
import requests
import datetime
import json
from io import open as iopen
import my_sql as sqlOp
import sqlsvr as ssvr

#carrega as configurações
with open('config.json') as config_file:
    config = json.load(config_file)

# variáveis globais
items_to_scrape = config['items_to_scrape']
intervalo = config['intervalo']
start_item = config['item_inicial']
indices = range(start_item, start_item + (items_to_scrape * 4), items_to_scrape)
paises = ssvr.return_countrycodes() #config['country_codes'].split(',')
googleplay_produtos = []

def repeat_to_length(string_to_expand, length):
   return (string_to_expand * (int((length/len(string_to_expand))+1)))[:length]

def scrape():
    print("scraping...")

    conn = ssvr.openConn()

    for country_code in paises:
        for indice in indices:
            url = "https://play.google.com/store/apps/category/GAME_WORD/collection/topselling_free"
            
            origem_raw = requests.post(url, {"start":str(indice), "num":str(items_to_scrape), "xhr":"1", "numChildren":"0", "gl": country_code['COUNTRY_CODE']})

            print("Capturando %s" % (url))

            if origem_raw.status_code != 200:
                print("Erro: %s" % str(origem_raw.status_code))
            origem = origem_raw.text
            html = BeautifulSoup(origem, 'html.parser')
            produtos = html.find_all('div', {'class': ['card-content']})

            for current, produto in enumerate(produtos):
                atual, descricao = str(current), str(produto.attrs['data-docid'])
                print(str(current + indice))
                titulo_produto = str.replace(produto.find('a', {'class': ['title']}).text, '\'', '\'\'')
                classificacao = str.replace(str.split(titulo_produto)[0], '.', '')
                fabricante = str.replace(produto.find('a', {'class': ['subtitle']}).text, '\'', '\'\'')
                link_fabricante = str.replace(produto.find('a', {'class': ['subtitle']}).attrs['href'], '\'', '\'\'')
                detalhes_produto = [str(produto.attrs['data-docid']), classificacao, 'br']
                imagem_produto = str.replace(produto.find('img', {'class': ['cover-image']}).attrs['data-cover-small'], 'https:', '')
                if config['capturar_icones'] != 0:
                    imagem_produto_grande = requests.get('https:%s' % (str.replace(produto.find('img', {'class': ['cover-image']}).attrs['data-cover-small'], 'https:', '')))
                    if imagem_produto_grande.status_code == 200:
                        extensao = str.replace(imagem_produto_grande.headers['content-type'], 'image/', '')
                        with iopen("c:\\temp\\%s.%s" % (descricao, extensao), 'wb') as file:
                            file.write(imagem_produto_grande.content)
                googleplay_produtos.append(detalhes_produto)

                ssvr.WriteItem(conn, 2, country_code['COUNTRY_CODE'], fabricante, link_fabricante, titulo_produto[titulo_produto.find('.  ') + 3:999], titulo_produto, descricao, imagem_produto, classificacao, 5)

                #sqlOp.WriteItem(conn, descricao, titulo_produto[titulo_produto.find('.  ') + 3:999], classificacao, country_code)

            for ix in range(intervalo, 0, -1):
                print("Esperando por %i segundos antes de efetuar o novo request \r" % ix, end="")
                time.sleep(1)

            print("")

    #sqlOp.closeConn(conn)
    ssvr.closeConn(conn)

while True:
    for ix in range(config['delay'], -1, -1):
        if ix == 0:
            print("Iniciando capturas...  %s\r" % (repeat_to_length(' ', 40)) , end="")
        else:
            print("Esperando por %i segundos antes de iniciar as capturas \r" % ix, end="")
        time.sleep(1)
    scrape()
    time.sleep(60)