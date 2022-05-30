
import requests
import json

# URL = "http://127.0.0.1:8000/stucrud/"
URL = "http://127.0.0.1:8000/api_view/"

#to retrive/read data from complex form database
def getData(id=None):
    data = {}
    if id is not None:
        data = {'id':id}
    json_data = json.dumps(data)  #from complex to json
    r = requests.get(url=URL, data=json_data)
    data = r.json()
    print(data)

# getData(2)
# getData()

# to create data(POST)

def post_data():
    data={
        'name':'jay',
        'roll': 104,
        'city': 'bhubneshvar'
    } # this is python data in the form of dictionary so have convert it into json form
    headers = {'content-type': 'application/json'}  # sollution of 'Unsupported media type "text/plain" in request.' error
    json_data = json.dumps(data)
    r = requests.post(url=URL, headers=headers, data=json_data)
    data = r.json()
    print(data)

post_data()

def update_data():
    data={
        'id': 3,
        'name':'romil',
        'city': 'kashi'
    }
    json_data = json.dumps(data)
    r = requests.put(url=URL, data=json_data) #for partial update use patch
    data = r.json()
    print(data)
update_data()

def delete_data():
    data={'id':3}
    json_data=json.dumps(data)
    r=requests.delete(url=URL, data=json_data) 
    data = r.json()
    print(data)
 
# delete_data()
