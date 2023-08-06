import json
import click
import requests
import json
import socket

# @click.command()
def main():

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    req = requests.get('http://ipinfo.io/json')

    response = req.json()
    
    if req.status_code == 200:
        
        response['LocalIP'] = local_ip
        print(json.dumps(response,indent=4))

    else:
        print("There seems to be a problem with requesting data, Please try again")

if __name__ == '__main__':
    main()