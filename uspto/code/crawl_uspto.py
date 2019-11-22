import requests
from bs4 import BeautifulSoup
import os
import json
import time
import re
import threading
import random

start_year = 2001
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


headers = {
    'Referer':'http://appft.uspto.gov/netahtml/PTO/search-adv.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
}

updating_dir = '../updating_data/'
checking_dir = '../data'

def get_total_num(year):

    '''
    this function gets the total number of patents in year

    Args:
        year: the year of uspto patents

    Returns:
        total_num: the total number of patents in year
    '''

    payload['p'] = start_page
    payload['Query'] = "PD%2F{}%2F{}%2F{}-%3E{}%2F{}%2F{}".format(1, 1, year, 12, 31, year)

    while True:

        try:
            request_url = 'http://appft.uspto.gov/netacgi/nph-Parser?Sect1={Sect1}&Sect2={Sect2}&p={p}&u={u}' \
                          '&r={r}&f={f}&l={l}&d={d}&Query={Query}'.format(**payload)
            res = requests.get(url= request_url, headers = headers)
            html_txt = res.text
            soup = BeautifulSoup(html_txt, 'html.parser')
            tag = soup.select('i > strong ')

            total_num = int(tag[2].text)
        except requests.exceptions.ConnectionError :
            print('request error -> wait for 1 minute')
            time.sleep(60)
            continue
        break

    return total_num

def get_patent_num(year):

    '''
    this function crawls the total "patents id" by anaylsis the html code in year

    Args:
        year: the year of uspto patents

    Returns:
        patent_num: the total patent id list in this year
    '''

    print('>>> get document number in {} year'.format(year))

    count = 0
    payload['p'] = start_page
    patent_num = []
    payload['Query'] = "PD%2F{}%2F{}%2F{}-%3E{}%2F{}%2F{}".format(1, 1, year, 12, 31, year)

    while True:

        try:
            request_url = 'http://appft.uspto.gov/netacgi/nph-Parser?Sect1={Sect1}&Sect2={Sect2}&p={p}&u={u}' \
                          '&r={r}&f={f}&l={l}&d={d}&Query={Query}'.format(**payload)
            time.sleep(2)
            res = requests.get(url= request_url, headers = headers)
            html_txt = res.text
            soup = BeautifulSoup(html_txt, 'html.parser')
            tag = soup.select('tr > td > a')

            for content in tag :
                if count % 2 == 0:
                    patent_num.append(content.text)
                count += 1
            payload['p'] += 1
        except requests.exceptions.ConnectionError as error:
            if str(error) == '(\'Connection aborted.\', BadStatusLine(\'Error #2000\\n\',))':
                break
            else:
                print('request error -> wait for 1 minute')
                time.sleep(60)
                continue
    print('>>> finishing getting document number in {} year'.format(year))

    return patent_num

def crawl_patent(patent, year):

    '''
    this function crawls the patents information by anaylsis the html code

    Args:
        patent: the list of patents' id should be crawled
        year: the year of uspto patents
    '''

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
    print(">>> crawling uspto patent in {} year".format(year))

    for id in patent:

        crawled_info[id] = {}

        num_payload['s1'] = "\"{}\".PGNR.".format(id)
        num_payload['OS'] = "DN/{}".format(id)
        num_payload['RS'] = "DN/{}".format(id)

        request_url = 'http://appft.uspto.gov/netacgi/nph-Parser?Sect1={Sect1}&Sect2={Sect2}&d={d}&p={p}&u={u}' \
                      '&r={r}&f={f}&l={l}&s1={s1}&OS={OS}&RS={RS}'.format(**num_payload)
        while True:
            try:
                time.sleep(random.uniform(2, 3))
                res = requests.get(url=request_url, headers = headers)
            except requests.exceptions.ConnectionError:
                print('request Connection Error')
                time.sleep(60)
                continue
            break

        html_txt = res.text
        soup = BeautifulSoup(html_txt, 'lxml')

        title = soup.find('font', {'size': '+1'}).text.replace('\n', '')
        Publication_Number = soup.find_all('td', {'align': 'RIGHT', 'width': '50%'})[0].text.replace('\n', '')
        # below is to prevent the error when the html code different, but most following the same format
        try:
            Publication_Date = soup.find_all('td', {'align': 'RIGHT', 'width': '50%'})[2].text.replace('\n', '')
        except:
            Publication_Date = ''
        try:
            Application_Number = soup.find('td', text = re.compile('Appl. No.')).next_sibling.text.replace('\n', '')
        except:
            Application_Number = ''
        try:
            filing_date = soup.find('td', text = re.compile('Filed:')).next_sibling.text.replace('\n', '')
        except:
            filing_date = ''
        try:
            Inventors = soup.find('td', text=re.compile('Inventors')).next_sibling.next_sibling.text.replace('\n', '')
        except:
            Inventors = ''

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
                        try:
                            crawled_info[id][t.text] += following
                        except:
                            break

        save_json(crawled_info[id], year)
        idx += 1

        print('finish {}/{} in {} year'.format(idx, len(patent), year))


def save_json(crawl_data, year):

    '''
    this function saves crawling data into json

    Args:
        crawl_data: the crawling patents
        year: the year of uspto patents
    '''

    year_name = time.strftime("%Y", time.localtime())
    date_name = time.strftime("%m%d", time.localtime())
    path = os.path.join(updating_dir, year_name, date_name, 'PY' + str(year), crawl_data['Publication_Number'])

    if not os.path.exists(path):
        os.makedirs(path)

    save_json = json.dumps(crawl_data, indent=4, sort_keys = False, separators = (',', ':'))
    with open(os.path.join(path, 'data.json'), 'w', encoding='utf-8') as f:
        f.write(save_json)

def check_crawled(year):

    '''
    this function checks the patents crawled or not

    Args:
        year: the year of uspto patents

    Returns:
        id_list: the list of patents should be crawled
    '''

    print('>>> checking {} data is crawled or not'.format(year))

    ck_path = os.path.join(checking_dir, str(year))
    if not os.path.exists(ck_path):
        crawled_id = []
    else:
        crawled_id = os.listdir(ck_path)

    if os.path.exists(updating_dir):

        year_dir = os.listdir(updating_dir)
        for y in year_dir:
            y_path = os.path.join(updating_dir, y)
            for date in os.listdir(y_path):
                path = os.path.join(y_path, date, year)
                id = os.listdir(path)
                crawled_id.extend(id)

    total_num = get_total_num(year)
    if len(crawled_id) < total_num :
        total_id = get_patent_num(year)
        id_list = list(set(total_id) - set(crawled_id))
        print('total num of crawling data: {}, finish crawled: {}, left crawled: {}'.format(len(total_id), len(crawled_id), len(id_list)))
    else :
        id_list = []
        print('the patent in {} year don\'t need to update'.format(year))

    return id_list

if __name__ == "__main__":

    for year in range(end_year, start_year - 1, -1):

        patent_num = check_crawled(year)
        if patent_num:
            crawl_patent(patent_num, year)
