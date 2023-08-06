import requests, json
import pandas as pd
import numpy as np

url = 'https://http.msging.net/commands'

class Test:
    
    def __init__(self, authorization, input):
        self.headers = {
                        'content-type': 'application/json',
                        'Authorization': fr'{authorization}'
                        }
        if isinstance(input,list) or isinstance(input,pd.Series):
            self.input = list(input)
        elif isinstance(input,pd.DataFrame):   
            try:
                self.input = input.iloc[:,0]
                self.answer_expected = input.iloc[:,1]
            except:
                self.input = input.iloc[:,0]
        else:                
            print('Please send a list or DataFrame.')

    def test(self, text):

        body =  {
                    "id": "{{$guid}}",
                    "to": "postmaster@ai.msging.net",
                    "method": "set",
                    "uri": "/analysis",
                    "type": "application/vnd.iris.ai.analysis-request+json",
                    "resource": {
                    "text":f"{text}"
                    }
                }

        r = requests.post(url, json=body,headers=self.headers)
        return(r.json())


    def test_content(self,intention,entities):

        body =  {
                    "id": "46544651",
                    "to": "postmaster@ai.msging.net",
                    "method": "set",
                    "uri": "/content/analysis",
                    "resource": {
                    "intent": intention,
                    "entities":entities,
                    "minEntityMatch":1
                    },
                    "type": "application/vnd.iris.ai.content-combination+json"
                }
            
        r = requests.post(url, json=body,headers=self.headers)
        return(r.json())

    def run_test(self, blip_score=None):
        intentions =  []
        entities =  []
        score =  []
        content = []
        answer = []


        for item in self.input:
            result = self.test(item)
            
            try:
                i = str(result['resource']['intentions'][0]['id'])
                
                print(f'OK -> {item}')
                score.append(result['resource']['intentions'][0]['score'])
                i_name = str(result['resource']['intentions'][0]['id'])
                intentions.append(i_name)
                e = [str(result['resource']['entities'][x]['value']) for x in range(len(result['resource']['entities']))]
                entities.append(list(e))
            except:
                print(f'ERROR -> {item}')
                intentions.append('none')
                score.append('none')
                entities.append('none')
            try:
                print(str(i_name))
                c = self.test_content( str(i_name), e)['resource']['result']['content']
                answer.append(c)
                content.append('match')

            except:
             answer.append('None')
             content.append('no match')
        
        try:
          dft = pd.DataFrame({'Text':self.input,'Intention': intentions, 'Entities':entities, 'Score':score, 'Match':content, 'Answer':answer,'Sent':['y' if s >= blip_score else 'n' for s in score]})
        except:
          dft = pd.DataFrame({'Text':self.input,'Intention': intentions, 'Entities':entities, 'Score':score, 'Match':content, 'Answer':answer})

        return(dft)

