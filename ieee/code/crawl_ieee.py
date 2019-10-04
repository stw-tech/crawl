import requests
import json
import time
import os
import random
from collections import Counter
from bs4 import BeautifulSoup
import re




start_year, end_year = 1975, 2017
paper_type = ['conference', 'journal']

start_page = 1
request_url = 'https://ieeexplore.ieee.org/rest/search'
headers = {
    'Host': 'ieeexplore.ieee.org',
    'Content-Type': 'application/json',
    'Referer':'https://ieeexplore.ieee.org/rest/search',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

payload = {
            "action":"search",
            "searchWithin": ["\"Publication Title\":{}", "\"Publication_Year\":{}"],
            "highlight":True,
            'rowsPerPage': 100,
            'pageNumber': start_page,
            "returnFacets":["ALL"],
            "returnType":"SEARCH",
            "newsearch": True,
            "sortType": "newest"
           }

proxy_list = ['104.236.248.219:3128', '167.71.249.181:8888']

def crawl_ieee(paper_list, p_type, year):

    print(">>> crawling {} {} paper".format(year, p_type))
    for id in paper_list:

        doc_link = 'https://ieeexplore.ieee.org/document/' + id

        while True:
            try:
                time.sleep(1)
                proxies = get_proxies()
                doc_res = requests.get(doc_link, proxies = proxies)

            except requests.exceptions.ConnectionError:
                print('requests.exceptions.ConnectionError: stop for 60s ')
                time.sleep(30)
                continue
            break

        html_txt = doc_res.text
        soup = BeautifulSoup(html_txt, 'lxml')
        # print(soup.prettify())
        tag = soup.find_all('script', type="text/javascript", src ='')

        for t in tag  :

            metadata_format = re.compile(r'global.document.metadata=.*', re.MULTILINE)
            metadata = re.findall(metadata_format, t.text)
            metadata = [mt.strip() for mt in metadata]

            if len(metadata) != 0 :

                try:
                    metadata = metadata[0][:-1].replace('global.document.metadata=', '')
                    metadata_dict = json.loads(metadata)
                    if metadata_dict != None:
                        save_json(metadata_dict, p_type, year)
                    else:
                        print('meta_data is None')
                except json.decoder.JSONDecodeError:
                    print('metadata decode error')

    print('finishing crawling')


def save_json(crawl_data, p_type, year):

    try:
        path = os.path.join('../data/', p_type, str(year), crawl_data['articleNumber'])
    except TypeError:
        print('crawl data type error')

    if not os.path.exists(path):
        os.makedirs(path)

    save_json = json.dumps(crawl_data, indent=4, sort_keys = False, separators = (',', ':'))
    with open(os.path.join(path, 'data.json'), 'w', encoding='utf-8') as f:
        f.write(save_json)

def check_crawled(p_type, year):

    print('>>> checking {} {} paper'.format(year, p_type))
    payload['pageNumber'] = start_page
    payload['searchWithin'] = ["\"Publication Title\":{}".format(p_type), "\"Publication_Year\":{}".format(year)]

    ck_dir = '../data'
    ck_path = os.path.join(ck_dir, p_type, str(year))

    if not os.path.exists(ck_path):
        crawled_paper = []
    else:
        crawled_paper = os.listdir(ck_path)
    while True:
        try:
            proxies = get_proxies()
            res = requests.post(url=request_url, data=json.dumps(payload), headers=headers, proxies = proxies)
            total_num = res.json()['totalRecords']
            total_page = res.json()['totalPages']
        except json.decoder.JSONDecodeError:
            print('json decode error')
            continue
        break

    if len(crawled_paper) < total_num:
        total_paper = []
        while payload['pageNumber'] <= total_page:

            while True:
                try:
                    time.sleep(random.uniform(2, 6))
                    proxies = get_proxies()
                    res = requests.post(url=request_url, data=json.dumps(payload), headers=headers, proxies = proxies)
                    res_json = res.json()
                    paper_per_page = len(res_json['records'])
                except json.decoder.JSONDecodeError:
                    print('json decode error')
                    time.sleep(60)
                    continue
                except KeyError:
                    print('KeyError')
                    time.sleep(60)
                    continue
                break

            for idx in range(paper_per_page):
                paper = res_json['records'][idx]
                paper_id = paper['articleNumber']
                total_paper.append(paper_id)

            payload['pageNumber'] += 1

        paper_list = list(set(total_paper) - set(crawled_paper))
        print('total num of crawling data :{}, finish crawling: {}, need to be crawled: {}'.format(len(total_paper), len(crawled_paper), len(paper_list)))

    else:
        print('Don\'t need to update')
        paper_list = []
    return paper_list

def get_proxies():

    index = random.randint(0, len(proxy_list) - 1)
    proxies = {'https': proxy_list[index]}

    return proxies
if __name__ == "__main__":

    for type in paper_type:

        for year in range(end_year, start_year-1, -1):
            paper_list = check_crawled(type, year)
            if len(paper_list) != 0:
                crawl_ieee(paper_list, type, year)