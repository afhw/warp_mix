import requests
import json


def getkey():
    ppkeys = requests.get('https://warp.halu.lu/')  # 还是大佬项目香！
    pkeys = ppkeys.content.decode('UTF8')
    new_data = json.loads(pkeys)
    # print(new_data)
    # print(new_data["key"])
    return new_data["key"]
