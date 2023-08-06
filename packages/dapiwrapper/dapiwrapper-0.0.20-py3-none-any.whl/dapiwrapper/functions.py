import requests

class Dapi:
    def __init__(self, stage):
        if stage == 'develop':
            self.url = "https://test-api.dcentralab.com/"
        if stage == 'staging':
            self.url = "https://staging-api.dcentralab.com/"

    def calculate_token_price_from_pair(self, key, pool, network, rpc_url=None):
        url = self.url + "calculateTokenPriceFromPair"
        headers = { 'X-API-KEY': key }
        data = {
            "network": network,
            "pool": pool,
            "rpc_url": rpc_url
        }
        response = requests.get(url, json=data, headers=headers)
        return response.json()

    def get_token_balance(self, key, user, token, network, rpc_url=None):
        url = self.url + "tokenBalance"
        headers = { 'X-API-KEY': key }
        data = {
            "network": network,
            "user": user,
            "token": token,
            "rpc_url": rpc_url
        }
        response = requests.get(url, json=data, headers=headers)
        return response.json()

    def get_token_balances_for_user(self, key, user, tokens : list, network, rpc_url=None):
        url = "https://test-api.dcentralab.com/tokenBalancesForUser"
        headers = { 'X-API-KEY': key }
        data = {
            "network": network,
            "user": user,
            "tokens": tokens,
            "rpc_url": rpc_url
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    
    def get_token_balance_for_users(self, key, users : list, token, network, rpc_url=None):
        url = self.url + "tokenBalanceForUsers"
        headers = { 'X-API-KEY': key }
        data = {
            "network": network,
            "users": users,
            "token": token,
            "rpc_url": rpc_url
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    
    def calculate_reserves_amount_from_pair(self, key, pool, amount, network, rpc_url=None):
        url = self.url + "calculateReservesAmountsFromPair"
        headers = { 'X-API-KEY': key }
        data = {
            "network": network,
            "pool": pool,
            "amount": amount,
            "rpc_url": rpc_url
        }
        response = requests.get(url, json=data, headers=headers)
        return response.json()
    
    def get_reserves_from_pair(self, key, pool, network, rpc_url=None):
        url = self.url + "getReservesFromPair"
        headers = { 'X-API-KEY': key }
        data = {
            "network": network,
            "pool": pool,
            "rpc_url": rpc_url
        }
        response = requests.get(url, json=data, headers=headers)
        return response.json()





