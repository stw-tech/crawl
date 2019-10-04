import boto3
import json
import glob
from tqdm import tqdm
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ieee')
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
    # try:
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
        table.put_item(
        Item={
                "abstract": _ToNull(jf["abstract"]),
                "articleId": _ToNull(jf["articleId"]),
                "articleNumber": _ToNull(jf["articleNumber"]),
                "authors": _ToNull(jf["authors"]),
                "content_type":  _ToNull(jf["content_type"]),
                "contentType":  _ToNull(jf["contentType"]),
                "htmlAbstractLink":  _ToNull(jf["htmlAbstractLink"]),
                "journalDisplayDateOfPublication": k,
                "keywords":  _ToNull(jf["keywords"]),
                "lastupdate":  _ToNull(jf["lastupdate"]),
                "onlineDate":  _ToDateTime((jf["onlineDate"])),
                "pdfUrl":  _ToNull(jf["pdfUrl"]),
                "persistentLink":  _ToNull(jf["persistentLink"]),
                "publicationTitle":  _ToNull(jf["publicationTitle"]),
                "publicationYear":  _ToNull(jf["publicationYear"]),
                "publisher":  _ToNull(jf["publisher"]),
                "rightsLink":  _ToNull(jf["rightsLink"]),
                "sponsors":  s,
                "standardTitle":  _ToNull(jf["standardTitle"]),
                "subType":  _ToNull(jf["subType"]),
                "xploreDocumentType": xplore,
                "volume":  v,
                "title":  _ToNull(jf["title"])
               
                
            }
        )
    # except:
    #     print(ieee_data)
