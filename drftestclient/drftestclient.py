import requests
import json
import os

class ShopClient(object):
    def __init__(self, base_url='http://drf3test.herokuapp.com/shop/', *args, **kwargs):
        # Set the env variable DRFTEST_TOKEN before using this script
        self.token = os.environ['DRFTEST_TOKEN']
        self.auth_header = {'Authorization': 'Token ' + self.token}
        self.base_url = base_url

    def place_order(self, widget_quantity=1, gizmo_quantity=1):
        data = [{"product": 1, "quantity": widget_quantity},
                {"product": 2, "quantity": gizmo_quantity}]
        url = '{0}orders/'.format(self.base_url)

        r = requests.post(url, data=json.dumps(data), headers = self.auth_header)
        print r.content

    def get_stamps(self):
        url = '{0}stamps/'.format(self.base_url)
        r = requests.get(url, headers = self.auth_header)
        print r.content

    def get_vouchers(self):
        url = '{0}vouchers/'.format(self.base_url)
        r = requests.get(url, headers = self.auth_header)
        print r.content
