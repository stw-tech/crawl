import requests
import json
import time
import os
import random
import datetime
from bs4 import BeautifulSoup
from util import map_name, b_code, b_acc_no
from itertools import product


date = datetime.datetime.now()
api_url = 'http://data.gcis.nat.gov.tw/od/data/api/'
crawled_items = [6] # api 6, 13, 15, 24~28, 31~39, 41~48
skip_limit = 500000
total_para = {
            # total parameters should be feeded
            'format': ['json'],
            'Business_Accounting_NO': b_acc_no,
            'Business_Current_Status' : ['01', '02', '03', '04', '05', '06', '07', '08', '09'],
            'Business_Register_Funds' : ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            'Business_Item': b_code['ALL'],
            'Business_Item_A': b_code['A'],
            'Business_Item_B': b_code['B'],
            'Business_Item_C': b_code['C'],
            'Business_Item_D': b_code['D'],
            'Business_Item_E': b_code['E'],
            'Business_Item_F': b_code['F'],
            'Business_Item_G': b_code['G'],
            'Business_Item_H': b_code['H'],
            'Business_Item_I': b_code['I'],
            'Business_Item_J': b_code['J'],
            'Business_Item_Z': b_code['Z'],
            'Company_Status' :  ['01'], # 01~33
            'Capital_Stock_Amount' : ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            'skip': [0],
            'top' : [1000]
             }

saving_dir = '../data'
def get_api_info():

    '''
    this function gets corresponding api_name, id, parameters, formula by crawling html

    Returns:
        api_dict : a dictionary with different api and corresponding api_name, id, parameters, formula
    '''

    Request_URL =  'https://data.gcis.nat.gov.tw/od/rule'

    res = requests.get(url = Request_URL)
    html_txt = res.text

    soup = BeautifulSoup(html_txt, 'html.parser')
    heading_tag = 'div.panel-heading label'     # tag of api id and name
    body_tag = 'div.panel-body '  # tag of api parameters

    header = soup.select(heading_tag)
    para_body = soup.select(body_tag + 'tr')

    api_dict = {}
    api_dict['id'], api_dict['name'], api_dict['para'], api_dict['formula'] = [], [], [], []

    idx = 0
    for state in header:
        api_dict['id'].append(state['for'])
        if idx < 9:
            api_dict['name'].append(state.text[2:])
        else :
            api_dict['name'].append(state.text[3:])
        idx += 1


    para_dic = {}
    for state in para_body:

        parameter = state.find('td').string[1:-1]
        para_dic[parameter] = None

        if parameter == 'top' :
            api_dict['para'].append(para_dic)
            para_dic = {}

    for state in soup.find_all('legend', text = 'API公式'):

        formula = str(state.next_sibling)
        formula = formula.replace('\r\n\t\t\t\t\t\t\t', '')
        api_dict['formula'].append(formula)

    return api_dict

def crawl_from_api(api):

    '''
    this function crawls the data from each api by feeding corresponding parameters

    Args:
        api: a dictionary with api's id, name, parameter, formula
    '''
    items = [i - 1 for i in crawled_items]

    for api_idx in items :

        para_idx = api_dict['para'][api_idx]
        name_idx = api_dict['name'][api_idx]

        feed_tmp = {}
        for para in para_idx.keys():
            if para in total_para.keys():
                feed_tmp[para] = total_para[para]

        para_idx_list = [dict(zip(feed_tmp.keys(), comb)) for comb in product(*(v for _, v in feed_tmp.items()))]

        for para_idx in para_idx_list:

            while para_idx['skip'] <= skip_limit:

                request_url = api['formula'][api_idx].format(**para_idx)

                while True:
                    try:
                        time.sleep(random.uniform(2, 10))
                        res = requests.get(url=request_url)
                    except requests.exceptions.ConnectionError:
                        print('Max retries exceeded with url')
                        time.sleep(60)
                        continue
                    break

                try:
                    x = res.json()
                    crawled_data = json.dumps(x, indent=4, sort_keys=False, ensure_ascii=False)
                    save_json(para_idx, name_idx, crawled_data)

                except json.decoder.JSONDecodeError:
                    print('the url is empty')
                    break

                para_idx['skip'] += para_idx['top']

def save_json(para, name, crawled_data):

    '''
    this function is to save json

    Args:
        para: a dictionary with the parameters of coressponding api should be feeded
        name: the name of the crawling api(str)
        crawled_data: the crawled data(str)
    '''

    excluded_fields = ('format', 'top', 'skip')
    save_keys = [k for k in para.keys() if k not in excluded_fields]

    dir_name = []

    for key in save_keys :
       k_name = map_name(key, para)
       dir_name.append(k_name)

    path = '/'.join(dir for dir in dir_name)
    json_path = os.path.join(saving_dir, name, path)

    if not os.path.exists(json_path):
        os.makedirs(json_path)

    file_name = '{}~{}.json'.format(para['skip'] + 1, para['skip'] + para['top'])
    with open(os.path.join(json_path, file_name), 'w', encoding='utf-8') as f:
        f.write(crawled_data)

if __name__ == "__main__":

    api_dict = get_api_info()
    crawl_from_api(api_dict)

