import boto3
import json
import glob
from tqdm import tqdm
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ieee')
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

for ieee_data in tqdm(glob.glob("./data/*/*/*/*.json")):
    try:
        with open(ieee_data , 'r',encoding = 'utf-8') as reader:
            jf = json.loads(reader.read())
        try:
            k = _ToDateTime((jf["journalDisplayDateOfPublication"]))
        except:
            k = None
        try:
            s = _ToNull(jf["sponsors"])
        except:
            s = None
        try:
            v = _ToNull(jf["volume"])
        except:
            v = None
        try:
            xplore = _ToNull(jf["xploreDocumentType"])
        except:
            xplore = None
        try:
            authors = _ToNull(jf["authors"])
        except:
            authors = None
        try:
            keywords = _ToNull(jf["keywords"])
        except:
            keywords = [
                {
                "kwd": [
                    "None"
                ],
                "type": "None"
                }
            ]
        try:
            abstract = _ToNull(jf["abstract"])
        except:
            abstract = None
        try:
            title = _ToNull(jf["title"])
        except:
            title = None
        try:
            articleId = _ToNull(jf["articleId"])
        except:
            articleId = None
        try:
            articleNumber = _ToNull(jf["articleNumber"])
        except:
            articleNumber = None
        try:
            content_type = _ToNull(jf["content_type"])
        except:
            content_type = None
        try:
            contentType = _ToNull(jf["contentType"])
        except:
            contentType = None
        try:
            htmlAbstractLink = _ToNull(jf["htmlAbstractLink"])
        except:
            htmlAbstractLink = None
        try:
            onlineDate = _ToDateTime((jf["onlineDate"]))
        except:
            onlineDate = None
        try:
            pdfUrl = _ToNull(jf["pdfUrl"])
        except:
            pdfUrl = None
        try:
            persistentLink = _ToNull(jf["persistentLink"])
        except:
            persistentLink = None
        try:
            publicationTitle = _ToNull(jf["publicationTitle"])
        except:
            publicationTitle = None
        try:
            publicationYear = _ToNull(jf["publicationYear"])
        except:
            publicationYear = None
        try:
            publisher = _ToNull(jf["publisher"])
        except:
            publisher = None
        try:
            rightsLink = _ToNull(jf["rightsLink"])
        except:
            rightsLink = None
        try:
            standardTitle = _ToNull(jf["standardTitle"])
        except:
            standardTitle = None
        try:
            subType = _ToNull(jf["subType"])
        except:
            subType = None
        table.put_item(
        Item={
                "abstract": abstract,
                "articleId": articleId,
                "articleNumber": articleNumber,
                "authors": authors,
                "content_type":  content_type,
                "contentType":  contentType,
                "htmlAbstractLink":  htmlAbstractLink,
                "journalDisplayDateOfPublication": k,
                "keywords":  keywords,
                "lastupdate":  _ToNull(jf["lastupdate"]),
                "onlineDate":  onlineDate,
                "pdfUrl":  pdfUrl,
                "persistentLink": persistentLink,
                "publicationTitle":  publicationTitle,
                "publicationYear":  publicationYear,
                "publisher":  publisher,
                "rightsLink":  rightsLink,
                "sponsors":  s,
                "standardTitle":  standardTitle,
                "subType":  subType,
                "xploreDocumentType": xplore,
                "volume":  v,
                "title":  title
            }
        )
    except Exception as e:
        print(e)
        #print(ieee_data)
        #fail.append(ieee_data+'\n')
    
fp = open("fail.txt", "a")
# 將 lines 所有內容寫入到檔案

fp.writelines(fail)
        
# 關閉檔案
fp.close()
