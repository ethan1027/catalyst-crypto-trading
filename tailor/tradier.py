import requests

response = requests.get('https://sandbox.tradier.com/v1/markets/history',
    params={'symbol': 'AAPL', 'interval': 'minute'},
    headers={'Authorization': 'Bearer pMvH8xPsbidNtBicXzBekIzYZ8hM', 'Accept': 'application/json'}
)
json_response = response.json()
print(response.status_code)
print(json_response)
