import requests

while True:
    for n in range(23, 51):
        response = requests.get('http://192.168.1.132:5000/' + f'test/{n}')
        print(response)
        response = requests.get('http://192.168.1.132:5000/' + f'test/{n}')
        print(response)