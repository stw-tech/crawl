from Bio import Entrez
import xmltojson
import json
import time
import os

year = 2019

def crawl(year):

    Entrez.email = "luk2310405@gmail.com"
    handle = Entrez.esearch(db = "pubmed", term= '(2018[Date - Publication] : 2019[Date - Publication])', retmax = 100000, retstart = 0)
    record = Entrez.read(handle)
    total_num = int(record['Count'])

    start = 0
    batch_size = 100000

    while start < total_num :

        for start in range(0, total_num, batch_size):

            time.sleep(3)
            handle = Entrez.esearch(db="pubmed", term='({}[Date - Publication] : {}[Date - Publication])'.format(year, year), retmax = batch_size, retstart = start)
            record = Entrez.read(handle)
            id_list = record['IdList']

            for id in id_list:

                time.sleep(2)
                data = Entrez.efetch(db = "pubmed", id = id, retmode = 'xml')
                xml = data.read()

                parse_json = xmltojson.parse(xml)
                data_dict = json.loads(parse_json)

                if data_dict['PubmedArticleSet'] != None:
                    save_json(data_dict, year)
                else:
                    print('Artice is None, id = {}'.format(id))
                # print('debug')


def save_json(crawl_data, year):

    try:
        id = crawl_data['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['PMID']['#text']
    except:
        id = crawl_data['PubmedArticleSet']['PubmedBookArticle']['BookDocument']['PMID']['#text']

    path = os.path.join('../data/', str(year), id)

    if not os.path.exists(path):
        os.makedirs(path)

    save_json = json.dumps(crawl_data, indent=4, sort_keys = False, separators = (',', ':'))
    with open(os.path.join(path, 'data.json'), 'w', encoding='utf-8') as f:
        f.write(save_json)


if __name__ == "__main__":


    patent = crawl(year)
