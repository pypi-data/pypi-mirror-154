import pandas as pd
import uuid
import json, requests

url = 'https://http.msging.net/commands'

class Manager:
  def __init__(self, authorization):
     self.headers = {
                        'content-type': 'application/json',
                        'Authorization': fr'{authorization}'
                        }
     self.authorization = authorization         

  def import_combinations(self, df):
    mylist = self.make_request_body(df)
    for item in mylist:
        myrequest = requests.post(url, data=item ,headers=self.headers)
        print(myrequest.json())

  def get_combinations(self):
    body = {
            "id": 'aa89s7da-b4as85da8as87',
            "to": 'postmaster@ai.msging.net',
            "method": 'get',
            "uri": f'/content'  
          }

    z = requests.post(url, json=body,headers=self.headers)
    response = z.json()

    if response['resource']['items'] == []:
      return('Não existe conteúdo nessa base')
    else:
      return(response)

  def delete_combinations(self):
    response = self.get_combinations()
    id_list = []
    
    try:
        content_size = response['resource']['total']
    except:
        print('Não existe conteúdo nessa base')
    
    else:
        for i in range(content_size):
              id_list.append(response['resource']['items'][i]['id'])


        for x in id_list:
            print(x)
            body = {
                      "id":"e9df4092-54c5-4631-b367-be1f99f76d65",
                      "to":"postmaster@ai.msging.net",
                      "method":"delete",
                      "uri":f"/content/{x}"
                    }
            r = requests.post(url, json=body,headers=self.headers)
            response = r.json()
            

  def ca_body(self,title,resp,combinations):
      id = str(uuid.uuid4())

      if len(title) == 0:
        name = str(resp)[:47] + '...'
      else:  
        pass
     
      content =  {
                    "id": f"{id}",
                    "to": "postmaster@ai.msging.net",
                    "method": "set",
                    "uri": f"/content/{id}",
                    "type": "application/vnd.iris.ai.content-result+json",
                    "resource": {
                      "id": f"{id}",
                      "name": f"{title}",                   
                      "result": {"type": "text/plain", "content": f"{resp}"},
                      "combinations": combinations
                    }
                }
      
      return(content)


  def make_request_body(self, df):
      combs = []

      try:
        if df['from']:
          df = df['resource']['items']
        else:
          pass
      except: 
        pass

      try:
        for resp in df.text.squeeze().unique():
          question_combs = df[df.text.squeeze() == resp][['intent','entities']]
          combinations = [{"intent": question_combs.intent.tolist()[qc],"entities":question_combs.entities.tolist()[qc],"minEntityMatch": 1} for qc in range(len(question_combs))]
          try:
            name = df[df.text.squeeze() == resp].title.tolist()[0]
          except:
            name = ''
          combs.append(json.dumps(self.ca_body(name,resp,combinations)))
      except AttributeError:
        for comb in range(len(df)):
          combs.append((json.dumps(self.ca_body(df[comb]['result']['content'], df[comb]['combinations']))))
      return(combs)


  def backup(self):
    combs = self.get_combinations()

    with open('json_data.json', 'w') as outfile:
      json.dump(combs['resource']['items'], outfile)
    

    