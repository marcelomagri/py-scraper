import schedule
import time
from bs4 import BeautifulSoup
import requests

# variáveis globais
items_to_scrape = 120
intervalo = 30
indices = range(0, items_to_scrape * 3 + 1, items_to_scrape)
paises = ['br', 'us']
googleplay_produtos = []

def msg():
    print("Oi")

def scrape():
    print("scraping...")

    url = "https://play.google.com/store/apps/category/GAME_WORD/collection/topselling_free?start=51&num=50&gl=%s"
    origem = requests.get(url % "br").text
    html = BeautifulSoup(origem, 'html.parser')
    produtos = html.find_all('div', {'class': ['card-content']})

    for produto in produtos:
        print(str(produto.attrs['data-docid']))
        titulo_produto = produto.find('a', {'class': ['title']}).text
        classificacao = str.replace(str.split(titulo_produto)[0], '.', '')
        detalhes_produto = [str(produto.attrs['data-docid']), classificacao, 'br']
        googleplay_produtos.append(detalhes_produto)

    time.sleep(15)

    origem = requests.get(url % "us").text
    html = BeautifulSoup(origem, 'html.parser')
    produtos = html.find_all('div', {'class': ['card-content']})

    for produto in produtos:
        print(str(produto.attrs['data-docid']))
        titulo_produto = produto.find('a', {'class': ['title']}).text
        classificacao = str.replace(str.split(titulo_produto)[0], '.', '')
        detalhes_produto = [str(produto.attrs['data-docid']), classificacao, 'us']
        googleplay_produtos.append(detalhes_produto)

    time.sleep(15)

schedule.every(5).seconds.do(msg)

while True:
    # schedule.run_pending()
    scrape()
    time.sleep(1)