import requests
from bs4 import BeautifulSoup
import os
import json
import time
import re

start_date = [2019, 6, 1]
end_date = [2019, 6, 31]

start_page = 1

payload = {
            "Sect1": "PTO2",
            "Sect2": "HITOFF",
            "p": start_page,
            "u":"%2Fnetahtml%2FPTO%2Fsearch-adv.html",
            "r":0,
            "f":'S',
            "l":50,
            "d":"PG01",
            "Query":"PD%2F{}%2F{}%2F{}-%3E{}%2F{}%2F{}".format(start_date[1], start_date[2], start_date[0], end_date[1], end_date[2], end_date[0])
           }



def get_doc_num_and_title():

    count = 0
    patent = {}
    patent['doc_num'], patent['title'] = [], []

    while True:

        try:
            request_url = 'http://appft.uspto.gov/netacgi/nph-Parser?Sect1={Sect1}&Sect2={Sect2}&p={p}&u={u}' \
                          '&r={r}&f={f}&l={l}&d={d}&Query={Query}'.format(**payload)
            time.sleep(2)
            res = requests.get(url= request_url)
            html_txt = res.text
            soup = BeautifulSoup(html_txt, 'html.parser')
            tag = soup.select('tr > td > a')

            for content in tag :
                if count % 2 == 0:
                    patent['doc_num'].append(content.text)
                else:
                    name = content.text.replace('\n', '')
                    patent['title'].append(name)
                count += 1

            payload['p'] += 1
        except requests.exceptions.ConnectionError:
            break
        # print('debug')
    return patent

def crawl_patent(patent):

    crawled_info = {}

    payload = {
        "Sect1": "PTO1",
        "Sect2": "HITOFF",
        "p": 1,
        "u": "%2Fnetahtml%2FPTO%2Fsrchnum.html",
        "r": 1,
        "f": 'G',
        "l": 50,
        "d": "PG01",
        's1': "\"{}\".PGNR.",
        'OS': 'DN/{}',
        'RS': 'DN/{}'
    }
    idx = 0
    for id in patent['doc_num']:

        crawled_info[id] = {}
        crawled_info[id]['title'] = patent['title'][idx]

        payload['s1'] = "\"{}\".PGNR.".format(id)
        payload['OS'] = "DN/{}".format(id)
        payload['RS'] = "DN/{}".format(id)

        request_url = 'http://appft.uspto.gov/netacgi/nph-Parser?Sect1={Sect1}&Sect2={Sect2}&d={d}&p={p}&u={u}' \
                      '&r={r}&f={f}&l={l}&s1={s1}&OS={OS}&RS={RS}'.format(**payload)
        time.sleep(3)
        res = requests.get(url=request_url)
        html_txt = res.text

        soup = BeautifulSoup(html_txt, 'lxml')
        print(soup.prettify())

        Publication_Number = soup.find_all('td', {'align': 'RIGHT', 'width': '50%'})[0].text.replace('\n', '')
        Publication_Date = soup.find_all('td', {'align': 'RIGHT', 'width': '50%'})[2].text.replace('\n', '')
        Application_Number = soup.find('td', text = re.compile('Appl. No.')).next_sibling.text.replace('\n', '')
        filing_date = soup.find('td', text = re.compile('Filed:')).next_sibling.text.replace('\n', '')

        crawled_info[id]['Publication_Number'] = Publication_Number
        crawled_info[id]['Application_Number'] = Application_Number
        crawled_info[id]['filing_date'] = filing_date
        crawled_info[id]['Publication_Date'] = Publication_Date

        tag = soup.select('center > b')
        for t in tag:
            if t.text == "Abstract" :

                p_tag = t.parent.next_sibling.next_sibling
                abstract = p_tag.text
                crawled_info[id][t.text] = abstract
                # print(abstract)
            if t.text == "Claims":
                crawled_info[id][t.text] = ''
                p_tag = t.parent
                following = p_tag
                while True:

                    following = following.next_sibling
                    if str(following) == '<br/>' or str(following) == '\n' or str(following) == '<hr/>' :
                        # print('<hr/>')
                        continue
                    if str(following) == "<center><b><i>Description</i></b></center>":
                        break
                    else:
                        crawled_info[id][t.text] += following

        save_json(crawled_info[id])
        idx += 1
        print('de')


    return crawled_info


def save_json(crawl_data):

    start = ['0'+ str(i) if i < 10 else str(i) for i in start_date ]
    end = ['0'+ str(i) if i < 10 else str(i) for i in end_date ]
    dir_name = ''.join(start) + '-' + ''.join(end)
    path = os.path.join('../data', dir_name, crawl_data['Publication_Number'])

    if not os.path.exists(path):
        os.makedirs(path)

    save_json = json.dumps(crawl_data, indent=4, sort_keys = False, separators = (',', ':'))
    with open(os.path.join(path, 'data.json'), 'w', encoding='utf-8') as f:
        f.write(save_json)

if __name__ == "__main__":

    patent = get_doc_num_and_title()
    crawl_patent(patent)