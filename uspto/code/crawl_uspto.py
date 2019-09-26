import requests
from bs4 import BeautifulSoup
import os
import json
import time
import re

start_year = 2018
end_year = 2019

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
            "Query":"PD%2F{}%2F{}%2F{}-%3E{}%2F{}%2F{}"
           }



def get_doc_num_and_title():

    count = 0
    payload['p'] = start_page
    patent = {}
    patent['doc_num'], patent['title'] = [], []

    while True:

        try:
            request_url = 'http://appft.uspto.gov/netacgi/nph-Parser?Sect1={Sect1}&Sect2={Sect2}&p={p}&u={u}' \
                          '&r={r}&f={f}&l={l}&d={d}&Query={Query}'.format(**payload)
            time.sleep(0.5)
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

def crawl_patent(patent, year):

    crawled_info = {}

    num_payload = {
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
    for id in patent:

        crawled_info[id] = {}

        num_payload['s1'] = "\"{}\".PGNR.".format(id)
        num_payload['OS'] = "DN/{}".format(id)
        num_payload['RS'] = "DN/{}".format(id)

        request_url = 'http://appft.uspto.gov/netacgi/nph-Parser?Sect1={Sect1}&Sect2={Sect2}&d={d}&p={p}&u={u}' \
                      '&r={r}&f={f}&l={l}&s1={s1}&OS={OS}&RS={RS}'.format(**num_payload)
        time.sleep(1.5)
        res = requests.get(url=request_url)
        html_txt = res.text

        soup = BeautifulSoup(html_txt, 'lxml')
        # print(soup.prettify())

        title = soup.find('font', {'size': '+1'}).text.replace('\n', '')
        Publication_Number = soup.find_all('td', {'align': 'RIGHT', 'width': '50%'})[0].text.replace('\n', '')
        Publication_Date = soup.find_all('td', {'align': 'RIGHT', 'width': '50%'})[2].text.replace('\n', '')
        Application_Number = soup.find('td', text = re.compile('Appl. No.')).next_sibling.text.replace('\n', '')
        filing_date = soup.find('td', text = re.compile('Filed:')).next_sibling.text.replace('\n', '')
        Inventors = soup.find('td', text=re.compile('Inventors')).next_sibling.next_sibling.text.replace('\n', '')
        link = 'http://pdfaiw.uspto.gov/.aiw?Docid={}'.format(id)

        crawled_info[id]['title'] = title
        crawled_info[id]['Publication_Number'] = Publication_Number
        crawled_info[id]['Application_Number'] = Application_Number
        crawled_info[id]['filing_date'] = filing_date
        crawled_info[id]['Publication_Date'] = Publication_Date
        crawled_info[id]['Inventors'] = Inventors
        crawled_info[id]['link'] = link

        tag = soup.select('center > b')
        for t in tag:
            if t.text == "Abstract" :

                p_tag = t.parent.next_sibling.next_sibling
                abstract = p_tag.text
                crawled_info[id][t.text] = abstract

            if t.text == "Claims":
                crawled_info[id][t.text] = ''
                p_tag = t.parent
                following = p_tag
                while True:

                    following = following.next_sibling
                    if str(following) == '<br/>' or str(following) == '\n' or str(following) == '<hr/>' :
                        continue
                    if str(following) == "<center><b><i>Description</i></b></center>":
                        break
                    else:
                        crawled_info[id][t.text] += following

        save_json(crawled_info[id], year)
        idx += 1

        print('finish {}/{}'.format(idx, len(patent)))

    return crawled_info


def save_json(crawl_data, year):


    path = os.path.join('../newdata', str(year), crawl_data['Publication_Number'])

    if not os.path.exists(path):
        os.makedirs(path)

    save_json = json.dumps(crawl_data, indent=4, sort_keys = False, separators = (',', ':'))
    with open(os.path.join(path, 'data.json'), 'w', encoding='utf-8') as f:
        f.write(save_json)

def check_crawled(patent_id, year):

    print('>>> checking data is crawled or not')

    ck_dir = '../newdata'
    ck_path = os.path.join(ck_dir, str(year))

    crawled_id = os.listdir(ck_path)
    total_id = patent_id
    pantent_id_list = list(set(total_id) - set(crawled_id))

    print('total num of crawling data: {}, finish crawled: {}, left crawled: {}'. format(len(total_id), len(crawled_id), len(pantent_id_list)))

    return pantent_id_list

if __name__ == "__main__":

    for year in range(start_year, end_year+1):

        print(">>> crawl uspto data in {} year".format(year))
        payload['Query'] = "PD%2F{}%2F{}%2F{}-%3E{}%2F{}%2F{}".format(1, 1, year, 12, 31, year)
        patent = get_doc_num_and_title()
        pantent_id_list = check_crawled(patent['doc_num'], year)
        crawl_patent(pantent_id_list, year)
