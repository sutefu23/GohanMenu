import sys
import requests
import base64
import json

# insecure warning をオフ
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 1レコード
class FileMakerRecord:
    def __init__(self, dic):
        self.fieldData = dic["fieldData"]
        self.recordId = dic["recordId"]

# データベース関数
class FileMakerDB:
    def __init__(self, filename, username, password):
        self.baseURL = f"https://192.168.1.153/fmi/data/v1/databases/{filename}/"
        self.username = username
        self.password = password
        
    # セッションに対応するトークンを新規に生成する
    def prepareToken(self):
        session = requests.Session()
        self.session = session
        url = self.baseURL + "sessions"
        headers = {}
        headers["Authorization"] = "Basic " + base64.b64encode((self.username + ":" + self.password).encode()).decode("ascii")
        headers["Content-Type"] = "application/json"
        response = session.post(url, headers=headers, json={}, verify=False)
        json = response.json()
        token = json["response"]["token"]
        self.token = token
        return token

    # テーブルの内容をすべて取得する
    def fetch(self, layout):
        result = []
        token = self.token
        if not token:
            return result
        session = self.session
        offset = 1
        limit = 100
        while True:
            url = f"{self.baseURL}layouts/{layout}/records?_offset={offset}&_limit={limit}"
            headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
            response = session.get(url, headers=headers, verify=False)
            json = response.json()
            if not json["response"]:
                break
            data = json["response"]["data"] 
            for dic in data:
                record = FileMakerRecord(dic)
                result.append(record)
            count = len(data)
            if count < limit:
                break
            offset += count
        return result
        
    # テーブルに絞り込み検索をかける
    def find(self, layout, query):
        result = []
        token = self.token
        if not token:
            return result
        session = self.session
        offset = 1
        limit = 100
        url = f"{self.baseURL}layouts/{layout}/_find"
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
        while True:
            request = json.dumps({"query": query, "offset": offset, "limit": limit}, ensure_ascii=False)
            response = session.post(url, headers=headers, data=request.encode("utf-8"), verify=False)
            res = response.json()
            if not res["response"]:
                break
            data = res["response"]["data"] 
            for dic in data:
                record = FileMakerRecord(dic)
                result.append(record)
            count = len(data)
            if count < limit:
                break
            offset += count
        return result       
    
    #レコードを削除する
    def delete(self, layout, recordID):
        token = self.token
        if not token:
            return 
        session = self.session
        url = f"{self.baseURL}layouts/{layout}/records/{recordID}"        
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
        session.delete(url, headers=headers)
        
    #レコード内容を更新する
    def update(self, layout, recordID, fields):
        token = self.token
        if not token:
            return 
        session = self.session
        url = f"{self.baseURL}layouts/{layout}/records/{recordID}"   
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
        update = json.dumps({"fieldData": fields}, ensure_ascii=False)
        session.patch(url, headers=headers, data=update.encode("utf-8"), verify=False)
      
    #レコードを新規登録する
    def insert(self, layout, fields):
        token = self.token
        if not token:
            return 
        session = self.session
        url = f"{self.baseURL}layouts/{layout}/records"   
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
        update = json.dumps({"fieldData": fields}, ensure_ascii=False)
        response = session.post(url, headers=headers, data=update.encode("utf-8"), verify=False)
        res = response.json()
        return res["response"]["recordId"] 
        
    #サーバースクリプトを実行する
    def executeScript(self, layout, script, param):
        token = self.token
        if not token:
            return 
        session = self.session
        url = f"{self.baseURL}layouts/{layout}/records?script={script}&script.param={param}"   
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
        session.get(url, headers=headers, verify=False)
        
# 生産管理DB
pm_osakaname = FileMakerDB("pm_osakaname", "api", "@pi")
# 補助DB
system = FileMakerDB("system", "admin", "ws161")

#test
#db_main.prepareToken()
#result = db_main.find("DATAAPI_8", [{"社員番号": "023"}])
#print(result[0].fieldData)

