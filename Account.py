import simplejson as json
import requests

class Account():
    def __init__(self, number):
        self.number = number
        self.balances = {}
        self.orders = []
        self.positions = []

    def get_access_token(self, refreshToken):
        self.response = requests.get('https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token=' + refreshToken)
        self.data = self.response.json()
        with open('token.json', 'w') as outfile:
            json.dump(self.data, outfile)
        print("Successfully grabbed access tokens")

    def get_account(self, accessed, refreshToken=0):
        if accessed =='N':
            self.get_access_token(refreshToken)
        with open('token.json') as json_file:
            data = json.load(json_file)
        # URL Data
        headers = {'Authorization' : data['token_type'] + ' ' + data['access_token']}

        balancesUrl = data['api_server'] + 'v1/accounts/51772572/balances'
        self.balances = requests.get(balancesUrl, headers=headers).json()
        ordersUrl = data['api_server'] + 'v1/accounts/51772572/orders'
        self.orders = requests.get(ordersUrl, headers=headers).json()
        positionsUrl = data['api_server'] + 'v1/accounts/51772572/positions'
        self.positions = requests.get(positionsUrl, headers=headers).json()

        with open('account.json', 'w') as outfile:
            outfile.write(json.dumps((self.balances, self.orders, self.positions), indent=4, sort_keys=True))

        
