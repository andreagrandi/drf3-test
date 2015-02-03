import requests
import json
import os

# Set the env variable DRFTEST_TOKEN before using this script
token = os.environ['DRFTEST_TOKEN']

auth_header = {'Authorization': 'Token ' + token}
base_url = 'http://drf3test.herokuapp.com/shop/'

def place_order():
    data = [{"product": 1, "quantity": 26}, {"product": 2, "quantity": 30}]
    r = requests.post(base_url + 'orders/', data=json.dumps(data), headers = auth_header)
    print r.content

def get_stamps():
    r = requests.get(base_url + 'stamps/', headers = auth_header)
    print r.content

def get_vouchers():
    r = requests.get(base_url + 'vouchers/', headers = auth_header)
    print r.content
