import boto3
import json
import glob
from tqdm import tqdm
from datetime import datetime


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



for pubmed_data in tqdm(glob.glob("./pubmed/*/*.json")):
    with open(pubmed_data , 'r',encoding = 'utf-8') as reader:
        jf = json.loads(reader.read())
        try:
            for i in range(len(jf["PubmedArticleSet"]['PubmedArticle'])):
                try:
                    ArticleId = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][i]['PubmedData']['ArticleIdList']['ArticleId'][0]['#text'])
                    try:
                        ArticleTitle = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][i]['MedlineCitation']['Article']['ArticleTitle'])
                    except:
                        ArticleTitle = None
                    try:
                        ArticleDate = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][i]['MedlineCitation']['Article']['ArticleDate'])
                    except:
                        ArticleDate = None
                    try:
                        AuthorList  = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][i]['MedlineCitation']['Article']['AuthorList'])
                    except:
                        AuthorList = None
                    try:
                        PublicationTypeList = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][i]['MedlineCitation']['Article']['PublicationTypeList'])
                    except:
                        PublicationTypeList = None
                    try:                    
                        Journal = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][i]['MedlineCitation']['Article']['Journal'])
                    except:
                        Journal = None
                    try:
                        Language = _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][i]['MedlineCitation']['Article']['Language'])
                    except:
                        Language = None
                    try:
                        Abstract =  _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][i]['MedlineCitation']['Abstract']['AbstractText'])
                    except:
                        Abstract = None
                    '''
                    if isinstance(_ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Abstract']['AbstractText']),str):
                        Abstract =  _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Abstract']['AbstractText'])
                    else if isinstance(_ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Abstract']['AbstractText']),str):
                        Abstract =  _ToNull(jf["PubmedArticleSet"]['PubmedArticle'][0]['MedlineCitation']['Abstract']['AbstractText'])
                    '''
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
                    print("pubmed_data_fail")
                    fail.append(pubmed_data+'_PubmedArticle'+str(i)+'\n')    
        except:
            print("no Article")
        try:    
            for i in range(len(jf["PubmedArticleSet"]['PubmedBookArticle'])):
                try:          
                    ArticleId = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][i]['PubmedBookData']['ArticleIdList']['ArticleId']['#text'])
                    try:
                        ArticleTitle = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][i]['BookDocument']['ArticleTitle']['#text'])
                    except:
                        ArticleTitle = None
                    try:
                        ArticleDate = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][i]['BookDocument']['ContributionDate'])
                    except:
                        ArticleDate = None
                    try:
                        AuthorList  = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][i]['BookDocument']['AuthorList'])
                    except:
                        AuthorList  = None
                    try:
                        PublicationTypeList = None
                    except:
                        PublicationTypeList = None
                    Journal = None
                    try:
                        Language = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][i]['BookDocument']['Language'])
                    except:
                        Language = None
                    try:
                        try:
                            Abstract = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][i]['BookDocument']['Abstract']['AbstractText']['#text'])
                        except:
                            Abstract = _ToNull(jf["PubmedArticleSet"]['PubmedBookArticle'][i]['BookDocument']['Abstract']['AbstractText'])
                    except:
                        Abstract = None
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
                    print("pubmedbook_data_fail")
                    fail.append(pubmed_data+'_PubmedBookArticle'+str(i)+'\n')
        except:
            print("No Book")
                
    
fp = open("fail.txt", "a")
# 將 lines 所有內容寫入到檔案

fp.writelines(fail)
        
# 關閉檔案
fp.close()
