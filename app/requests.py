import requests


def fetchTokensData():
    url = 'https://the-open-league-static-data.s3.amazonaws.com/season/S5/tokens.json'
    response = requests.get(url)
    tokens = response.json()['items']
    return tokens
