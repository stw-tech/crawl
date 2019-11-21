from Bio import Entrez
import xmltojson
import json
import time
import os
import urllib

start_year = 1900
end_year = 2019
save_dir = 'E:/ssbi_dataset/pubmed_50'

def crawl(year, start_num):

    '''
    this function crawls the paper in pubmed dataset

    Args:
        start_num: the starting index of crawling data
        year: year
    '''

    Entrez.email = "luk2310405@gmail.com"
    time.sleep(1)
    handle = Entrez.esearch(db = "pubmed", term= '({}[Date - Publication] : {}[Date - Publication])'.format(year, year), usehistory = 'y')

    record = Entrez.read(handle)
    total_num = int(record['Count'])
    webenv = record['WebEnv']
    query_key = record["QueryKey"]

    batch_size = 50
    print('total num of crawling data: {}, finish crawled: {}, left crawled: {}'. format(total_num, start_num, total_num-start_num))
    if (total_num-start_num) != 0:

        print('>>> crawling data in {} year'.format(year))
        for start in range(start_num, total_num, batch_size):

            time.sleep(1)
            end = min(total_num, start + batch_size)
            print('total records: {}, downloading records {} to {} '.format(total_num, start+1, end))
            try:
                fetch_handle = Entrez.efetch(db = 'pubmed', retmode = 'xml', retstart = start, retmax = batch_size, webenv = webenv, query_key = query_key)
            except urllib.error.HTTPError :
                print(' HTTP Error 400: Bad Request')
                time.sleep(60)

            xml = fetch_handle.read()
            parse_json = xmltojson.parse(xml)
            data_dict = json.loads(parse_json)

            save_json(data_dict, year, start+1, end)
            fetch_handle.close()

def save_json(crawl_data, year, start, end):

    '''
    this function saves the json

    Args:
        crawl_data: The crawling of PubMed data
        year: year
        start: start index
        end: end index
    '''
    path = os.path.join(save_dir, str(year))

    if not os.path.exists(path):
        os.makedirs(path)

    save_json = json.dumps(crawl_data, indent=4, sort_keys = False, separators = (',', ':'))
    with open(os.path.join(path, str(start)+'~'+str(end)+'.json'), 'w', encoding='utf-8') as f:
        f.write(save_json)

def check_crawled(year):

    '''
    this function saves the json

    Args:
        year: year
    Returns:
        start_num: start index of crawling data
    '''
    
    print('>>> checking data in {} year is crawled or not'.format(year))
    ck_path = os.path.join(save_dir, str(year))

    if not os.path.exists(ck_path):
        start_num = 0
    else:
        crawled_id = os.listdir(ck_path)
        crawled_id.sort(key=lambda fn: os.path.getmtime(ck_path + '\\'+fn))
        latest_file = crawled_id[-1]

        start_num = int(latest_file.split('~')[1].replace('.json', ''))

    return start_num

if __name__ == "__main__":

    for year in range(end_year, start_year-1, -1):

        start_num = check_crawled(year)
        patent = crawl(year, start_num)
