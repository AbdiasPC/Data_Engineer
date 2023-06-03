import json
import requests
import pandas as pd

url = 'https://jsonplaceholder.typicode.com/'

""" List of endpoints

/posts	    100 posts
/comments	500 comments
/albums	    100 albums
/photos	    5000 photos
/todos	    200 todos
/users	    10 users
"""
#endpointsList = ['posts','comments','albums','photos','todos','users']

def _connect_api(host: str, endpoint: str) -> bool:
    url = host + endpoint
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
            raise ValueError('Connection failed')
    except requests.exceptions.RequestException as e:
        print("Message: ", e.message)
        print("Args: ", e.args)
    
def get_data(host: str = 'https://jsonplaceholder.typicode.com/', endpoint: str = '') -> list:
    if _connect_api(host= host, endpoint= endpoint):
        url = host + endpoint
        response = requests.get(url)
        return response.json()

def extractData():
    endpointsList = ['posts','comments','albums','photos','todos','users']
    for endpoint in endpointsList:
        data = get_data(endpoint= endpoint)
        with open('./data/'+endpoint+'.json', 'w', encoding='utf') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def create_users_table():
    df_user = pd.DataFrame(columns=['id','name','username','email','phone','website'])
    with open('./data/users.json') as f:
        json_users = json.load(f)
        for user in json_users:
            new_keys = ['id','name','username','email','phone','website']
            new_dic = {key: user[key] for key in new_keys}
            df_dic = pd.DataFrame([new_dic])
            df_user = pd.concat([df_user, df_dic], ignore_index=True)
        print(df_user.sample(5))
        
def create_user_address_table():
    df_address = pd.DataFrame(columns=['street','suite','city','zipcode','user_id','lat','lng'])
    with open('./data/users.json') as f:
        json_address = json.load(f)
        for adress in json_address:
            info = adress['address']
            new_keys = ['street','suite','city','zipcode']
            new_dic = {key: info[key] for key in new_keys}
            new_dic['userId'] = str(adress['id'])
            new_dic['lat'] = adress['address']['geo']['lat']
            new_dic['lng'] = adress['address']['geo']['lng']
            df_dic = pd.DataFrame([new_dic])
            df_address = pd.concat([df_address, df_dic], ignore_index=True)
        df_address = df_address[['userId','street','suite','city','zipcode','lat','lng']]
        print(df_address.sample(5))
        
def create_todos_table():
    df_todos = pd.DataFrame(columns=['userId','id','title','completed'])
    with open('./data/todos.json') as f:
        json_todos = json.load(f)
        for todo in json_todos:
            df_dic = pd.DataFrame([todo])
            df_todos = pd.concat([df_todos, df_dic], ignore_index=True)
        print(df_todos.sample(5))
        
def create_albums_table():
    df_albums = pd.DataFrame(columns=['userId','id','title'])
    with open('./data/albums.json') as f:
        json_albums = json.load(f)
        for album in json_albums:
            df_dic = pd.DataFrame([album])
            df_albums = pd.concat([df_albums, df_dic], ignore_index=True)
        print(df_albums.sample(5))

if __name__ == '__main__':
    # -- Extract data from all endpoints: posts, comments, albums, photos, todos and users -- #
    #extractData()
    
    # -- create users dataframe -- #
    print('USERS TABLE:')
    create_users_table()
    print('\n')
    
    # -- create todos dataframe -- #
    print('TODOS TABLE:')
    create_todos_table()
    print('\n')
            
    # -- create albums dataframe -- #
    print('ALBUMS TABLE:')
    create_albums_table()
    print('\n')
    
    # -- create address dataframe -- #
    print('ADDRESS TABLE:')
    create_user_address_table()
    print('\n')
