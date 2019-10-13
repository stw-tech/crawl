import boto3
import json
import glob
from tqdm import tqdm
from datetime import datetime


for pubmed_data in tqdm(glob.glob("./crawl/PubMed/example.json")):
    with open(pubmed_data , 'r',encoding = 'utf-8') as reader:
        jf = json.loads(reader.read())



dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ncbi')
fail =[]
def _ToDateTime(data):
    if(data == ""):
        return None
    else:
        time = datetime.strptime(data, "%d %B %Y")
        return time.strftime('%Y-%m-%d')
def _ToNull(data):
    if(data == ""):
        return None
    else:
        return data
def _ToString(data):
    if(data == None):
        return "Null"
    else:
        return data




for pubmed_data in tqdm(glob.glob("./newdata/*/*/*.json")):
    try:
        with open(pubmed_data , 'r',encoding = 'utf-8') as reader:
            jf = json.loads(reader.read())
        try:
            ArticleId = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['PubmedData']['ArticleIdList']['ArticleId'][0]['#text'])
            ArticleTitle = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle'])
            ArticleDate = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleDate'])
            AuthorList  = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Article']['AuthorList'])
            PublicationTypeList = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Article']['PublicationTypeList'])
            Journal = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Article']['Journal'])
            Language = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Article']['Language'])
            Abstract =  _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Abstract']['AbstractText'])
            '''
            if isinstance(_ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Abstract']['AbstractText']),str):
                Abstract =  _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Abstract']['AbstractText'])
            else if isinstance(_ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Abstract']['AbstractText']),str):
                Abstract =  _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Abstract']['AbstractText'])
            '''
        
        except:
            ArticleId = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][0]['PubmedBookData']['ArticleIdList']['ArticleId']['#text'])
            ArticleTitle = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][0]['BookDocument']['ArticleTitle']['#text'])
            ArticleDate = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][0]['BookDocument']['ContributionDate'])
            AuthorList  = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][0]['BookDocument']['AuthorList'])
            PublicationTypeList = None
            Journal = None
            Language = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][0]['BookDocument']['Language'])
            try:
                Abstract = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][0]['BookDocument']['Abstract']['AbstractText']['#text'])
            except:
                Abstract = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][0]['BookDocument']['Abstract']['AbstractText'])
        
        table.put_item(
            Item={
                "Abstract": Abstract,
                "ArticleDate": ArticleDate,
                "ArticleId": ArticleId,
                "ArticleTitle": ArticleTitle,
                "AuthorList": AuthorList,
                "Journal": Journal,
                "Language": Language,
                "PublicationTypeList": PublicationTypeList
            }
        )
    except:
        print(pubmed_data)
        fail.append(pubmed_data+'\n')
    
fp = open("fail.txt", "a")
# 將 lines 所有內容寫入到檔案

fp.writelines(fail)
        
# 關閉檔案
fp.close()