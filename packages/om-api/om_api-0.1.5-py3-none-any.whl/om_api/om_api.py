import json
import requests
import pandas as pd

def make_request(request_type: str, url: str, cookie: dict, param: dict = ..., data: dict = ...):
    if param is ...:
        param = {}
    if data is ...:
        data = {}
    if request_type == 'get':
        response = requests.get(url, cookies=cookie, params=param)
    else:
        response = requests.post(url, cookies=cookie, params=param, data=data)

    id = str(response.json()["params"]["id"])
    responseToken = str(response.json()["params"]["responseToken"])
    monitoring_url = url+'/status/'+ id
    response = requests.get(monitoring_url, cookies=cookie)


    while response.json()['params']['status'] != 'SUCCESS':
        response = requests.get(monitoring_url, cookies=cookie)
        if response.json()['params']['status'] in ['FAILED', 'TIMED_OUT', 'REJECTED', 'REMOVED', 'CANCELED']:
            print('Request failed')
            break

    print(response.json()['params']['status'])
    
    response = requests.get(f'{url}/response/{id}?responseToken={responseToken}', cookies=cookie)
    return response


def DataFrame_to_List(data):
    list = []
    list.append(data.columns.to_list())
    list.append(data.values.tolist())
    return list


def get_properties(list_name: str, url: str, cookie: dict):
    """Возвращает список свойств справочника"""
    param = {"type": "list", # Тип источника multicube | om_multicube | list
         "name": list_name  # Название МК/справочника
        }
    response = make_request(url=url, request_type='get', cookie=cookie, param=param)
    row_data = response.json()['params']['data']['requestedData']
    return row_data[0][6:]

def get_list(list_name: str):
    """Возвращает справочник в формате DataFrame"""
    param = {"type": "list", # Тип источника multicube | om_multicube | list
         "name": list_name  # Название МК/справочника
        }
    response = make_request(request_type= 'get', param=param)
    row_data = response.json()['params']['data']['requestedData']
    data = pd.DataFrame(row_data[1:],
                        columns=row_data[0])
    return data


def get_parents(list_name: str):
    """Возвращает список парентов в справочнике"""
    data = get_list(list_name)
    parents = data.loc[data['Parent'].isna()==True]['Item Name']
    parents = parents.to_list()
    return parents


def get_items(list_name: str, parent: str = ...):
    data = get_list(list_name)
    if parent is ...:
        elements = data['Item Name']
    else:
        elements = data.loc[data['Parent'] == parent]['Item Name']
    elements = elements.to_list()
    return elements


def get_items_under_parent(list_name: str, parent: str):
    data = get_list(list_name)
    elements = data.loc[data['Parent'] == parent]['Item Name']
    elements = elements.to_list()
    return elements


def add_item_to_list(list_name: str, item_name: str, parent: str= ...):
    if parent is ... :
        data_json = {'Item Name': item_name}
        src_to_dest_column_map = {'Item Name': 'Item Name'}
    else:
        data_json = {'Item Name': item_name, 'Parent': parent}
        src_to_dest_column_map = {'Item Name': 'Item Name', 'Parent':'Parent'}
    param = json.dumps({
        "SRC": {
            "TYPE": 'OM_WEB_SERVICE_PASSIVE',
            "PARAMS": {
            }
        },
        "DEST": {
            "TYPE": 'LIST',
            "PARAMS": {
                "NAME": list_name,
                "TRANSFORM": {
                    "CHARSET": "UTF-8",
                    "SRC_TO_DEST_COLUMN_MAP": src_to_dest_column_map,
                    "DIMENSIONS": {
                    },
                    "CUSTOM_COLUMNS": [],
                    "SRC_COLUMN_PREPARE_DATA_MAP": {}
                },
            }
        },
        "DATA": [data_json]
    })
    response = make_request(request_type='post', data=param)
    
    return


def change_properties(list_name: str, item_name: str, properties: dict, parent: str = ...):
    if parent is ... :
        data_json = {'Item Name': item_name}
        src_to_dest_column_map = {'Item Name': 'Item Name'}
    else:
        data_json = {'Item Name': item_name, 'Parent': parent}
        src_to_dest_column_map = {'Item Name': 'Item Name', 'Parent':'Parent'}    
    for i in properties.keys():
        src_to_dest_column_map.update({i:i})
    data_json.update(properties)
    param = json.dumps({
        "SRC": {
            "TYPE": 'OM_WEB_SERVICE_PASSIVE',
            "PARAMS": {
            }
        },
        "DEST": {
            "TYPE": 'LIST',
            "PARAMS": {
                "NAME": list_name,
                "TRANSFORM": {
                    "CHARSET": "UTF-8",
                    "SRC_TO_DEST_COLUMN_MAP": src_to_dest_column_map,
                    "DIMENSIONS": {
                    },
                    "CUSTOM_COLUMNS": [],
                    "SRC_COLUMN_PREPARE_DATA_MAP": {}
                },
            }
        },
        "DATA": [data_json]
    })
    response = make_request(request_type='post', data=param)
    
    return 


def add_item_with_properties(list_name: str, item_name: str, properties: dict, parent: str = ...):
    if item_name in get_items(list_name):
        change_properties(list_name, item_name, properties, parent)
    else:
        add_item_to_list(list_name, item_name, parent)
        change_properties(list_name, item_name, properties, parent)